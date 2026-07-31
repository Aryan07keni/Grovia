import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useApp } from '../../context/AppContext';
import { ArrowLeft, Star, ShoppingCart, Clock, MapPin, Heart, TrendingUp, Apple, Shield, Truck, Info } from 'lucide-react';
import axios from 'axios';
import './ProductDetail.css';

function ProductDetail() {
  const { productId } = useParams();
  const { API, selectedStore, addToCart, cart, user } = useApp();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedWeight, setSelectedWeight] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [adding, setAdding] = useState(false);
  const [activeTab, setActiveTab] = useState('description');
  const [wishlist, setWishlist] = useState(false);

  useEffect(() => {
    if (productId) {
      fetchProduct();
    } else {
      navigate('/');
    }
  }, [productId]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API}/products/${productId}`);
      setProduct(res.data);
      
      if (res.data.weight_options && res.data.weight_options.length > 0) {
        setSelectedWeight(res.data.weight_options[0]);
      }
    } catch (e) {
      console.error('Failed to fetch product:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (!selectedStore) {
      alert('Please select a store first');
      return;
    }
    
    setAdding(true);
    const success = await addToCart(product.id, selectedStore.id, quantity, selectedWeight);
    if (success) {
      alert('Added to cart!');
    }
    setAdding(false);
  };

  const toggleWishlist = () => {
    setWishlist(!wishlist);
  };

  if (loading) {
    return (
      <div className="product-detail-page">
        <div className="loading-skeleton"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-detail-page">
        <div className="error-container">
          <h2>Product not found</h2>
          <button className="detail-add-btn" onClick={() => navigate('/')}>Go Home</button>
        </div>
      </div>
    );
  }

  const currentPrice = product.store_availability?.find(s => s.store_id === selectedStore?.id)?.price || product.base_price;
  const discount = product.mrp > currentPrice 
    ? Math.round(((product.mrp - currentPrice) / product.mrp) * 100) 
    : 0;

  return (
    <div className="product-detail-page">
      <div className="product-detail-layout">
        {/* Image Section */}
        <div className="product-detail-image-section">
          <div className="product-detail-image">
            <img src={product.image} alt={product.name} />
            {discount > 0 && (
              <span className="detail-discount-badge">{discount}% OFF</span>
            )}
            <button 
              className={`wishlist-btn ${wishlist ? 'active' : ''}`}
              onClick={toggleWishlist}
            >
              <Heart size={20} fill={wishlist ? '#ef4444' : 'none'} stroke={wishlist ? '#ef4444' : 'currentColor'} />
            </button>
          </div>
        </div>

        {/* Info Section */}
        <div className="product-detail-info">
          <span className="product-detail-category">
            {product.category?.name || 'Premium Product'}
          </span>
          
          <h1 className="product-detail-name">{product.name}</h1>
          
          <div className="product-detail-rating">
            <Star size={16} fill="#ff9800" stroke="#ff9800" />
            <span>{product.rating || 4.5}</span>
            <span style={{ color: '#999' }}>(4.5k+ ratings)</span>
          </div>
          
          <div className="product-detail-price-block">
            <span className="detail-price">Rs. {currentPrice}</span>
            {product.mrp > currentPrice && (
              <>
                <span className="detail-mrp">Rs. {product.mrp}</span>
                <span className="detail-save">Save Rs. {product.mrp - currentPrice}</span>
              </>
            )}
          </div>
          
          <p className="product-detail-desc">
            {product.description || 'This premium product is sourced from the finest quality ingredients to ensure freshness and taste. Perfect for everyday use and special occasions.'}
          </p>

          {/* Weight Options */}
          {product.weight_options && product.weight_options.length > 0 && (
            <div className="product-detail-weights">
              <h3>Select Weight</h3>
              <div className="weight-options">
                {product.weight_options.map(weight => (
                  <button
                    key={weight}
                    className={`weight-option ${selectedWeight === weight ? 'active' : ''}`}
                    onClick={() => setSelectedWeight(weight)}
                  >
                    {weight}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Quantity Selector */}
          <div className="product-detail-qty">
            <h3>Quantity</h3>
            <div className="qty-selector">
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                disabled={quantity <= 1}
              >
                -
              </button>
              <span>{quantity}</span>
              <button onClick={() => setQuantity(quantity + 1)}>
                +
              </button>
            </div>
          </div>

          {/* Add to Cart Button */}
          <button 
            className="detail-add-btn btn-primary"
            onClick={handleAddToCart}
            disabled={adding || !selectedStore}
          >
            <ShoppingCart size={20} />
            {adding ? 'Adding...' : `Add to Cart - Rs. ${currentPrice * quantity}`}
          </button>

          {/* Store Availability */}
          <div className="store-availability">
            <h3>
              <MapPin size={18} />
              Available at
            </h3>
            <div className="store-avail-list">
              {product.store_availability?.slice(0, 3).map(store => (
                <div key={store.store_id} className="store-avail-card glass-card">
                  <div>
                    <div className="store-avail-name">{store.store_name}</div>
                    <div className="store-avail-meta">
                      <span><Clock size={12} /> {store.delivery_time}</span>
                      <span><Truck size={12} /> Free delivery</span>
                    </div>
                  </div>
                  <div className="store-avail-price">
                    <span className="store-avail-price-val">Rs. {store.price}</span>
                    {store.mrp > store.price && (
                      <span className="store-avail-mrp">Rs. {store.mrp}</span>
                    )}
                    <span className="store-avail-stock">
                      {store.in_stock ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Tabs Section */}
      <div className="related-section">
        <div className="description-tabs" style={{ display: 'flex', gap: '16px', borderBottom: '1px solid #e0e0e0', marginBottom: '24px' }}>
          <button 
            className={`tab-btn ${activeTab === 'description' ? 'active' : ''}`}
            onClick={() => setActiveTab('description')}
            style={{ padding: '12px 24px', background: 'none', border: 'none', fontWeight: '600', cursor: 'pointer', color: activeTab === 'description' ? '#2e7d32' : '#666', borderBottom: activeTab === 'description' ? '2px solid #2e7d32' : 'none' }}
          >
            Description
          </button>
          <button 
            className={`tab-btn ${activeTab === 'nutrition' ? 'active' : ''}`}
            onClick={() => setActiveTab('nutrition')}
            style={{ padding: '12px 24px', background: 'none', border: 'none', fontWeight: '600', cursor: 'pointer', color: activeTab === 'nutrition' ? '#2e7d32' : '#666', borderBottom: activeTab === 'nutrition' ? '2px solid #2e7d32' : 'none' }}
          >
            Nutrition & Benefits
          </button>
          <button 
            className={`tab-btn ${activeTab === 'comparison' ? 'active' : ''}`}
            onClick={() => setActiveTab('comparison')}
            style={{ padding: '12px 24px', background: 'none', border: 'none', fontWeight: '600', cursor: 'pointer', color: activeTab === 'comparison' ? '#2e7d32' : '#666', borderBottom: activeTab === 'comparison' ? '2px solid #2e7d32' : 'none' }}
          >
            Price Comparison
          </button>
        </div>

        {activeTab === 'description' && (
          <div className="description-content">
            <h3>About this product</h3>
            <p>{product.description || 'This premium product is sourced from the finest quality ingredients to ensure freshness and taste. Perfect for everyday use and special occasions.'}</p>
            
            <h3 style={{ marginTop: '24px' }}>Key Features</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Premium quality ingredients</li>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Freshly sourced</li>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ No artificial preservatives</li>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Best value for money</li>
            </ul>
          </div>
        )}

        {activeTab === 'nutrition' && (
          <div className="nutrition-content">
            <h3><Apple size={20} style={{ marginRight: '8px' }} /> Nutritional Information</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px', margin: '24px 0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Energy</span><strong>250 kcal</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Protein</span><strong>5g</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Carbohydrates</span><strong>30g</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Fat</span><strong>12g</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Fiber</span><strong>3g</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f5f5f5', borderRadius: '12px' }}>
                <span>Sugar</span><strong>8g</strong>
              </div>
            </div>
            
            <h3><Shield size={18} style={{ marginRight: '8px' }} /> Health Benefits</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Rich in essential vitamins and minerals</li>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Supports digestive health</li>
              <li style={{ padding: '8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>✓ Boosts immune system</li>
            </ul>
          </div>
        )}

        {activeTab === 'comparison' && (
          <div className="price-comparison">
            <h3><TrendingUp size={20} style={{ marginRight: '8px' }} /> Price Comparison Across Stores</h3>
            <div style={{ background: '#f5f5f5', borderRadius: '16px', overflow: 'hidden', margin: '16px 0' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '16px', padding: '16px', background: '#e0e0e0', fontWeight: '700' }}>
                <span>Store</span>
                <span>Price</span>
                <span>Delivery</span>
                <span>Savings</span>
              </div>
              {product.store_availability?.map(store => (
                <div key={store.store_id} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '16px', padding: '16px', borderBottom: '1px solid #e0e0e0' }}>
                  <span>{store.store_name}</span>
                  <span style={{ fontWeight: '700', color: '#2e7d32' }}>Rs. {store.price}</span>
                  <span style={{ fontSize: '0.85rem', color: '#666' }}>{store.delivery_time}</span>
                  <span style={{ background: '#e8f5e9', color: '#2e7d32', padding: '4px 8px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: '600', textAlign: 'center', display: 'inline-block', width: 'fit-content' }}>
                    Save Rs. {store.mrp - store.price}
                  </span>
                </div>
              ))}
            </div>
            <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '16px' }}>
              <Info size={14} style={{ marginRight: '4px' }} />
              Prices may vary across stores. Select your preferred store for the best deal.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductDetail;