import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyC1p3owqbWfpi-eJnouOeW0a2BGUPLgqKY",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "grovia-app-dbf8d.firebaseapp.com",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "grovia-app-dbf8d",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "grovia-app-dbf8d.firebasestorage.app",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "554048067555",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "1:554048067555:web:f1487e46e74873b46e72d6",
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID || "G-VGG10V9DVD"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
