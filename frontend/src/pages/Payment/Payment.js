import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../../context/AppContext';
import FloatingGroceries from '../../components/FloatingGroceries/FloatingGroceries';
import { MapPin, Check, ArrowLeft, ShieldCheck, Truck, Wallet } from 'lucide-react';
import axios from 'axios';
import './Payment.css';

function Payment() {
  const { cart, API, getAuthHeaders, selectedStore, fetchCart } = useApp();
  const navigate = useNavigate();
  const [address, setAddress] = useState({ label: 'Home', full_address: '', city: '', pincode: '' });
  const [savedAddresses, setSavedAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const res = await axios.get(`${API}/user/addresses`, { headers: getAuthHeaders() });
      setSavedAddresses(res.data.addresses || []);
      if (res.data.addresses?.length > 0) setSelectedAddress(res.data.addresses[0].id);
    } catch (e) { console.error(e); }
  };

  const handleAddAddress = async () => {
    if (!address.full_address || !address.pincode) return;
    try {
      const res = await axios.post(`${API}/user/addresses`, address, { headers: getAuthHeaders() });
      setSavedAddresses([...savedAddresses, res.data]);
      setSelectedAddress(res.data.id);
      setAddress({ label: 'Home', full_address: '', city: '', pincode: '' });
    } catch (e) { console.error(e); }
  };

  // Load Razorpay script
  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      if (window.Razorpay) {
        resolve(true);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  // Handle Razorpay payment
  const handleRazorpayPayment = async (createdOrderId) => {
    try {
      // Step 1: Create Razorpay order
      const razorpayOrderResponse = await axios.post(
        `${API}/create-razorpay-order`,
        {
          amount: cart.total,
          currency: 'INR'
        },
        { headers: getAuthHeaders() }
      );
      
      const { order_id, amount, currency, key_id } = razorpayOrderResponse.data;
      
      // Step 2: Load Razorpay script
      const scriptLoaded = await loadRazorpayScript();
      if (!scriptLoaded) {
        alert('Failed to load Razorpay. Please check your internet connection.');
        return false;
      }
      
      // Step 3: Get selected address details
      const selectedAddr = savedAddresses.find(addr => addr.id === selectedAddress);
      
      // Step 4: Configure Razorpay options
      const options = {
        key: key_id,
        amount: amount,
        currency: currency,
        name: 'Grovia',
        description: `Order from ${selectedStore?.name || 'Grovia'}`,
        order_id: order_id,
        handler: async (response) => {
          // Step 5: Verify payment
          try {
            const verifyResponse = await axios.post(
              `${API}/verify-razorpay-payment`,
              {
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_signature: response.razorpay_signature,
                order_id: createdOrderId
              },
              { headers: getAuthHeaders() }
            );
            
            if (verifyResponse.data.status === 'success') {
              setOrderId(createdOrderId);
              setOrderPlaced(true);
              fetchCart();
              setProcessing(false);
              return true;
            }
          } catch (error) {
            console.error('Payment verification failed:', error);
            alert('Payment verification failed. Please contact support.');
            return false;
          }
        },
        prefill: {
          name: '',
          email: '',
          contact: ''
        },
        notes: {
          address: selectedAddr?.full_address || '',
          store: selectedStore?.name || ''
        },
        theme: {
          color: '#2e7d32'
        },
        modal: {
          ondismiss: () => {
            setProcessing(false);
          }
        }
      };
      
      const razorpay = new window.Razorpay(options);
      razorpay.open();
      return true;
      
    } catch (error) {
      console.error('Razorpay order creation failed:', error);
      alert(error.response?.data?.detail || 'Failed to initialize payment. Please try again.');
      return false;
    }
  };

  const [paymentMethod, setPaymentMethod] = useState('Razorpay');

  const handlePlaceOrder = async () => {
    if (!selectedAddress && !address.full_address) return;
    setProcessing(true);
    
    try {
      let addrId = selectedAddress;
      if (!addrId && address.full_address) {
        const addrRes = await axios.post(`${API}/user/addresses`, address, { headers: getAuthHeaders() });
        addrId = addrRes.data.id;
      }
      
      if (paymentMethod === 'COD') {
        const res = await axios.post(`${API}/orders`, {
          address_id: addrId,
          payment_method: 'Pay on Delivery (COD)',
          store_id: selectedStore?.id || 'store-1'
        }, { headers: getAuthHeaders() });
        
        setOrderId(res.data.id);
        setOrderPlaced(true);
        fetchCart();
        setProcessing(false);
        return;
      }

      // Create order first for Razorpay
      const res = await axios.post(`${API}/orders`, {
        address_id: addrId,
        payment_method: 'Razorpay',
        store_id: selectedStore?.id || 'store-1'
      }, { headers: getAuthHeaders() });
      
      const createdOrderId = res.data.id;
      
      // Handle Razorpay payment
      await handleRazorpayPayment(createdOrderId);
      
    } catch (e) { 
      console.error(e);
      setProcessing(false);
    }
  };

  if (orderPlaced) {
    return (
      <div className="payment-page page-container" data-testid="order-success-page">
        <FloatingGroceries />
        <div className="order-success glass-card" data-testid="order-success">
          <div className="success-check"><Check size={48} /></div>
          <h1>Order Placed Successfully</h1>
          <p className="success-id">Order ID: {orderId.slice(0, 8).toUpperCase()}</p>
          <p className="success-msg">Your groceries will be delivered in 15-20 minutes</p>
          <div className="success-actions">
            <button className="btn-primary" onClick={() => navigate('/profile?tab=orders')} data-testid="view-orders-btn">View Orders</button>
            <button className="btn-outline" onClick={() => navigate('/')} data-testid="continue-shopping-btn">Continue Shopping</button>
          </div>
        </div>
      </div>
    );
  }

  if (cart.items.length === 0) { navigate('/cart'); return null; }

  return (
    <div className="payment-page page-container" data-testid="payment-page">
      <FloatingGroceries />
      <div className="payment-content">
        <button className="cart-back-btn" onClick={() => navigate('/cart')} data-testid="payment-back-btn">
          <ArrowLeft size={18} /> Back to Cart
        </button>
        <h1 className="payment-title">Checkout</h1>

        <div className="payment-layout">
          <div className="payment-left">
            {/* Delivery Address */}
            <div className="payment-section glass-card" data-testid="delivery-address-section">
              <h2><MapPin size={20} /> Delivery Address</h2>
              {savedAddresses.length > 0 && (
                <div className="saved-addresses">
                  {savedAddresses.map(addr => (
                    <div key={addr.id} className={`address-card ${selectedAddress === addr.id ? 'active' : ''}`}
                      onClick={() => setSelectedAddress(addr.id)} data-testid={`address-${addr.id}`}>
                      <span className="address-label">{addr.label}</span>
                      <span className="address-text">{addr.full_address}, {addr.city} - {addr.pincode}</span>
                    </div>
                  ))}
                </div>
              )}
              <div className="new-address-form">
                <h3>Add New Address</h3>
                <div className="form-row">
                  <input type="text" placeholder="Label (Home, Office...)" value={address.label}
                    onChange={(e) => setAddress({...address, label: e.target.value})} data-testid="address-label-input" />
                </div>
                <div className="form-row">
                  <input type="text" placeholder="Full address" value={address.full_address}
                    onChange={(e) => setAddress({...address, full_address: e.target.value})} data-testid="address-full-input" />
                </div>
                <div className="form-row-double">
                  <input type="text" placeholder="City" value={address.city}
                    onChange={(e) => setAddress({...address, city: e.target.value})} data-testid="address-city-input" />
                  <input type="text" placeholder="Pincode" value={address.pincode} maxLength={6}
                    onChange={(e) => setAddress({...address, pincode: e.target.value.replace(/\D/g, '')})} data-testid="address-pincode-input" />
                </div>
                <button className="btn-outline add-addr-btn" onClick={handleAddAddress} data-testid="add-address-btn">Save Address</button>
              </div>
            </div>

            {/* Payment Section */}
            <div className="payment-section glass-card" data-testid="payment-section">
              <h2><Wallet size={20} /> Payment Method</h2>
              <div className="payment-methods">
                <div className={`payment-method ${paymentMethod === 'Razorpay' ? 'active' : ''}`} 
                  onClick={() => setPaymentMethod('Razorpay')} data-testid="payment-razorpay">
                  <Wallet size={22} className="pm-icon" />
                  <div>
                    <span className="pm-name">Razorpay</span>
                    <span className="pm-desc">Pay securely with Credit/Debit Card, UPI, NetBanking</span>
                  </div>
                </div>

                <div className={`payment-method ${paymentMethod === 'COD' ? 'active' : ''}`} 
                  onClick={() => setPaymentMethod('COD')} data-testid="payment-cod">
                  <Truck size={22} className="pm-icon" />
                  <div>
                    <span className="pm-name">Cash / Pay on Delivery</span>
                    <span className="pm-desc">Pay cash or UPI to driver upon delivery</span>
                  </div>
                </div>
              </div>

              {paymentMethod === 'Razorpay' && (
                <div className="razorpay-info">
                  <p>You will be redirected to Razorpay secure payment page</p>
                  <div className="payment-icons">
                    <span>💳 Cards</span>
                    <span>📱 UPI</span>
                    <span>🏦 NetBanking</span>
                    <span>👛 Wallet</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="payment-right">
            <div className="order-summary-card glass-card" data-testid="payment-order-summary">
              <h2>Order Summary</h2>
              <div className="summary-items">
                {cart.items.map(item => (
                  <div key={item.id} className="summary-item">
                    <div className="summary-item-info">
                      <span className="summary-item-name">{item.name}</span>
                      <span className="summary-item-qty">x{item.quantity} ({item.weight_option})</span>
                    </div>
                    <span className="summary-item-price">Rs. {item.price * item.quantity}</span>
                  </div>
                ))}
              </div>
              <div className="summary-breakdown">
                <div className="summary-row"><span>Subtotal</span><span>Rs. {cart.subtotal}</span></div>
                <div className="summary-row"><span>Delivery</span><span>{cart.delivery_fee > 0 ? `Rs. ${cart.delivery_fee}` : 'FREE'}</span></div>
                <div className="summary-row total"><span>Total</span><span>Rs. {cart.total}</span></div>
              </div>
              <button className="btn-primary place-order-btn" onClick={handlePlaceOrder} disabled={processing} data-testid="place-order-btn">
                {processing ? 'Processing...' : (paymentMethod === 'Razorpay' ? `Pay ₹${cart.total} via Razorpay` : `Place Order (Pay ₹${cart.total} on Delivery)`)}
              </button>
              <div className="secure-badge"><ShieldCheck size={16} /> <span>100% Secure Checkout</span></div>
              <div className="delivery-info"><Truck size={16} /> <span>Estimated delivery: 15-20 min</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Payment;