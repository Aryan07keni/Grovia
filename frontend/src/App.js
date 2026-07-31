import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AppProvider, useApp } from './context/AppContext';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Navbar from './components/Navbar/Navbar';
import Login from './pages/Login/Login';
import Explore from './pages/Explore/Explore';
import Cart from './pages/Cart/Cart';
import Payment from './pages/Payment/Payment';
import Profile from './pages/Profile/Profile';
import Category from './pages/Category/Category';
import ProductDetail from './pages/ProductDetail/ProductDetail';
import StoreSelection from './pages/StoreSelection/StoreSelection';
import CartBar from './components/CartBar/CartBar';
import './App.css';

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '52752986857-qbja4qfmto0ppscgjoloutejfiggeb7l.apps.googleusercontent.com';

function AppContent() {
  const { user } = useApp();
  const location = useLocation();
  
  // Hide navbar on login page
  const hideNavbar = location.pathname === '/login';
  const showCartBar = !['/login', '/cart', '/payment'].includes(location.pathname);

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Explore />} />
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/category/:categoryId" element={<Category />} />
        <Route path="/product/:productId" element={<ProductDetail />} />
        <Route path="/stores" element={<StoreSelection />} />
      </Routes>
      {showCartBar && <CartBar />}
    </>
  );
}

function App() {
  const content = (
    <AppProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AppProvider>
  );

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      {content}
    </GoogleOAuthProvider>
  );
}

export default App;