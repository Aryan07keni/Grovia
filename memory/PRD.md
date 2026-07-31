# Grovia - Premium Grocery Web Application

## Original Problem Statement
Build a modern, minimal, premium grocery web app called "Grovia" inspired by Zepto/Blinkit with glassmorphism theme, Google Auth, Google Maps for store detection, ML recommendations, and Razorpay payments. React.js frontend with separate CSS files (no TypeScript, no Tailwind), FastAPI backend.

## Architecture
- **Frontend**: React.js (CRA) with separate CSS files, glassmorphism theme
- **Backend**: FastAPI (Python) with in-memory data storage
- **Database**: Supabase keys configured (tables need manual creation for persistence)
- **Auth**: Google OAuth + Phone OTP (demo mode)
- **Maps**: Google Maps JavaScript API
- **Icons**: Lucide-react

## User Personas
1. **Grocery Shopper**: Browses products, adds to cart, checks out
2. **Price-Conscious Buyer**: Compares prices across stores
3. **Quick Delivery Seeker**: Selects nearest store for fast delivery

## Core Requirements
- Login with Google OAuth and Phone OTP
- Browse 105+ products across 13 categories
- 8 stores with location-based selection
- Multi-store price comparison per product
- Cart with quantity controls and price breakdown
- Payment page with UPI, Card, COD options
- Profile with orders, addresses, wishlist, help

## What's Been Implemented (April 1, 2026)
- Full backend API (32 endpoints) with 105 products, 13 categories, 8 stores
- Login page with glassmorphism + floating grocery animations
- Explore page with category browsing, product grid, recommendations
- Store selection with Google Maps integration
- Product detail with multi-store pricing and availability
- Cart with quantity controls, price breakdown
- Payment page with UPI/Card/COD + order success state
- Profile with orders, addresses, wishlist, fav stores, help, refunds
- Category page for filtered browsing
- Responsive design with hover effects and transitions

## Prioritized Backlog
### P0 (Critical)
- Supabase table creation for data persistence
- Razorpay payment integration (user deferred)

### P1 (Important)
- ML collaborative filtering recommendations (scikit-learn)
- Real SMS OTP verification (Twilio/similar)
- Order tracking and delivery status

### P2 (Nice to Have)
- Push notifications
- Coupon/discount system
- Admin dashboard
- Real product images from CDN
