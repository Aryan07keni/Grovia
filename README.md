# Grovia 🛒 - Ultra-Fast Grocery E-Commerce Platform

Grovia is a modern, high-performance, full-stack grocery delivery platform featuring a glassmorphism UI aesthetic, store-based location discovery, dynamic inventory pricing, machine learning recommendations, and seamless checkout via Razorpay and Cash on Delivery.

---

## ✨ Features

- 🏪 **Multi-Store Discovery**: Locate nearby grocery stores using real-time distance calculations and interactive map discovery.
- ⚡ **Lightning Fast Delivery**: Browse products tailored to your selected store's stock and store-specific pricing.
- 🎯 **ML Recommendations**: Machine learning recommendation engine providing personalized product suggestions.
- 🛒 **Interactive Cart & Floating Cart Bar**: Instant quantity adjustments on product cards and a global floating cart bar.
- 💳 **Dual Checkout Options**: Seamless online payment processing via **Razorpay** and **Cash / Pay on Delivery (COD)** fallback.
- 👤 **User Profiles & Order Tracking**: Address book management, order history tracking, and wishlist saving.
- 🎨 **Glassmorphism Aesthetic**: Modern UI designed with sleek gradients, micro-animations, and responsive layout.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 (Create React App / CRACO)
- **Routing**: React Router v6
- **Icons**: Lucide React
- **Styling**: Vanilla CSS with Design System Tokens & Glassmorphism
- **Authentication**: JWT & Google OAuth Provider

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Authentication**: JOSE JWT Tokens & Google OAuth Token Verification
- **Payments**: Razorpay Integration SDK
- **Machine Learning**: Hybrid Scikit-Learn Recommender Model

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.11+
- Node.js 18+

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## ☁️ Deployment

For online production hosting:
- **Frontend**: Deploy `frontend/` to **[Vercel](https://vercel.com)**
- **Backend**: Deploy `backend/` to **[Render](https://render.com)**

Refer to [DEPLOYMENT.md](DEPLOYMENT.md) for full step-by-step cloud deployment instructions.
