"""
Grovia Grocery App - Comprehensive Seed Data
100+ products across 13 categories, 8 stores with Indian pricing
"""

CATEGORIES = [
    {"id": "cat-1", "name": "Fruits & Vegetables", "image": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=300&h=300&fit=crop", "icon": "apple"},
    {"id": "cat-2", "name": "Dairy & Breakfast", "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=300&fit=crop", "icon": "milk"},
    {"id": "cat-3", "name": "Snacks & Munchies", "image": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=300&h=300&fit=crop", "icon": "cookie"},
    {"id": "cat-4", "name": "Cold Drinks & Juices", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&h=300&fit=crop", "icon": "cup-soda"},
    {"id": "cat-5", "name": "Instant & Frozen Food", "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=300&h=300&fit=crop", "icon": "flame"},
    {"id": "cat-6", "name": "Tea, Coffee & Health Drinks", "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300&h=300&fit=crop", "icon": "coffee"},
    {"id": "cat-7", "name": "Bakery & Biscuits", "image": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300&h=300&fit=crop", "icon": "croissant"},
    {"id": "cat-8", "name": "Sweet Tooth", "image": "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=300&h=300&fit=crop", "icon": "candy"},
    {"id": "cat-9", "name": "Atta, Rice & Dal", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop", "icon": "wheat"},
    {"id": "cat-10", "name": "Masala, Oil & More", "image": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&h=300&fit=crop", "icon": "flame-kindling"},
    {"id": "cat-11", "name": "Baby Care", "image": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop", "icon": "baby"},
    {"id": "cat-12", "name": "Personal Care", "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=300&h=300&fit=crop", "icon": "sparkles"},
    {"id": "cat-13", "name": "Cleaning Essentials", "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300&h=300&fit=crop", "icon": "spray-can"},
]

PRODUCTS = [
    # ====== FRUITS & VEGETABLES (cat-1) ======
    {"id": "p1", "name": "Fresh Red Apple", "category_id": "cat-1", "description": "Crisp and juicy Shimla red apples, handpicked from premium orchards. Rich in fiber and antioxidants, perfect for daily snacking or making fresh juice.", "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=400&fit=crop", "weight_options": ["250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 85, "mrp": 120, "unit": "per kg", "rating": 4.5},
    {"id": "p2", "name": "Fresh Banana", "category_id": "cat-1", "description": "Naturally ripened yellow bananas, great source of potassium and energy. Perfect for smoothies, breakfast bowls, or as a quick snack.", "image": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop", "weight_options": ["6 pcs", "12 pcs"], "default_weight": "6 pcs", "base_price": 40, "mrp": 55, "unit": "per dozen", "rating": 4.3},
    {"id": "p3", "name": "Orange - Nagpur", "category_id": "cat-1", "description": "Sweet and tangy Nagpur oranges, bursting with Vitamin C. These seedless oranges are perfect for juicing or eating fresh.", "image": "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 70, "mrp": 95, "unit": "per kg", "rating": 4.4},
    {"id": "p4", "name": "Alphonso Mango", "category_id": "cat-1", "description": "The king of mangoes! Premium Ratnagiri Alphonso mangoes with rich golden pulp, heavenly aroma, and unmatched sweetness.", "image": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 350, "mrp": 450, "unit": "per kg", "rating": 4.8},
    {"id": "p5", "name": "Green Grapes - Seedless", "category_id": "cat-1", "description": "Fresh seedless green grapes, crisp and sweet. Great for snacking, adding to fruit salads, or as a healthy dessert.", "image": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&h=400&fit=crop", "weight_options": ["250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 65, "mrp": 85, "unit": "per kg", "rating": 4.2},
    {"id": "p6", "name": "Pomegranate", "category_id": "cat-1", "description": "Ruby-red pomegranate seeds packed with antioxidants. Known for boosting heart health and immunity. Each fruit is carefully selected.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8W2gegNZ9-2YyE_efhyW-uJ16tGF_YsiMlQ&s&fit=crop", "weight_options": ["1 pc", "2 pcs", "500g"], "default_weight": "1 pc", "base_price": 60, "mrp": 80, "unit": "per pc", "rating": 4.3},
    {"id": "p7", "name": "Watermelon", "category_id": "cat-1", "description": "Refreshing and hydrating watermelon, perfect for hot summer days. Sweet, juicy red flesh with minimal seeds.", "image": "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop", "weight_options": ["1 pc (2-3 kg)", "Half cut"], "default_weight": "1 pc (2-3 kg)", "base_price": 45, "mrp": 65, "unit": "per pc", "rating": 4.1},
    {"id": "p8", "name": "Fresh Tomato", "category_id": "cat-1", "description": "Farm-fresh red tomatoes, essential for every Indian kitchen. Perfect for curries, salads, chutneys, and soups.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN9-OuOtsl4iecwrOQ4c00iOqngoUdBz1dzQ&sw=400&h=400&fit=crop", "weight_options": ["250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 30, "mrp": 45, "unit": "per kg", "rating": 4.0},
    {"id": "p9", "name": "Potato", "category_id": "cat-1", "description": "Premium quality potatoes, versatile for every recipe. From aloo paratha to french fries, these potatoes are perfect for all dishes.", "image": "https://www.bbassets.com/media/uploads/p/l/40048457_20-fresho-potato-new-crop.jpg&fit=crop", "weight_options": ["500g", "1 kg", "2 kg", "5 kg"], "default_weight": "1 kg", "base_price": 25, "mrp": 35, "unit": "per kg", "rating": 4.2},
    {"id": "p10", "name": "Onion", "category_id": "cat-1", "description": "Fresh red onions, a staple in Indian cooking. Essential for curries, biryanis, salads, and everyday cooking.", "image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg", "5 kg"], "default_weight": "1 kg", "base_price": 35, "mrp": 50, "unit": "per kg", "rating": 4.1},
    {"id": "p11", "name": "Carrot - Ooty", "category_id": "cat-1", "description": "Fresh Ooty carrots, naturally sweet and crunchy. Rich in beta-carotene and perfect for salads, juices, and halwa.", "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400&h=400&fit=crop", "weight_options": ["250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 40, "mrp": 55, "unit": "per kg", "rating": 4.3},
    {"id": "p12", "name": "Green Capsicum", "category_id": "cat-1", "description": "Crunchy green bell peppers, great for stir-fries, stuffed capsicum, salads, and sandwiches. Rich in Vitamin C.", "image": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400&h=400&fit=crop", "weight_options": ["250g", "500g"], "default_weight": "250g", "base_price": 35, "mrp": 50, "unit": "per kg", "rating": 4.0},
    {"id": "p13", "name": "Broccoli", "category_id": "cat-1", "description": "Fresh green broccoli florets, packed with vitamins and minerals. Perfect for stir-fries, soups, and healthy salads.", "image": "https://tse3.mm.bing.net/th/id/OIP.7hcOKFs2NkgQo8XFgwHarwHaE7?pid=Api&P=0&h=180&fit=crop", "weight_options": ["250g", "500g"], "default_weight": "250g", "base_price": 55, "mrp": 75, "unit": "per kg", "rating": 4.2},
    {"id": "p14", "name": "Baby Spinach", "category_id": "cat-1", "description": "Tender baby spinach leaves, washed and ready to use. Great for salads, smoothies, palak paneer, and pasta.", "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 30, "mrp": 45, "unit": "per bunch", "rating": 4.1},
    {"id": "p15", "name": "Cauliflower", "category_id": "cat-1", "description": "Fresh white cauliflower, perfect for gobi manchurian, aloo gobi, and paratha stuffing. Naturally grown and pesticide-free.", "image": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop", "weight_options": ["1 pc (400-500g)", "1 pc (700g-1kg)"], "default_weight": "1 pc (400-500g)", "base_price": 35, "mrp": 50, "unit": "per pc", "rating": 4.0},
    {"id": "p16", "name": "Papaya", "category_id": "cat-1", "description": "Ripe sweet papaya, rich in enzymes and vitamins. Excellent for digestion and makes a great breakfast fruit.", "image": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=400&h=400&fit=crop", "weight_options": ["1 pc (500g-1kg)"], "default_weight": "1 pc (500g-1kg)", "base_price": 45, "mrp": 60, "unit": "per pc", "rating": 4.0},

    # ====== DAIRY & BREAKFAST (cat-2) ======
    {"id": "p17", "name": "Amul Toned Milk", "category_id": "cat-2", "description": "Amul Toned Milk with 3% fat content. Pasteurized and homogenized for safe consumption. Perfect for tea, coffee, and daily use.", "image": "https://m.media-amazon.com/images/I/41wtmuLk21L._AC_UF894,1000_QL80_.jpgw=400&h=400&fit=crop", "weight_options": ["500 ml", "1 L", "2 L"], "default_weight": "1 L", "base_price": 28, "mrp": 32, "unit": "per litre", "rating": 4.5},
    {"id": "p18", "name": "Amul Fresh Curd", "category_id": "cat-2", "description": "Thick and creamy Amul dahi, made from pasteurized toned milk. Perfect for raita, lassi, kadhi, and daily meals.", "image": "https://cdn.grofers.com/da/cms-assets/cms/product/2107cdc3-8d54-41fb-a7ee-89d8573b9f06.jpg&fit=crop", "weight_options": ["200g", "400g", "1 kg"], "default_weight": "400g", "base_price": 30, "mrp": 35, "unit": "per pack", "rating": 4.3},
    {"id": "p19", "name": "Amul Paneer", "category_id": "cat-2", "description": "Fresh and soft Amul paneer block, made from pure cow milk. Ideal for paneer tikka, palak paneer, and kadai paneer.", "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&h=400&fit=crop", "weight_options": ["200g", "500g", "1 kg"], "default_weight": "200g", "base_price": 80, "mrp": 95, "unit": "per pack", "rating": 4.6},
    {"id": "p20", "name": "Amul Butter", "category_id": "cat-2", "description": "Amul pasteurized butter, utterly butterly delicious. Perfect for parathas, toast, cooking, and baking.", "image": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 56, "mrp": 60, "unit": "per pack", "rating": 4.7},
    {"id": "p21", "name": "Amul Cheese Slices", "category_id": "cat-2", "description": "Processed cheese slices, perfect for sandwiches, burgers, and grilled cheese. Each slice melts beautifully.", "image": "https://www.bbassets.com/media/uploads/p/l/104808_9-amul-cheese-slices.jpgw=400&h=400&fit=crop", "weight_options": ["5 slices", "10 slices", "20 slices"], "default_weight": "10 slices", "base_price": 95, "mrp": 110, "unit": "per pack", "rating": 4.4},
    {"id": "p22", "name": "Farm Fresh Eggs", "category_id": "cat-2", "description": "Farm fresh white eggs, protein-packed and perfect for breakfast. Great for omelettes, boiled eggs, and baking.", "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=400&fit=crop", "weight_options": ["6 pcs", "12 pcs", "30 pcs"], "default_weight": "12 pcs", "base_price": 72, "mrp": 84, "unit": "per tray", "rating": 4.3},
    {"id": "p23", "name": "Britannia White Bread", "category_id": "cat-2", "description": "Soft and fresh Britannia white bread, perfect for sandwiches, toast, and breakfast. Made with the finest ingredients.", "image": "https://www.britannia.co.in/_next/image?url=https:%2F%2Fd22qhov8mohr82.cloudfront.net%2F98790_BRITANNIA_HEALTHY_SLICE_BREAD_450_G_f6ca184077.png&w=1920&q=100&fit=crop", "weight_options": ["400g", "800g"], "default_weight": "400g", "base_price": 35, "mrp": 40, "unit": "per pack", "rating": 4.1},
    {"id": "p24", "name": "Kelloggs Cornflakes", "category_id": "cat-2", "description": "Crunchy golden corn flakes, a classic breakfast cereal. Enjoy with cold milk and fruits for a nutritious start to your day.", "image": "https://images.unsplash.com/photo-1521483451569-e33803c0330c?w=400&h=400&fit=crop", "weight_options": ["250g", "475g", "875g"], "default_weight": "475g", "base_price": 175, "mrp": 210, "unit": "per box", "rating": 4.2},
    {"id": "p25", "name": "Greek Yogurt - Plain", "category_id": "cat-2", "description": "Thick and creamy Greek yogurt, high in protein and probiotics. Perfect for smoothie bowls, dips, and healthy desserts.", "image": "https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "400g"], "default_weight": "200g", "base_price": 60, "mrp": 75, "unit": "per cup", "rating": 4.4},

    # ====== SNACKS & MUNCHIES (cat-3) ======
    {"id": "p26", "name": "Lays Classic Salted", "category_id": "cat-3", "description": "Crispy and light Lays potato chips with classic salted flavor. The perfect snack for movie nights and parties.", "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&h=400&fit=crop", "weight_options": ["25g", "52g", "130g", "235g"], "default_weight": "130g", "base_price": 40, "mrp": 50, "unit": "per pack", "rating": 4.3},
    {"id": "p27", "name": "Kurkure Masala Munch", "category_id": "cat-3", "description": "Crunchy and spicy Kurkure with authentic Indian masala flavor. A favorite tea-time snack across India.", "image": "https://www.bbassets.com/media/uploads/p/l/102761_18-kurkure-namkeen-masala-munch.jpgw=400&h=400&fit=crop", "weight_options": ["25g", "75g", "155g"], "default_weight": "75g", "base_price": 20, "mrp": 25, "unit": "per pack", "rating": 4.1},
    {"id": "p28", "name": "Haldiram Aloo Bhujia", "category_id": "cat-3", "description": "Traditional Haldiram's aloo bhujia namkeen, a classic Indian savory snack. Crispy, spicy, and absolutely addictive.", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=400&fit=crop", "weight_options": ["150g", "350g", "1 kg"], "default_weight": "350g", "base_price": 85, "mrp": 99, "unit": "per pack", "rating": 4.5},
    {"id": "p29", "name": "Pringles Original", "category_id": "cat-3", "description": "Iconic Pringles stackable chips with original flavor. Perfectly seasoned and impossibly uniform for satisfying crunch.", "image": "https://www.bbassets.com/media/uploads/p/l/40312565_3-pringles-sour-cream-onion-potato-chips.jpgw=400&h=400&fit=crop", "weight_options": ["37g", "107g", "165g"], "default_weight": "107g", "base_price": 99, "mrp": 120, "unit": "per can", "rating": 4.4},
    {"id": "p30", "name": "Doritos Nacho Cheese", "category_id": "cat-3", "description": "Bold and cheesy Doritos tortilla chips with nacho cheese flavor. Perfect for dipping with salsa or guacamole.", "image": "https://images.unsplash.com/photo-1613919113640-25732ec5e61f?w=400&h=400&fit=crop", "weight_options": ["44g", "140g"], "default_weight": "140g", "base_price": 55, "mrp": 65, "unit": "per pack", "rating": 4.2},
    {"id": "p31", "name": "Act II Microwave Popcorn", "category_id": "cat-3", "description": "Butter-flavored microwave popcorn, ready in just 3 minutes. Perfect for movie nights at home.", "image": "https://images.unsplash.com/photo-1585735878802-5145e0e tried?w=400&h=400&fit=crop", "weight_options": ["99g", "297g (3 pack)"], "default_weight": "99g", "base_price": 45, "mrp": 55, "unit": "per pack", "rating": 4.0},
    {"id": "p32", "name": "Bingo Mad Angles", "category_id": "cat-3", "description": "Tangy tomato flavored triangle-shaped chips. A uniquely Indian snack with bold flavors and satisfying crunch.", "image": "https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=400&h=400&fit=crop", "weight_options": ["18g", "72.5g", "130g"], "default_weight": "72.5g", "base_price": 20, "mrp": 25, "unit": "per pack", "rating": 4.0},
    {"id": "p33", "name": "Haldiram Sev Bhujia", "category_id": "cat-3", "description": "Fine and crispy sev namkeen from Haldiram's. A traditional Rajasthani snack perfect with chai or as a topping.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmRLkNUDtO9VoTyrav_PXfrbyLbAVFxmhKFQ&sw=400&h=400&fit=crop", "weight_options": ["150g", "350g", "1 kg"], "default_weight": "350g", "base_price": 75, "mrp": 90, "unit": "per pack", "rating": 4.3},

    # ====== COLD DRINKS & JUICES (cat-4) ======
    {"id": "p34", "name": "Coca Cola", "category_id": "cat-4", "description": "The iconic Coca-Cola, served ice cold for maximum refreshment. Perfect for parties, meals, and celebrations.", "image": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400&h=400&fit=crop", "weight_options": ["250 ml", "500 ml", "750 ml", "1.25 L", "2 L"], "default_weight": "750 ml", "base_price": 38, "mrp": 42, "unit": "per bottle", "rating": 4.3},
    {"id": "p35", "name": "Sprite", "category_id": "cat-4", "description": "Clear, crisp, and refreshing lemon-lime soda. Sprite's clean taste quenches your thirst like no other.", "image": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400&h=400&fit=crop", "weight_options": ["250 ml", "500 ml", "750 ml", "2 L"], "default_weight": "750 ml", "base_price": 38, "mrp": 42, "unit": "per bottle", "rating": 4.2},
    {"id": "p36", "name": "Real Mango Juice", "category_id": "cat-4", "description": "100% pure mango juice by Real, made from Alphonso mangoes. No added preservatives, just pure mango goodness.", "image": "https://images.unsplash.com/photo-1546173159-315724a31696?w=400&h=400&fit=crop", "weight_options": ["200 ml", "1 L"], "default_weight": "1 L", "base_price": 99, "mrp": 120, "unit": "per pack", "rating": 4.4},
    {"id": "p37", "name": "Paper Boat Aam Panna", "category_id": "cat-4", "description": "Traditional aam panna drink by Paper Boat, a refreshing raw mango drink with cumin and mint. Nostalgia in every sip.", "image": "https://m.media-amazon.com/images/I/51LKJhz714L._SL1500_.jpg&fit=crop", "weight_options": ["200 ml", "500 ml"], "default_weight": "200 ml", "base_price": 30, "mrp": 40, "unit": "per pack", "rating": 4.5},
    {"id": "p38", "name": "Red Bull Energy Drink", "category_id": "cat-4", "description": "Red Bull gives you wings! Premium energy drink to boost your focus and energy levels. Perfect for workouts and late nights.", "image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=70,metadata=none,w=1080/da/cms-assets/cms/product/1a7eadf1-79fc-4352-b754-6ab13f2b15fa.png?bg_token=color.background.quaternary&fit=crop", "weight_options": ["250 ml", "355 ml", "473 ml"], "default_weight": "250 ml", "base_price": 115, "mrp": 125, "unit": "per can", "rating": 4.1},
    {"id": "p39", "name": "Tropicana Orange Juice", "category_id": "cat-4", "description": "100% pure orange juice by Tropicana, no added sugar. Start your morning right with a glass of fresh orange juice.", "image": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=400&h=400&fit=crop", "weight_options": ["200 ml", "1 L"], "default_weight": "1 L", "base_price": 95, "mrp": 110, "unit": "per pack", "rating": 4.3},
    {"id": "p40", "name": "Sting Energy Drink", "category_id": "cat-4", "description": "Sting energy drink with berry blast flavor. Affordable energy boost with great taste for active lifestyles.", "image": "https://www.bbassets.com/media/uploads/p/l/40113908_5-sting-energy-drink.jpg&fit=crop", "weight_options": ["250 ml"], "default_weight": "250 ml", "base_price": 20, "mrp": 22, "unit": "per can", "rating": 3.9},
    {"id": "p41", "name": "Frooti Mango Drink", "category_id": "cat-4", "description": "India's favorite mango drink! Sweet and refreshing Frooti, perfect for a quick thirst quencher on hot days.", "image": "https://www.bbassets.com/media/uploads/p/l/265783_7-frooti-drink-fresh-n-juicy-mango.jpgw=400&h=400&fit=crop", "weight_options": ["200 ml", "600 ml", "1.2 L"], "default_weight": "600 ml", "base_price": 25, "mrp": 30, "unit": "per pack", "rating": 4.0},

    # ====== INSTANT & FROZEN FOOD (cat-5) ======
    {"id": "p42", "name": "Maggi 2-Minute Noodles", "category_id": "cat-5", "description": "India's beloved instant noodles! Maggi Masala noodles ready in just 2 minutes. The ultimate comfort food.", "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=400&h=400&fit=crop", "weight_options": ["70g", "140g (2 pack)", "420g (6 pack)", "840g (12 pack)"], "default_weight": "420g (6 pack)", "base_price": 84, "mrp": 96, "unit": "per pack", "rating": 4.6},
    {"id": "p43", "name": "Yippee Noodles Magic Masala", "category_id": "cat-5", "description": "Round noodle blocks with magical masala flavor. Yippee noodles stay long and don't clump for a better eating experience.", "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop", "weight_options": ["70g", "140g", "420g (6 pack)"], "default_weight": "420g (6 pack)", "base_price": 78, "mrp": 90, "unit": "per pack", "rating": 4.3},
    {"id": "p44", "name": "McCain French Fries", "category_id": "cat-5", "description": "Premium frozen french fries by McCain, crispy on the outside and fluffy inside. Just fry or bake for restaurant-style fries.", "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=400&fit=crop", "weight_options": ["425g", "750g", "1.25 kg"], "default_weight": "425g", "base_price": 130, "mrp": 155, "unit": "per pack", "rating": 4.4},
    {"id": "p45", "name": "Frozen Green Peas", "category_id": "cat-5", "description": "IQF frozen green peas, picked at peak freshness. No preservatives, just pure peas for your favorite dishes.", "image": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=400&h=400&fit=crop", "weight_options": ["200g", "500g", "1 kg"], "default_weight": "500g", "base_price": 60, "mrp": 75, "unit": "per pack", "rating": 4.2},
    {"id": "p46", "name": "Frozen Sweet Corn", "category_id": "cat-5", "description": "Premium frozen sweet corn kernels, ready to cook. Perfect for soups, salads, pasta, and corn chaat.", "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=400&fit=crop", "weight_options": ["200g", "500g"], "default_weight": "500g", "base_price": 65, "mrp": 80, "unit": "per pack", "rating": 4.1},
    {"id": "p47", "name": "MTR Ready to Eat Poha", "category_id": "cat-5", "description": "Authentic MTR poha, ready to eat in just 3 minutes. Traditional Indori poha taste with minimal effort.", "image": "https://i5.walmartimages.com/seo/MTR-3-Minutes-Breakfast-Ready-to-Eat-Indian-Snack-Poha-Pouch-160g-Pack-of-6_37a991d1-2400-4f50-b597-c6c664babb6e.3ce27abb22f2c9f69f47300f25cd834b.jpeg&fit=crop", "weight_options": ["60g", "180g"], "default_weight": "180g", "base_price": 55, "mrp": 65, "unit": "per pack", "rating": 4.0},
    {"id": "p48", "name": "Top Ramen Curry Noodles", "category_id": "cat-5", "description": "Nissin Top Ramen with authentic curry flavor. Quick and tasty instant noodles for a satisfying meal.", "image": "https://tse2.mm.bing.net/th/id/OIP.Ie0O86g_0hjAWyDXzOOxjwHaHa?pid=Api&P=0&h=180&fit=crop", "weight_options": ["70g", "280g (4 pack)"], "default_weight": "280g (4 pack)", "base_price": 60, "mrp": 72, "unit": "per pack", "rating": 4.1},

    # ====== TEA, COFFEE & HEALTH DRINKS (cat-6) ======
    {"id": "p49", "name": "Tata Tea Gold", "category_id": "cat-6", "description": "Premium Tata Tea Gold, a blend of 15% long leaves for a rich, aromatic cup. India's most trusted tea brand.", "image": "https://m.media-amazon.com/images/I/5109sLDpkvL._SL1000_.jpg&fit=crop", "weight_options": ["100g", "250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 225, "mrp": 260, "unit": "per pack", "rating": 4.5},
    {"id": "p50", "name": "Nescafe Classic Coffee", "category_id": "cat-6", "description": "Nescafe Classic instant coffee, made from 100% pure coffee beans. Rich aroma and smooth taste for coffee lovers.", "image": "https://tse2.mm.bing.net/th/id/OIP.UcpKZLTNet97i0uaGeL3LAHaHa?pid=Api&P=0&h=180&fit=crop", "weight_options": ["50g", "100g", "200g"], "default_weight": "100g", "base_price": 210, "mrp": 245, "unit": "per jar", "rating": 4.6},
    {"id": "p51", "name": "Bru Instant Coffee", "category_id": "cat-6", "description": "Bru instant coffee with a unique blend of coffee and chicory. Smooth, mild, and perfect for South Indian filter coffee lovers.", "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=400&fit=crop", "weight_options": ["50g", "100g", "200g"], "default_weight": "100g", "base_price": 170, "mrp": 200, "unit": "per pack", "rating": 4.3},
    {"id": "p52", "name": "Organic Green Tea", "category_id": "cat-6", "description": "Premium organic green tea bags, rich in antioxidants. Helps boost metabolism and supports weight management.", "image": "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?w=400&h=400&fit=crop", "weight_options": ["25 bags", "50 bags", "100 bags"], "default_weight": "25 bags", "base_price": 120, "mrp": 150, "unit": "per box", "rating": 4.2},
    {"id": "p53", "name": "Horlicks Classic Malt", "category_id": "cat-6", "description": "Horlicks health drink with essential nutrients. Clinically proven to make kids taller, stronger, and sharper.", "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=400&fit=crop", "weight_options": ["200g", "500g", "1 kg"], "default_weight": "500g", "base_price": 230, "mrp": 270, "unit": "per jar", "rating": 4.3},
    {"id": "p54", "name": "Bournvita", "category_id": "cat-6", "description": "Cadbury Bournvita chocolate health drink. Packed with vitamins and minerals for growing children.", "image": "https://www.bbassets.com/media/uploads/p/l/281026_22-cadbury-dairy-milk-chocolate.jpg&h=180&fit=crop", "weight_options": ["200g", "500g", "1 kg"], "default_weight": "500g", "base_price": 215, "mrp": 250, "unit": "per jar", "rating": 4.4},

    # ====== BAKERY & BISCUITS (cat-7) ======
    {"id": "p55", "name": "Parle-G Biscuits", "category_id": "cat-7", "description": "India's iconic glucose biscuit! Parle-G has been the nation's favorite since 1939. Perfect with chai.", "image": "https://www.bbassets.com/media/uploads/p/l/102102_4-parle-gluco-biscuits-parle-g.jpgw=400&h=400&fit=crop", "weight_options": ["56.4g", "140g", "250g", "800g"], "default_weight": "250g", "base_price": 25, "mrp": 30, "unit": "per pack", "rating": 4.7},
    {"id": "p56", "name": "Oreo Chocolate Cream", "category_id": "cat-7", "description": "Twist, lick, dunk! Oreo chocolate sandwich cookies with vanilla cream filling. A global favorite.", "image": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=400&h=400&fit=crop", "weight_options": ["46.3g", "120g", "300g", "600g"], "default_weight": "300g", "base_price": 55, "mrp": 65, "unit": "per pack", "rating": 4.5},
    {"id": "p57", "name": "Sunfeast Dark Fantasy", "category_id": "cat-7", "description": "Luxurious dark chocolate-filled cookies by Sunfeast. Premium biscuits for those who love rich chocolate experiences.", "image": "https://www.bbassets.com/media/uploads/p/l/40235654_13-sunfeast-dark-fantasy-choco-fills-cookie-original-crunchy-creamy.jpgw=400&h=400&fit=crop", "weight_options": ["75g", "200g", "400g"], "default_weight": "200g", "base_price": 60, "mrp": 70, "unit": "per pack", "rating": 4.6},
    {"id": "p58", "name": "Monaco Salted Biscuits", "category_id": "cat-7", "description": "Crispy and salty Monaco biscuits, perfect for tea time. Great on their own or topped with cheese and veggies.", "image": "https://images.unsplash.com/photo-1590080876351-941da357be05?w=400&h=400&fit=crop", "weight_options": ["75.4g", "200g", "400g"], "default_weight": "200g", "base_price": 35, "mrp": 40, "unit": "per pack", "rating": 4.2},
    {"id": "p59", "name": "Britannia Marie Gold", "category_id": "cat-7", "description": "Light and crispy Marie biscuits by Britannia. Low in calories, perfect for health-conscious tea lovers.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvJCdSNzolGKHxDFbENdbEdi22MPUVivW4YA&sw=400&h=400&fit=crop", "weight_options": ["90g", "250g", "600g"], "default_weight": "250g", "base_price": 30, "mrp": 38, "unit": "per pack", "rating": 4.3},
    {"id": "p60", "name": "Fresh Chocolate Cake", "category_id": "cat-7", "description": "Freshly baked moist chocolate cake with rich ganache frosting. Made daily in our bakery with premium ingredients.", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=400&fit=crop", "weight_options": ["250g", "500g", "1 kg"], "default_weight": "500g", "base_price": 199, "mrp": 250, "unit": "per cake", "rating": 4.5},
    {"id": "p61", "name": "Britannia Good Day Butter", "category_id": "cat-7", "description": "Butter cookies with a delightful crunch by Britannia Good Day. Perfect for afternoon tea breaks.", "image": "https://tse4.mm.bing.net/th/id/OIP.shPHDs0Oy35DbUE0N4NA_QHaHa?pid=Api&P=0&h=180&fit=crop", "weight_options": ["75g", "200g", "400g"], "default_weight": "200g", "base_price": 35, "mrp": 42, "unit": "per pack", "rating": 4.1},

    # ====== SWEET TOOTH (cat-8) ======
    {"id": "p62", "name": "Cadbury Dairy Milk", "category_id": "cat-8", "description": "The iconic Cadbury Dairy Milk chocolate, made with a glass and a half of milk. Pure chocolate indulgence.", "image": "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=400&h=400&fit=crop", "weight_options": ["13g", "52g", "110g", "160g"], "default_weight": "110g", "base_price": 85, "mrp": 100, "unit": "per bar", "rating": 4.7},
    {"id": "p63", "name": "KitKat 4 Finger", "category_id": "cat-8", "description": "Have a break, have a KitKat! Crispy wafer fingers covered in smooth milk chocolate. A worldwide favorite.", "image": "https://images.unsplash.com/photo-1582176604856-e824b4736522?w=400&h=400&fit=crop", "weight_options": ["37.3g", "58g"], "default_weight": "37.3g", "base_price": 30, "mrp": 35, "unit": "per bar", "rating": 4.4},
    {"id": "p64", "name": "5 Star Chocolate", "category_id": "cat-8", "description": "Cadbury 5 Star with caramel and nougat center coated in milk chocolate. Chewy, gooey, and irresistible.", "image": "https://tse4.mm.bing.net/th/id/OIP.OV2H50pdrfQEGm841p5RygHaDh?pid=Api&P=0&h=180&fit=crop", "weight_options": ["22g", "40g"], "default_weight": "40g", "base_price": 20, "mrp": 25, "unit": "per bar", "rating": 4.2},
    {"id": "p65", "name": "Gulab Jamun Mix", "category_id": "cat-8", "description": "MTR Gulab Jamun instant mix, make perfect gulab jamuns at home in minutes. Soft, spongy, and soaked in sugar syrup.", "image": "https://images.unsplash.com/photo-1666190059743-9298d tried?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 70, "mrp": 85, "unit": "per pack", "rating": 4.3},
    {"id": "p66", "name": "Rasgulla - Haldiram", "category_id": "cat-8", "description": "Soft and spongy Haldiram's rasgulla in sugar syrup. A classic Bengali sweet loved across India.", "image": "https://images.unsplash.com/photo-1601303516-7488e1f72407?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg"], "default_weight": "500g", "base_price": 120, "mrp": 145, "unit": "per tin", "rating": 4.4},
    {"id": "p67", "name": "Ferrero Rocher", "category_id": "cat-8", "description": "Premium Ferrero Rocher chocolates with a whole hazelnut center, crispy wafer, and smooth chocolate coating.", "image": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=400&h=400&fit=crop", "weight_options": ["3 pcs", "8 pcs", "16 pcs", "24 pcs"], "default_weight": "16 pcs", "base_price": 449, "mrp": 525, "unit": "per box", "rating": 4.8},

    # ====== ATTA, RICE & DAL (cat-9) ======
    {"id": "p68", "name": "Aashirvaad Whole Wheat Atta", "category_id": "cat-9", "description": "India's No.1 atta brand! Aashirvaad whole wheat flour makes soft, fluffy rotis every time. 100% whole wheat.", "image": "https://tse4.mm.bing.net/th/id/OIP.l92OT1XcVi-seJvscC5rPQHaHa?pid=Api&P=0&h=180&fit=crop", "weight_options": ["1 kg", "2 kg", "5 kg", "10 kg"], "default_weight": "5 kg", "base_price": 245, "mrp": 280, "unit": "per pack", "rating": 4.6},
    {"id": "p69", "name": "India Gate Basmati Rice", "category_id": "cat-9", "description": "Premium India Gate Basmati rice, extra long grain. Fluffy and aromatic, perfect for biryani, pulao, and jeera rice.", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop", "weight_options": ["1 kg", "2 kg", "5 kg", "10 kg"], "default_weight": "5 kg", "base_price": 425, "mrp": 500, "unit": "per pack", "rating": 4.7},
    {"id": "p70", "name": "Toor Dal (Arhar)", "category_id": "cat-9", "description": "Premium quality toor dal, essential for everyday dal tadka. Clean, polished, and cooks quickly.", "image": "https://www.bbassets.com/media/uploads/p/l/10000425_16-bb-royal-toor-dalarhar-dal-desi.jpgw=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 140, "mrp": 165, "unit": "per pack", "rating": 4.3},
    {"id": "p71", "name": "Moong Dal (Yellow)", "category_id": "cat-9", "description": "Split yellow moong dal, light and easy to digest. Perfect for dal fry, khichdi, and moong dal halwa.", "image": "https://images.unsplash.com/photo-1613844237701-8f3664fc2eff?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 120, "mrp": 145, "unit": "per pack", "rating": 4.2},
    {"id": "p72", "name": "Chana Dal", "category_id": "cat-9", "description": "Premium quality chana dal (Bengal gram), great for dal, chana dal fry, and various Indian snacks.", "image": "https://images.unsplash.com/photo-1612257416648-ee7a6c6f68d4?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 95, "mrp": 115, "unit": "per pack", "rating": 4.1},
    {"id": "p73", "name": "Sona Masoori Rice", "category_id": "cat-9", "description": "Premium Sona Masoori rice, a medium-grain daily rice. Perfect for everyday meals, idli, and dosa.", "image": "https://cdn.shopify.com/s/files/1/0623/7395/3675/files/Sona_Masoori_rice_-_Slide_3_with_Meal.webp?v=1727949015&fit=crop", "weight_options": ["1 kg", "5 kg", "10 kg", "25 kg"], "default_weight": "5 kg", "base_price": 320, "mrp": 375, "unit": "per pack", "rating": 4.4},

    # ====== MASALA, OIL & MORE (cat-10) ======
    {"id": "p74", "name": "Fortune Sunflower Oil", "category_id": "cat-10", "description": "Fortune refined sunflower oil, light and healthy for everyday cooking. Rich in Vitamin E and low in saturated fats.", "image": "https://www.bbassets.com/media/uploads/p/l/40317533_1-fortune-sun-lite-refined-sunflower-oil.jpg&w=400&h=400&fit=crop", "weight_options": ["1 L", "2 L", "5 L"], "default_weight": "5 L", "base_price": 620, "mrp": 730, "unit": "per can", "rating": 4.4},
    {"id": "p75", "name": "MDH Garam Masala", "category_id": "cat-10", "description": "MDH Deggi Mirch & Garam Masala blend, essential for authentic Indian cooking. Aromatic and full of flavor.", "image": "https://www.bbassets.com/media/uploads/p/l/40019860_3-mdh-masala-garam.jpgw=400&h=400&fit=crop", "weight_options": ["50g", "100g", "500g"], "default_weight": "100g", "base_price": 65, "mrp": 78, "unit": "per pack", "rating": 4.5},
    {"id": "p76", "name": "Everest Kitchen King", "category_id": "cat-10", "description": "Everest Kitchen King masala, an all-purpose spice mix. One masala for all your curries, sabzis, and gravies.", "image": "https://images.unsplash.com/photo-1599909533879-0b5bfc3aab5d?w=400&h=400&fit=crop", "weight_options": ["50g", "100g", "200g"], "default_weight": "100g", "base_price": 55, "mrp": 66, "unit": "per pack", "rating": 4.3},
    {"id": "p77", "name": "Saffola Gold Oil", "category_id": "cat-10", "description": "Saffola Gold blended edible oil with natural antioxidants. Heart-healthy cooking oil for your family.", "image": "https://www.bbassets.com/media/uploads/p/l/40070789_6-saffola-gold-refined-cooking-oil-blended-rice-bran-sunflower-oil-helps-keeps-heart-healthy.jpg&fit=crop", "weight_options": ["1 L", "2 L", "5 L"], "default_weight": "5 L", "base_price": 735, "mrp": 860, "unit": "per can", "rating": 4.3},
    {"id": "p78", "name": "Turmeric Powder", "category_id": "cat-10", "description": "Pure and natural turmeric powder (haldi), essential for every Indian kitchen. Anti-inflammatory and adds golden color.", "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 45, "mrp": 55, "unit": "per pack", "rating": 4.2},
    {"id": "p79", "name": "Red Chilli Powder", "category_id": "cat-10", "description": "Premium Kashmiri red chilli powder, adds vibrant color and mild heat to dishes. Essential Indian spice.", "image": "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 55, "mrp": 68, "unit": "per pack", "rating": 4.1},
    {"id": "p80", "name": "Mustard Oil - Kachi Ghani", "category_id": "cat-10", "description": "Pure cold-pressed mustard oil (kachi ghani). Traditional cooking oil with a pungent aroma, ideal for pickles and frying.", "image": "http://cdn.shopify.com/s/files/1/0434/5475/9072/products/GO-102_1200x1200.jpg?v=1676566402&fit=crop", "weight_options": ["500 ml", "1 L", "5 L"], "default_weight": "1 L", "base_price": 165, "mrp": 190, "unit": "per bottle", "rating": 4.2},

    # ====== BABY CARE (cat-11) ======
    {"id": "p81", "name": "Pampers Diapers", "category_id": "cat-11", "description": "Pampers All Night diapers with up to 12 hours of dryness. Soft cotton-like material gentle on baby's skin.", "image": "https://www.bbassets.com/media/uploads/p/l/40351253_1-pampers-premium-care-diaper-pants-s-4-8-kg.jpg&fit=crop", "weight_options": ["S (32 pcs)", "M (28 pcs)", "L (24 pcs)", "XL (20 pcs)"], "default_weight": "M (28 pcs)", "base_price": 549, "mrp": 650, "unit": "per pack", "rating": 4.5},
    {"id": "p82", "name": "Himalaya Baby Wash", "category_id": "cat-11", "description": "Gentle Himalaya baby body wash with chickpea and green gram. Mild, tear-free formula for delicate baby skin.", "image": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop", "weight_options": ["100 ml", "200 ml", "400 ml"], "default_weight": "200 ml", "base_price": 135, "mrp": 155, "unit": "per bottle", "rating": 4.4},
    {"id": "p83", "name": "Cerelac Wheat", "category_id": "cat-11", "description": "Nestle Cerelac baby cereal with wheat and milk. Iron-fortified, easy to digest, suitable for babies 6 months and above.", "image": "https://sp.yimg.com/ib/th?id=OPAC.MjYMJKM0Vhac5g474C474&o=5&pid=21.1&w=160&h=105&fit=crop", "weight_options": ["300g", "500g"], "default_weight": "300g", "base_price": 225, "mrp": 260, "unit": "per box", "rating": 4.6},
    {"id": "p84", "name": "Johnson's Baby Oil", "category_id": "cat-11", "description": "Johnson's Baby Oil for gentle massage. Clinically proven mild formula that locks in moisture for soft, smooth baby skin.", "image": "https://www.bbassets.com/media/uploads/p/l/230067_8-johnsons-baby-baby-oil-with-vitamin-e.jpgw=400&h=400&fit=crop", "weight_options": ["100 ml", "200 ml", "500 ml"], "default_weight": "200 ml", "base_price": 145, "mrp": 170, "unit": "per bottle", "rating": 4.3},
    {"id": "p85", "name": "MamyPoko Pants", "category_id": "cat-11", "description": "MamyPoko Pants Style diapers with extra absorb system. Easy to wear like pants and keeps baby comfortable all day.", "image": "https://www.bbassets.com/media/uploads/p/l/40359031_2-mamypoko-all-night-absorb-disposable-baby-diaper-xxl.jpgw=400&h=400&fit=crop", "weight_options": ["S (36 pcs)", "M (32 pcs)", "L (28 pcs)", "XL (24 pcs)"], "default_weight": "L (28 pcs)", "base_price": 599, "mrp": 699, "unit": "per pack", "rating": 4.4},

    # ====== PERSONAL CARE (cat-12) ======
    {"id": "p86", "name": "Dove Cream Bar Soap", "category_id": "cat-12", "description": "Dove beauty cream bar with 1/4 moisturizing cream. Gentle cleansing that won't dry out your skin.", "image": "https://www.bbassets.com/media/uploads/p/l/40111422_1-dove-bathing-bar-soap-almond-cream-beauty.jpgw=400&h=400&fit=crop", "weight_options": ["75g", "100g (3 pack)", "125g (4 pack)"], "default_weight": "100g (3 pack)", "base_price": 145, "mrp": 170, "unit": "per pack", "rating": 4.5},
    {"id": "p87", "name": "Head & Shoulders Shampoo", "category_id": "cat-12", "description": "Head & Shoulders anti-dandruff shampoo for clean and flake-free hair. Clinically proven formula.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTebDQUn36fvUWwKjsM5KXVJKSNV3b8-bYZQQ&sw=400&h=400&fit=crop", "weight_options": ["72 ml", "180 ml", "340 ml", "650 ml"], "default_weight": "340 ml", "base_price": 265, "mrp": 310, "unit": "per bottle", "rating": 4.3},
    {"id": "p88", "name": "Colgate MaxFresh Toothpaste", "category_id": "cat-12", "description": "Colgate MaxFresh toothpaste with cooling crystals for intense freshness. Fights cavities and freshens breath.", "image": "https://www.bbassets.com/media/uploads/p/l/20005544_21-colgate-toothpaste-maxfresh-anti-cavity-peppermint-ice.jpgw=400&h=400&fit=crop", "weight_options": ["80g", "150g", "300g"], "default_weight": "150g", "base_price": 95, "mrp": 110, "unit": "per tube", "rating": 4.4},
    {"id": "p89", "name": "Dettol Handwash", "category_id": "cat-12", "description": "Dettol original antibacterial handwash. Kills 99.9% germs and keeps hands clean and protected.", "image": "https://sp.yimg.com/ib/th?id=OPAC.6K6Qolv2uhemFw474C474&o=5&pid=21.1&w=160&h=105&fit=crop", "weight_options": ["200 ml", "750 ml (refill)", "900 ml"], "default_weight": "200 ml", "base_price": 65, "mrp": 79, "unit": "per pump", "rating": 4.2},
    {"id": "p90", "name": "Nivea Body Lotion", "category_id": "cat-12", "description": "Nivea nourishing body lotion for 48-hour deep moisture. Enriched with almond oil for silky smooth skin.", "image": "'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQS_FHUZ5QnAvzIlCMVf8ainTNXRKbYeBwGTA&s&w=160&h=105&fit=crop", "weight_options": ["120 ml", "200 ml", "400 ml"], "default_weight": "200 ml", "base_price": 185, "mrp": 215, "unit": "per bottle", "rating": 4.3},
    {"id": "p91", "name": "Gillette Mach3 Razor", "category_id": "cat-12", "description": "Gillette Mach3 razor with 3-blade technology for a close, comfortable shave. Ergonomic handle for better control.", "image": "https://sp.yimg.com/ib/th?id=OPAC.RTJjlkB9LNE6jg474C474&o=5&pid=21.1&w=160&h=105&fit=crop", "weight_options": ["1 pc", "1 pc + 2 cartridges"], "default_weight": "1 pc", "base_price": 195, "mrp": 230, "unit": "per pack", "rating": 4.1},

    # ====== CLEANING ESSENTIALS (cat-13) ======
    {"id": "p92", "name": "Harpic Toilet Cleaner", "category_id": "cat-13", "description": "Harpic Power Plus toilet cleaner with 10x better stain removal. Kills 99.9% germs for a sparkling clean toilet.", "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400&h=400&fit=crop", "weight_options": ["500 ml", "1 L"], "default_weight": "500 ml", "base_price": 89, "mrp": 105, "unit": "per bottle", "rating": 4.3},
    {"id": "p93", "name": "Lizol Floor Cleaner", "category_id": "cat-13", "description": "Lizol disinfectant floor cleaner with citrus fragrance. Kills 99.9% germs and leaves floors shiny.", "image": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=400&h=400&fit=crop", "weight_options": ["500 ml", "975 ml", "2 L"], "default_weight": "975 ml", "base_price": 155, "mrp": 185, "unit": "per bottle", "rating": 4.2},
    {"id": "p94", "name": "Vim Dishwash Gel", "category_id": "cat-13", "description": "Vim dishwash gel with lemon freshness. Cuts through tough grease and leaves dishes sparkling clean.", "image": "https://www.bbassets.com/media/uploads/p/m/900459772_5-vim-dishwash-liquid-gel.jpg?w=400&h=400&fit=crop", "weight_options": ["250 ml", "500 ml", "750 ml"], "default_weight": "500 ml", "base_price": 95, "mrp": 115, "unit": "per bottle", "rating": 4.1},
    {"id": "p95", "name": "Surf Excel Matic", "category_id": "cat-13", "description": "Surf Excel Matic top load detergent powder. Designed for washing machines with superior stain removal.", "image": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg", "4 kg"], "default_weight": "2 kg", "base_price": 355, "mrp": 420, "unit": "per pack", "rating": 4.4},
    {"id": "p96", "name": "Comfort Fabric Conditioner", "category_id": "cat-13", "description": "Comfort After Wash fabric conditioner for soft and fragrant clothes. Keeps clothes fresh and easy to iron.", "image": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=400&h=400&fit=crop", "weight_options": ["220 ml", "860 ml", "1.6 L"], "default_weight": "860 ml", "base_price": 179, "mrp": 215, "unit": "per bottle", "rating": 4.2},
    {"id": "p97", "name": "Colin Glass Cleaner", "category_id": "cat-13", "description": "Colin glass and surface cleaner spray. Streak-free shine for glass, mirrors, and other surfaces.", "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=400&fit=crop", "weight_options": ["250 ml", "500 ml"], "default_weight": "500 ml", "base_price": 105, "mrp": 125, "unit": "per bottle", "rating": 4.0},

    # ====== BONUS PRODUCTS ======
    {"id": "p98", "name": "Amul Ghee", "category_id": "cat-2", "description": "Pure cow ghee by Amul, made from fresh cream. Rich aroma and taste, essential for Indian cooking and sweets.", "image": "https://tse1.mm.bing.net/th/id/OIP.pCKEOQtSyPb8u5VByDD-DQHaHa?pid=Api&P=0&h=180&fit=crop", "weight_options": ["200 ml", "500 ml", "1 L"], "default_weight": "500 ml", "base_price": 285, "mrp": 330, "unit": "per jar", "rating": 4.7},
    {"id": "p99", "name": "Peanut Butter - Creamy", "category_id": "cat-2", "description": "High-protein creamy peanut butter, made from roasted peanuts. No added sugar, perfect for toast and smoothies.", "image": "https://www.bbassets.com/media/uploads/p/l/40083093_7-sundrop-peanut-butter-creamy.jpgw=400&h=400&fit=crop", "weight_options": ["200g", "400g", "1 kg"], "default_weight": "400g", "base_price": 199, "mrp": 240, "unit": "per jar", "rating": 4.3},
    {"id": "p100", "name": "Lay's Magic Masala", "category_id": "cat-3", "description": "Lays potato chips with India's favorite Magic Masala flavor. Spicy, tangy, and absolutely irresistible.", "image": "https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=400&h=400&fit=crop", "weight_options": ["25g", "52g", "130g", "235g"], "default_weight": "130g", "base_price": 40, "mrp": 50, "unit": "per pack", "rating": 4.4},
    {"id": "p101", "name": "Pepsi", "category_id": "cat-4", "description": "Pepsi cola soft drink. Bold cola taste that complements any meal. Refreshing and energizing.", "image": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400&h=400&fit=crop", "weight_options": ["250 ml", "500 ml", "750 ml", "2 L"], "default_weight": "750 ml", "base_price": 38, "mrp": 42, "unit": "per bottle", "rating": 4.1},
    {"id": "p102", "name": "Rajma (Red Kidney Beans)", "category_id": "cat-9", "description": "Premium quality rajma, essential for the classic rajma chawal. Soaked and cooked to perfection for a hearty meal.", "image": "https://images.unsplash.com/photo-1612257416648-ee7a6c6f68d4?w=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 115, "mrp": 140, "unit": "per pack", "rating": 4.2},
    {"id": "p103", "name": "Coriander Powder", "category_id": "cat-10", "description": "Freshly ground coriander (dhania) powder. Aromatic spice that adds depth of flavor to curries and chutneys.", "image": "https://www.bbassets.com/media/uploads/p/l/40095123_11-tata-sampann-coriander-powder.jpg&w=400&h=400&fit=crop", "weight_options": ["100g", "200g", "500g"], "default_weight": "200g", "base_price": 50, "mrp": 62, "unit": "per pack", "rating": 4.1},
    {"id": "p104", "name": "Sugar", "category_id": "cat-9", "description": "Premium refined white sugar crystals. Essential pantry staple for tea, coffee, cooking, and baking.", "image": "https://www.bbassets.com/media/uploads/p/l/40214887_2-parrys-white-label-sugar.jpgw=400&h=400&fit=crop", "weight_options": ["500g", "1 kg", "2 kg", "5 kg"], "default_weight": "1 kg", "base_price": 42, "mrp": 50, "unit": "per pack", "rating": 4.0},
    {"id": "p105", "name": "Salt - Tata", "category_id": "cat-9", "description": "Tata Salt, desh ka namak! Iodized vacuum evaporated salt for healthy cooking. India's most trusted salt brand.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQl3NfL_mzKQJI_6IUv1Cl9xZBn8fuSQd9HkA&sw=400&h=400&fit=crop", "weight_options": ["1 kg", "2 kg"], "default_weight": "1 kg", "base_price": 22, "mrp": 28, "unit": "per pack", "rating": 4.5},
]

BANGALORE_STORES = [
    {
        "id": "store-1", "name": "Grovia Express - Koramangala",
        "address": "80 Feet Road, Koramangala 4th Block, Bangalore 560034",
        "lat": 12.9352, "lng": 77.6245, "rating": 4.7,
        "delivery_time": "10-15 min", "phone": "+91 80 4567 1234",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "7:00 AM - 11:00 PM"
    },
    {
        "id": "store-2", "name": "Grovia Fresh - Indiranagar",
        "address": "100 Feet Road, Indiranagar, Bangalore 560038",
        "lat": 12.9784, "lng": 77.6408, "rating": 4.8,
        "delivery_time": "8-12 min", "phone": "+91 80 4567 5678",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "6:00 AM - 11:30 PM"
    },
    {
        "id": "store-3", "name": "QuickBasket - HSR Layout",
        "address": "27th Main, HSR Layout Sector 1, Bangalore 560102",
        "lat": 12.9121, "lng": 77.6446, "rating": 4.5,
        "delivery_time": "12-18 min", "phone": "+91 80 4567 9012",
        "image": "https://images.unsplash.com/photo-1601599561213-832382fd07ba?w=400&h=300&fit=crop",
        "open_hours": "7:00 AM - 10:30 PM"
    },
    {
        "id": "store-4", "name": "FreshMart - Whitefield",
        "address": "ITPL Main Road, Whitefield, Bangalore 560066",
        "lat": 12.9698, "lng": 77.7500, "rating": 4.6,
        "delivery_time": "15-20 min", "phone": "+91 80 4567 3456",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "8:00 AM - 10:00 PM"
    },
    {
        "id": "store-5", "name": "GreenGrocer - BTM Layout",
        "address": "16th Main, BTM 2nd Stage, Bangalore 560076",
        "lat": 12.9165, "lng": 77.6101, "rating": 4.4,
        "delivery_time": "10-15 min", "phone": "+91 80 4567 7890",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "7:00 AM - 11:00 PM"
    },
    {
        "id": "store-6", "name": "SuperSave - Marathahalli",
        "address": "Outer Ring Road, Marathahalli, Bangalore 560037",
        "lat": 12.9591, "lng": 77.6974, "rating": 4.3,
        "delivery_time": "15-22 min", "phone": "+91 80 4567 2345",
        "image": "https://images.unsplash.com/photo-1601599561213-832382fd07ba?w=400&h=300&fit=crop",
        "open_hours": "8:00 AM - 10:00 PM"
    },
    {
        "id": "store-7", "name": "Daily Needs - JP Nagar",
        "address": "15th Cross, JP Nagar 6th Phase, Bangalore 560078",
        "lat": 12.8920, "lng": 77.5868, "rating": 4.5,
        "delivery_time": "12-18 min", "phone": "+91 80 4567 6789",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "6:30 AM - 10:30 PM"
    },
    {
        "id": "store-8", "name": "Farm Fresh - Electronic City",
        "address": "Phase 1, Electronic City, Bangalore 560100",
        "lat": 12.8440, "lng": 77.6593, "rating": 4.6,
        "delivery_time": "18-25 min", "phone": "+91 80 4567 0123",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "7:00 AM - 10:00 PM"
    },
]
# MUMBAI STORES
MUMBAI_STORES = [
    {
        "id": "store-mum-1", "name": "Reliance Smart - Andheri West",
        "address": "SV Road, Andheri West, Mumbai 400058",
        "lat": 19.1196, "lng": 72.8464, "rating": 4.3,
        "delivery_time": "15-20 min", "phone": "+91 22 1234 5678",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "8:00 AM - 10:00 PM"
    },
    {
        "id": "store-mum-2", "name": "D-Mart - Andheri East",
        "address": "Marol Maroshi Road, Andheri East, Mumbai 400059",
        "lat": 19.1120, "lng": 72.8650, "rating": 4.4,
        "delivery_time": "12-18 min", "phone": "+91 22 8765 4321",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "9:00 AM - 9:00 PM"
    },
    {
        "id": "store-mum-3", "name": "Star Bazaar - Andheri West",
        "address": "Lokhandwala Complex, Andheri West, Mumbai 400053",
        "lat": 19.1330, "lng": 72.8280, "rating": 4.2,
        "delivery_time": "10-15 min", "phone": "+91 22 3456 7890",
        "image": "https://images.unsplash.com/photo-1601599561213-832382fd07ba?w=400&h=300&fit=crop",
        "open_hours": "8:00 AM - 9:30 PM"
    },
    {
        "id": "store-mum-4", "name": "Nature's Basket - Andheri",
        "address": "Juhu Versova Link Road, Andheri West, Mumbai 400061",
        "lat": 19.1260, "lng": 72.8220, "rating": 4.5,
        "delivery_time": "10-12 min", "phone": "+91 22 4567 8901",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "9:00 AM - 10:00 PM"
    },
     {
        "id": "store-mum-5", "name": "Big Bazaar - Goregaon",
        "address": "Western Express Highway, Goregaon East, Mumbai 400063",
        "lat": 19.1620, "lng": 72.8520, "rating": 4.1,
        "delivery_time": "15-20 min", "phone": "+91 22 5678 9012",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "10:00 AM - 8:00 PM"
    },
    {
        "id": "store-mum-6", "name": "More Supermarket - Malad",
        "address": "Link Road, Malad West, Mumbai 400064",
        "lat": 19.1850, "lng": 72.8350, "rating": 4.0,
        "delivery_time": "12-18 min", "phone": "+91 22 6789 0123",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=300&fit=crop",
        "open_hours": "8:00 AM - 9:00 PM"
    },
     {
        "id": "store-mum-7", "name": "Spencer's - Juhu",
        "address": "Juhu Tara Road, Juhu, Mumbai 400049",
        "lat": 19.0990, "lng": 72.8250, "rating": 4.3,
        "delivery_time": "10-15 min", "phone": "+91 22 7890 1234",
        "image": "https://images.unsplash.com/photo-1591596788197-49d4c91c1c8d?w=400&h=300&fit=crop",
        "open_hours": "9:00 AM - 10:00 PM"
    },
    {
        "id": "store-mum-8", "name": "Apna Bazaar - Vile Parle",
        "address": "Station Road, Vile Parle West, Mumbai 400056",
        "lat": 19.1020, "lng": 72.8380, "rating": 4.2,
        "delivery_time": "8-12 min", "phone": "+91 22 8901 2345",
        "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop",
        "open_hours": "7:00 AM - 10:00 PM"
    }
]

# Combine all stores
STORES = BANGALORE_STORES + MUMBAI_STORES


# Store-Product pricing matrix - each store has different prices and availability
import random
random.seed(42)

STORE_PRODUCTS = {}
for store in STORES:
    store_id = store["id"]
    STORE_PRODUCTS[store_id] = {}
    for product in PRODUCTS:
        # Each store has ~85% of products
        if random.random() < 0.85:
            # Price varies by +/- 15% from base price
            price_variation = random.uniform(0.85, 1.15)
            price = round(product["base_price"] * price_variation)
            STORE_PRODUCTS[store_id][product["id"]] = {
                "price": price,
                "mrp": product["mrp"],
                "in_stock": random.random() < 0.9  # 90% chance in stock
            }

# Helper to get products with product data
def get_product_by_id(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None

def get_category_by_id(category_id):
    for c in CATEGORIES:
        if c["id"] == category_id:
            return c
    return None

def get_store_by_id(store_id):
    for s in STORES:
        if s["id"] == store_id:
            return s
    return None

def get_products_by_category(category_id):
    return [p for p in PRODUCTS if p["category_id"] == category_id]

def search_products(query):
    query = query.lower()
    return [p for p in PRODUCTS if query in p["name"].lower() or query in p["description"].lower()]

def get_store_products(store_id):
    store_prods = STORE_PRODUCTS.get(store_id, {})
    result = []
    for pid, pricing in store_prods.items():
        product = get_product_by_id(pid)
        if product and pricing["in_stock"]:
            result.append({**product, "store_price": pricing["price"], "store_mrp": pricing["mrp"]})
    return result

def get_product_store_availability(product_id):
    availability = []
    for store in STORES:
        store_prods = STORE_PRODUCTS.get(store["id"], {})
        if product_id in store_prods:
            pricing = store_prods[product_id]
            availability.append({
                "store_id": store["id"],
                "store_name": store["name"],
                "store_address": store["address"],
                "price": pricing["price"],
                "mrp": pricing["mrp"],
                "in_stock": pricing["in_stock"],
                "delivery_time": store["delivery_time"],
                "lat": store["lat"],
                "lng": store["lng"]
            })
    return availability
