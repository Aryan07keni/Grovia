# Grovia Deployment Guide

This guide provides complete step-by-step instructions for deploying the **Grovia** application online.

---

## 1. Backend Deployment (Render / Railway)

### Option A: Render (Recommended)

1. Sign in to [Render](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your Git Repository containing the `GROVIA-MAIN` project.
4. Configure the service settings:
   - **Name**: `grovia-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add the following **Environment Variables** under *Advanced*:
   - `PYTHON_VERSION`: `3.11.0`
   - `JWT_SECRET`: `grovia_jwt_secret_key_2024_secure` (or a custom random string)
   - `CORS_ORIGINS`: `*` (or your frontend URL e.g., `https://grovia-frontend.vercel.app`)
   - `RAZORPAY_KEY_ID`: `rzp_test_SYLM4DZwgsL1Ed` (or your live Razorpay key)
   - `RAZORPAY_KEY_SECRET`: `Xmkv7qQRPzC7eLb9a0m3XAxa` (or your live Razorpay secret)
   - `GOOGLE_MAPS_API_KEY`: `AIzaSyCqArq4Yo9E0dnt52m-m9fXia7IkdSCG6M`
6. Click **Create Web Service**. Note your backend URL (e.g. `https://grovia-backend.onrender.com`).

---

## 2. Frontend Deployment (Vercel)

### Option A: Vercel Dashboard (Recommended)

1. Sign in to [Vercel](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your Git Repository.
4. Configure the deployment:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: Click `Edit` and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install --legacy-peer-deps`
5. Expand **Environment Variables** and add:
   - `REACT_APP_BACKEND_URL`: `https://grovia-backend.onrender.com` *(Replace with your Render backend URL)*
   - `REACT_APP_GOOGLE_CLIENT_ID`: `52752986857-qbja4qfmto0ppscgjoloutejfiggeb7l.apps.googleusercontent.com`
   - `REACT_APP_GOOGLE_MAPS_API_KEY`: `AIzaSyCqArq4Yo9E0dnt52m-m9fXia7IkdSCG6M`
   - `REACT_APP_RAZORPAY_KEY_ID`: `rzp_test_SYLM4DZwgsL1Ed`
6. Click **Deploy**.

---

## 3. Local Production Preview

To test the production build locally:

```bash
# Frontend production build
cd frontend
npm run build
npx serve -s build -l 3000

# Backend server
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000
```
