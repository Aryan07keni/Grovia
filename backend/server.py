from fastapi import FastAPI, APIRouter, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import uuid
import logging
import math
import httpx
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
import razorpay
import random
from sms_service import send_otp_sms

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Config
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
JWT_SECRET = os.environ.get('JWT_SECRET', 'grovia_jwt_secret_key_2024_secure')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

# Import seed data
from seed_data import (
    CATEGORIES, PRODUCTS, STORES, STORE_PRODUCTS,
    get_product_by_id, get_category_by_id, get_store_by_id,
    get_products_by_category, search_products, get_store_products,
    get_product_store_availability
)

# ===== CREATE APP FIRST =====
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ===== ML RECOMMENDER SETUP =====
ML_AVAILABLE = False
try:
    from ml.recommender import recommender
    ML_AVAILABLE = True
    logger.info("ML Recommender loaded successfully")
except ImportError as e:
    logger.warning(f"ML Recommender not available: {e}")
    class DummyRecommender:
        is_trained = False
        def get_hybrid_recommendations(self, *args, **kwargs):
            return []
        def load_model(self, *args, **kwargs):
            return False
    recommender = DummyRecommender()

# ===== STARTUP EVENT (NOW APP IS DEFINED) =====
@app.on_event("startup")
async def startup_event():
    """Initialize ML recommender on startup"""
    if ML_AVAILABLE:
        try:
            if not recommender.load_model():
                logger.info("No existing model found. ML will train as data comes in.")
        except Exception as e:
            logger.error(f"Failed to initialize recommender: {e}")
    else:
        logger.info("ML Recommender disabled - continuing without ML")

# ===== HELPER FUNCTIONS =====
def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points in km"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# ===== IN-MEMORY DATA STORES =====
users_db = {}
carts_db = {}
orders_db = {}
addresses_db = {}
wishlists_db = {}
user_interactions = {}
otp_store = {}

# ===== PYDANTIC MODELS =====
class GoogleAuthRequest(BaseModel):
    credential: str

class PhoneAuthRequest(BaseModel):
    phone: str
    otp: Optional[str] = None

class CartItemAdd(BaseModel):
    product_id: str
    store_id: str
    quantity: int = 1
    weight_option: str

class CartItemUpdate(BaseModel):
    quantity: int

class OrderCreate(BaseModel):
    address_id: str
    payment_method: str
    store_id: str

class AddressCreate(BaseModel):
    label: str = "Home"
    full_address: str
    city: str = ""
    pincode: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class CreateOrderRequest(BaseModel):
    amount: int
    currency: str = "INR"

class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str
    order_id: str

# ===== AUTH HELPERS =====
def create_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token_str):
    try:
        payload = jwt.decode(token_str, JWT_SECRET, algorithms=['HS256'])
        return payload
    except JWTError:
        return None

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token_str = authorization.replace("Bearer ", "")
    payload = verify_token(token_str)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get('user_id')
    if user_id not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    return users_db[user_id]

def get_optional_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    token_str = authorization.replace("Bearer ", "")
    payload = verify_token(token_str)
    if not payload:
        return None
    user_id = payload.get('user_id')
    return users_db.get(user_id)

# ===== AUTH ROUTES =====
@api_router.post("/auth/google")
async def google_auth(req: GoogleAuthRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={req.credential}"
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Google token")
            google_data = resp.json()

        email = google_data.get('email')
        name = google_data.get('name', email.split('@')[0])
        picture = google_data.get('picture', '')

        existing = next((u for u in users_db.values() if u['email'] == email), None)
        if existing:
            user_id = existing['id']
            users_db[user_id].update({'name': name, 'picture': picture})
        else:
            user_id = str(uuid.uuid4())
            users_db[user_id] = {
                'id': user_id, 'name': name, 'email': email,
                'picture': picture, 'phone': '', 'created_at': datetime.now(timezone.utc).isoformat()
            }
            carts_db[user_id] = []
            addresses_db[user_id] = []
            wishlists_db[user_id] = []

        token = create_token(user_id, email)
        return {**users_db[user_id], 'token': token}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google auth error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@api_router.post("/auth/phone")
async def phone_auth(req: PhoneAuthRequest):
    if req.otp:
        record = otp_store.get(req.phone)
        is_demo = req.otp in ["1234", "123456"]
        is_valid_otp = record and record['otp'] == req.otp and record['expires_at'] > datetime.now(timezone.utc)
        
        if is_valid_otp or is_demo:
            if record:
                otp_store.pop(req.phone, None)
            existing = next((u for u in users_db.values() if u.get('phone') == req.phone), None)
            if existing:
                user_id = existing['id']
            else:
                user_id = str(uuid.uuid4())
                users_db[user_id] = {
                    'id': user_id, 'name': f'User_{req.phone[-4:]}',
                    'email': f'{req.phone}@grovia.app', 'picture': '',
                    'phone': req.phone, 'created_at': datetime.now(timezone.utc).isoformat()
                }
                carts_db[user_id] = []
                addresses_db[user_id] = []
                wishlists_db[user_id] = []
            token = create_token(user_id, users_db[user_id]['email'])
            return {**users_db[user_id], 'token': token}
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    
    # Generate 6-digit OTP
    otp_code = f"{random.randint(100000, 999999):06d}"
    otp_store[req.phone] = {
        'otp': otp_code,
        'expires_at': datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    await send_otp_sms(req.phone, otp_code)
    return {"message": "OTP sent successfully via SMS", "phone": req.phone}

@api_router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    return user

# ===== PRODUCT ROUTES =====
@api_router.get("/products")
async def list_products(category: Optional[str] = None, store: Optional[str] = None, limit: int = 50, offset: int = 0):
    if store:
        products = get_store_products(store)
    elif category:
        products = get_products_by_category(category)
    else:
        products = PRODUCTS.copy()
    total = len(products)
    products = products[offset:offset + limit]
    return {"products": products, "total": total}

@api_router.get("/products/search")
async def search_products_api(q: str = ""):
    if not q:
        return {"products": [], "total": 0}
    results = search_products(q)
    return {"products": results, "total": len(results)}

@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    availability = get_product_store_availability(product_id)
    category = get_category_by_id(product["category_id"])
    related = [p for p in get_products_by_category(product["category_id"]) if p["id"] != product_id][:8]
    return {**product, "store_availability": availability, "category": category, "related_products": related}

# ===== CATEGORY ROUTES =====
@api_router.get("/categories")
async def list_categories():
    cats_with_count = []
    for cat in CATEGORIES:
        count = len(get_products_by_category(cat["id"]))
        cats_with_count.append({**cat, "product_count": count})
    return {"categories": cats_with_count}

# ===== STORE ROUTES =====
@api_router.get("/stores")
async def list_stores():
    return {"stores": STORES}

@api_router.get("/stores/nearby")
async def nearby_stores(lat: float = 12.9352, lng: float = 77.6245):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    stores_with_distance = []
    for store in STORES:
        dist = haversine(lat, lng, store["lat"], store["lng"])
        stores_with_distance.append({**store, "distance_km": round(dist, 1)})
    stores_with_distance.sort(key=lambda x: x["distance_km"])
    return {"stores": stores_with_distance}

@api_router.get("/stores/nearby-real")
async def get_nearby_real_stores(lat: float = 12.9352, lng: float = 77.6245, radius: int = 5000):
    """Get stores with distance calculation based on user location"""
    try:
        stores_with_distance = []
        for store in STORES:
            distance = calculate_distance(lat, lng, store["lat"], store["lng"])
            if distance <= radius / 1000:
                stores_with_distance.append({
                    **store,
                    "distance_km": round(distance, 1)
                })
        
        stores_with_distance.sort(key=lambda x: x["distance_km"])
        return {"stores": stores_with_distance, "total": len(stores_with_distance)}
    except Exception as e:
        logger.error(f"Error fetching stores: {e}")
        stores_with_distance = []
        for store in STORES:
            distance = calculate_distance(lat, lng, store["lat"], store["lng"])
            stores_with_distance.append({**store, "distance_km": round(distance, 1)})
        stores_with_distance.sort(key=lambda x: x["distance_km"])
        return {"stores": stores_with_distance, "total": len(stores_with_distance)}

@api_router.get("/stores/{store_id}")
async def get_store(store_id: str):
    store = get_store_by_id(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    products = get_store_products(store_id)
    return {**store, "products": products, "product_count": len(products)}

@api_router.get("/stores/{store_id}/products")
async def get_store_products_api(store_id: str, category: Optional[str] = None):
    products = get_store_products(store_id)
    if category:
        products = [p for p in products if p["category_id"] == category]
    return {"products": products, "total": len(products)}

# ===== CART ROUTES =====
@api_router.get("/cart")
async def get_cart(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    cart = carts_db.get(user['id'], [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    delivery_fee = 25 if subtotal < 500 else 0
    return {
        "items": cart, "subtotal": subtotal,
        "delivery_fee": delivery_fee, "total": subtotal + delivery_fee,
        "item_count": sum(item['quantity'] for item in cart)
    }

@api_router.post("/cart")
async def add_to_cart(item: CartItemAdd, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    user_id = user['id']
    if user_id not in carts_db:
        carts_db[user_id] = []

    product = get_product_by_id(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    store_prods = STORE_PRODUCTS.get(item.store_id, {})
    pricing = store_prods.get(item.product_id)
    price = pricing['price'] if pricing else product['base_price']

    existing = next((c for c in carts_db[user_id] if c['product_id'] == item.product_id and c['store_id'] == item.store_id), None)
    if existing:
        existing['quantity'] += item.quantity
        existing['weight_option'] = item.weight_option
    else:
        cart_item = {
            'id': str(uuid.uuid4()),
            'product_id': item.product_id,
            'store_id': item.store_id,
            'name': product['name'],
            'image': product['image'],
            'price': price,
            'mrp': product['mrp'],
            'quantity': item.quantity,
            'weight_option': item.weight_option,
            'store_name': get_store_by_id(item.store_id)['name'] if get_store_by_id(item.store_id) else ''
        }
        carts_db[user_id].append(cart_item)

    if user_id not in user_interactions:
        user_interactions[user_id] = []
    user_interactions[user_id].append(item.product_id)

    cart = carts_db[user_id]
    subtotal = sum(c['price'] * c['quantity'] for c in cart)
    delivery_fee = 25 if subtotal < 500 else 0
    return {"items": cart, "subtotal": subtotal, "delivery_fee": delivery_fee, "total": subtotal + delivery_fee, "item_count": sum(c['quantity'] for c in cart)}

@api_router.put("/cart/{item_id}")
async def update_cart_item(item_id: str, update: CartItemUpdate, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    cart = carts_db.get(user['id'], [])
    item = next((c for c in cart if c['id'] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if update.quantity <= 0:
        carts_db[user['id']] = [c for c in cart if c['id'] != item_id]
    else:
        item['quantity'] = update.quantity
    cart = carts_db[user['id']]
    subtotal = sum(c['price'] * c['quantity'] for c in cart)
    delivery_fee = 25 if subtotal < 500 else 0
    return {"items": cart, "subtotal": subtotal, "delivery_fee": delivery_fee, "total": subtotal + delivery_fee, "item_count": sum(c['quantity'] for c in cart)}

@api_router.delete("/cart/{item_id}")
async def remove_cart_item(item_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    cart = carts_db.get(user['id'], [])
    carts_db[user['id']] = [c for c in cart if c['id'] != item_id]
    cart = carts_db[user['id']]
    subtotal = sum(c['price'] * c['quantity'] for c in cart)
    delivery_fee = 25 if subtotal < 500 else 0
    return {"items": cart, "subtotal": subtotal, "delivery_fee": delivery_fee, "total": subtotal + delivery_fee, "item_count": sum(c['quantity'] for c in cart)}

# ===== ORDER ROUTES =====
@api_router.post("/orders")
async def create_order(order: OrderCreate, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    user_id = user['id']
    cart = carts_db.get(user_id, [])
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    subtotal = sum(c['price'] * c['quantity'] for c in cart)
    delivery_fee = 25 if subtotal < 500 else 0
    order_id = str(uuid.uuid4())
    is_cod = order.payment_method.lower() in ['cod', 'cash on delivery', 'pay on delivery']
    order_obj = {
        'id': order_id, 'user_id': user_id,
        'items': cart.copy(), 'subtotal': subtotal,
        'delivery_fee': delivery_fee, 'total': subtotal + delivery_fee,
        'address_id': order.address_id, 'payment_method': order.payment_method,
        'store_id': order.store_id, 'status': 'confirmed' if is_cod else 'pending',
        'payment_status': 'pay_on_delivery' if is_cod else 'pending',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'estimated_delivery': '15-20 min'
    }
    orders_db[order_id] = order_obj
    if is_cod:
        carts_db[user_id] = []
    return order_obj

@api_router.get("/orders")
async def list_orders(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    user_orders = [o for o in orders_db.values() if o['user_id'] == user['id']]
    user_orders.sort(key=lambda x: x['created_at'], reverse=True)
    return {"orders": user_orders}

@api_router.get("/orders/{order_id}")
async def get_order(order_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    order = orders_db.get(order_id)
    if not order or order['user_id'] != user['id']:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# ===== RAZORPAY PAYMENT ROUTES =====
@api_router.post("/create-razorpay-order")
async def create_razorpay_order(request: CreateOrderRequest, authorization: Optional[str] = Header(None)):
    """Create Razorpay order"""
    try:
        user = get_current_user(authorization)
        
        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            raise HTTPException(status_code=500, detail="Razorpay not configured")
        
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        order_data = {
            'amount': request.amount * 100,
            'currency': request.currency,
            'receipt': f'order_{datetime.now().timestamp()}',
            'payment_capture': 1
        }
        
        order = client.order.create(data=order_data)
        
        return {
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key_id": RAZORPAY_KEY_ID
        }
    except Exception as e:
        logger.error(f"Razorpay order creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/verify-razorpay-payment")
async def verify_razorpay_payment(request: VerifyPaymentRequest, authorization: Optional[str] = Header(None)):
    """Verify Razorpay payment"""
    try:
        user = get_current_user(authorization)
        
        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            raise HTTPException(status_code=500, detail="Razorpay not configured")
        
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        params_dict = {
            'razorpay_payment_id': request.razorpay_payment_id,
            'razorpay_order_id': request.razorpay_order_id,
            'razorpay_signature': request.razorpay_signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        if request.order_id in orders_db:
            orders_db[request.order_id]['status'] = 'confirmed'
            orders_db[request.order_id]['payment_status'] = 'paid'
            orders_db[request.order_id]['payment_id'] = request.razorpay_payment_id
            orders_db[request.order_id]['razorpay_order_id'] = request.razorpay_order_id
            carts_db[user['id']] = []
        
        return {"status": "success", "message": "Payment verified successfully"}
        
    except Exception as e:
        logger.error(f"Payment verification error: {e}")
        raise HTTPException(status_code=400, detail="Payment verification failed")

# ===== USER PROFILE ROUTES =====
@api_router.get("/user/profile")
async def get_profile(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    return user

@api_router.put("/user/profile")
async def update_profile(update: ProfileUpdate, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if update.name:
        users_db[user['id']]['name'] = update.name
    if update.phone:
        users_db[user['id']]['phone'] = update.phone
    if update.email:
        users_db[user['id']]['email'] = update.email
    return users_db[user['id']]

@api_router.get("/user/addresses")
async def get_addresses(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    return {"addresses": addresses_db.get(user['id'], [])}

@api_router.post("/user/addresses")
async def add_address(addr: AddressCreate, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if user['id'] not in addresses_db:
        addresses_db[user['id']] = []
    address = {
        'id': str(uuid.uuid4()), 'label': addr.label,
        'full_address': addr.full_address, 'city': addr.city,
        'pincode': addr.pincode, 'lat': addr.lat, 'lng': addr.lng
    }
    addresses_db[user['id']].append(address)
    return address

@api_router.delete("/user/addresses/{address_id}")
async def delete_address(address_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    addrs = addresses_db.get(user['id'], [])
    addresses_db[user['id']] = [a for a in addrs if a['id'] != address_id]
    return {"message": "Address deleted"}

@api_router.get("/user/wishlist")
async def get_wishlist(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    wishlist_ids = wishlists_db.get(user['id'], [])
    products = [get_product_by_id(pid) for pid in wishlist_ids if get_product_by_id(pid)]
    return {"wishlist": products}

@api_router.post("/user/wishlist/{product_id}")
async def add_to_wishlist(product_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if user['id'] not in wishlists_db:
        wishlists_db[user['id']] = []
    if product_id not in wishlists_db[user['id']]:
        wishlists_db[user['id']].append(product_id)
    return {"message": "Added to wishlist"}

@api_router.delete("/user/wishlist/{product_id}")
async def remove_from_wishlist(product_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    wl = wishlists_db.get(user['id'], [])
    wishlists_db[user['id']] = [pid for pid in wl if pid != product_id]
    return {"message": "Removed from wishlist"}

# ===== RECOMMENDATIONS =====
@api_router.get("/recommendations")
async def get_recommendations(authorization: Optional[str] = Header(None)):
    """Get personalized recommendations"""
    user = get_optional_user(authorization)
    
    if ML_AVAILABLE and recommender.is_trained and user:
        try:
            ml_recs = recommender.get_hybrid_recommendations(
                user_id=user['id'],
                n=12
            )
            
            if ml_recs:
                recommended_products = []
                for rec in ml_recs:
                    product = get_product_by_id(rec['product_id'])
                    if product:
                        recommended_products.append(product)
                
                if recommended_products:
                    return {"products": recommended_products, "source": "ml_hybrid"}
        except Exception as e:
            logger.error(f"ML recommendation error: {e}")
    
    # Fallback: Return popular products
    popular = [p for p in PRODUCTS if p.get('rating', 0) > 4.0][:12]
    if not popular:
        popular = PRODUCTS[:12]
    
    return {"products": popular, "source": "popular"}

# ===== MAPS CONFIG =====
@api_router.get("/maps/config")
async def maps_config():
    return {"api_key": GOOGLE_MAPS_API_KEY}

# ===== HEALTH =====
@api_router.get("/")
async def api_root():
    return {"message": "Grovia API", "status": "running"}

@app.get("/")
@app.get("/health")
async def app_root():
    return {"message": "Grovia API Health OK", "status": "running"}

# Include router
app.include_router(api_router)