import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const AppContext = createContext();
const rawBackend = process.env.REACT_APP_BACKEND_URL || 'https://grovia-yyxm.onrender.com';
const BACKEND = rawBackend.endsWith('/api') ? rawBackend.slice(0, -4) : rawBackend;
const API = `${BACKEND.replace(/\/$/, '')}/api`;

export function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState({ items: [], subtotal: 0, delivery_fee: 0, total: 0, item_count: 0 });
  const [selectedStore, setSelectedStore] = useState(null);
  const [deliveryLocation, setDeliveryLocation] = useState(() => {
    const saved = localStorage.getItem('grovia_delivery');
    return saved ? JSON.parse(saved) : null;
  });
  const [categories, setCategories] = useState([]);
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(false);

  const getAuthHeaders = useCallback(() => {
    const token = localStorage.getItem('grovia_token');
    console.log('Getting auth headers, token exists:', !!token);
    return token ? { Authorization: `Bearer ${token}` } : {};
  }, []);

  // Handler for setting selected store with localStorage persistence
  const handleSetSelectedStore = (store) => {
    setSelectedStore(store);
    if (store) {
      localStorage.setItem('grovia_selected_store', JSON.stringify(store));
    } else {
      localStorage.removeItem('grovia_selected_store');
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('grovia_token');
    const userData = localStorage.getItem('grovia_user');
    console.log('Initial load - token exists:', !!token, 'userData exists:', !!userData);
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
        fetchCart(token);
      } catch (e) {
        console.error('Error loading user data:', e);
        localStorage.removeItem('grovia_token');
        localStorage.removeItem('grovia_user');
      }
    }
    fetchCategories();
    fetchStores();
  }, []);

  // Load saved store from localStorage when stores are loaded
  useEffect(() => {
    const savedStore = localStorage.getItem('grovia_selected_store');
    if (savedStore && stores.length > 0) {
      try {
        const parsedStore = JSON.parse(savedStore);
        const storeExists = stores.find(s => s.id === parsedStore.id);
        if (storeExists) {
          setSelectedStore(parsedStore);
        } else if (stores.length > 0) {
          handleSetSelectedStore(stores[0]);
        }
      } catch (e) {
        console.error('Failed to load saved store:', e);
        if (stores.length > 0) {
          handleSetSelectedStore(stores[0]);
        }
      }
    } else if (stores.length > 0 && !selectedStore) {
      handleSetSelectedStore(stores[0]);
    }
  }, [stores]);

  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API}/categories`);
      setCategories(res.data.categories);
    } catch (e) { 
      console.error('Failed to fetch categories:', e); 
    }
  };

  const fetchStores = async () => {
    try {
      const res = await axios.get(`${API}/stores`);
      setStores(res.data.stores);
    } catch (e) { 
      console.error('Failed to fetch stores:', e); 
    }
  };

  const fetchCart = async (token) => {
    try {
      const authToken = token || localStorage.getItem('grovia_token');
      if (!authToken) {
        console.log('No token available, skipping cart fetch');
        return;
      }
      
      const res = await axios.get(`${API}/cart`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setCart(res.data);
    } catch (e) { 
      console.error('Failed to fetch cart:', e.response?.status, e.response?.data);
      // If 401, clear invalid token
      if (e.response?.status === 401) {
        localStorage.removeItem('grovia_token');
        localStorage.removeItem('grovia_user');
        setUser(null);
      }
    }
  };

  const login = (userData) => {
    console.log('Login successful, setting user and token');
    setUser(userData);
    localStorage.setItem('grovia_token', userData.token);
    localStorage.setItem('grovia_user', JSON.stringify(userData));
    fetchCart(userData.token);
  };

  const logout = () => {
    console.log('Logging out');
    setUser(null);
    setCart({ items: [], subtotal: 0, delivery_fee: 0, total: 0, item_count: 0 });
    localStorage.removeItem('grovia_token');
    localStorage.removeItem('grovia_user');
  };

  const addToCart = async (productId, storeId, quantity, weightOption) => {
    try {
      const token = localStorage.getItem('grovia_token');
      console.log('addToCart called - token exists:', !!token);
      
      if (!token) {
        console.error('No token found. User not logged in.');
        alert('Please login to add items to cart');
        return false;
      }
      
      const store_id = storeId || (selectedStore ? selectedStore.id : 'store-1');
      console.log('Adding to cart:', { productId, store_id, quantity, weightOption });
      
      const res = await axios.post(`${API}/cart`, {
        product_id: productId,
        store_id: store_id,
        quantity,
        weight_option: weightOption
      }, { 
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        } 
      });
      
      console.log('Cart updated successfully:', res.data);
      setCart(res.data);
      return true;
    } catch (e) {
      console.error('Add to cart failed:', e.response?.status, e.response?.data || e.message);
      
      // Handle specific error cases
      if (e.response?.status === 401) {
        console.log('Token expired or invalid');
        alert('Session expired. Please login again.');
        localStorage.removeItem('grovia_token');
        localStorage.removeItem('grovia_user');
        setUser(null);
        window.location.href = '/login';
      } else if (e.response?.status === 404) {
        alert('Product or store not found. Please refresh and try again.');
      } else if (e.response?.status === 400) {
        alert(e.response?.data?.detail || 'Invalid request. Please try again.');
      } else {
        alert('Failed to add to cart. Please try again.');
      }
      
      return false;
    }
  };

  const updateCartItem = async (itemId, quantity) => {
    try {
      const token = localStorage.getItem('grovia_token');
      if (!token) return;
      
      const res = await axios.put(`${API}/cart/${itemId}`, { quantity }, { 
        headers: { Authorization: `Bearer ${token}` } 
      });
      setCart(res.data);
    } catch (e) { 
      console.error('Update cart failed:', e); 
    }
  };

  const removeCartItem = async (itemId) => {
    try {
      const token = localStorage.getItem('grovia_token');
      if (!token) return;
      
      const res = await axios.delete(`${API}/cart/${itemId}`, { 
        headers: { Authorization: `Bearer ${token}` } 
      });
      setCart(res.data);
    } catch (e) { 
      console.error('Remove from cart failed:', e); 
    }
  };

  const value = {
    user,
    cart,
    selectedStore,
    categories,
    stores,
    loading,
    API,
    login,
    logout,
    addToCart,
    updateCartItem,
    removeCartItem,
    setSelectedStore: handleSetSelectedStore,
    setDeliveryLocation,
    fetchCart,
    getAuthHeaders,
    setLoading,
    fetchStores
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
}