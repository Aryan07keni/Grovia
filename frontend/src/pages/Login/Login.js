import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '52752986857-qbja4qfmto0ppscgjoloutejfiggeb7l.apps.googleusercontent.com';
import { useApp } from '../../context/AppContext';
import { Phone, ArrowRight, ShieldCheck } from 'lucide-react';
import FloatingGroceries from '../../components/FloatingGroceries/FloatingGroceries';
import axios from 'axios';
import './Login.css';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

function Login() {
  const { login, user } = useApp();
  const navigate = useNavigate();
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [timer, setTimer] = useState(30);

  useEffect(() => {
    let interval;
    if (otpSent && timer > 0) {
      interval = setInterval(() => setTimer(t => t - 1), 1000);
    }
    return () => clearInterval(interval);
  }, [otpSent, timer]);

  if (user) { navigate('/'); return null; }

  const handleGoogleSuccess = async (credentialResponse) => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.post(`${API}/auth/google`, { credential: credentialResponse.credential });
      login(res.data);
      navigate('/');
    } catch (e) {
      setError('Google login failed. Please try again.');
    }
    setLoading(false);
  };

  const handleSendOtp = async () => {
    if (phone.length < 10) { setError('Enter a valid 10-digit phone number'); return; }
    setLoading(true);
    setError('');
    try {
      await axios.post(`${API}/auth/phone`, { phone: `+91${phone}` });
      setOtpSent(true);
      setTimer(30);
      setOtp('');
    } catch (e) {
      setError('Failed to send OTP');
    }
    setLoading(false);
  };

  const handleVerifyOtp = async () => {
    if (otp.length < 4) { setError('Enter the 6-digit OTP sent to your phone'); return; }
    setLoading(true);
    setError('');
    try {
      const res = await axios.post(`${API}/auth/phone`, { phone: `+91${phone}`, otp });
      login(res.data);
      navigate('/');
    } catch (e) {
      setError(e.response?.data?.detail || 'Invalid or expired OTP');
    }
    setLoading(false);
  };

  return (
    <div className="login-page" data-testid="login-page">
      <div className="login-bg">
        <img src="https://images.unsplash.com/photo-1542838132-92c53300491e?w=1920&h=1080&fit=crop" alt="" className="login-bg-img" />
        <div className="login-bg-overlay" />
      </div>
      <FloatingGroceries />
      <div className="login-container">
        <div className="login-card glass-card" data-testid="login-card">
          <div className="login-header">
            <h1 className="login-logo">Grovia</h1>
            <p className="login-subtitle">Fresh groceries, delivered fast</p>
          </div>

          {error && <div className="login-error" data-testid="login-error">{error}</div>}

          <div className="login-form">
            {!otpSent ? (
              <>
                <div className="input-group">
                  <div className="input-prefix">
                    <Phone size={18} />
                    <span>+91</span>
                  </div>
                  <input type="tel" placeholder="Enter phone number" value={phone} maxLength={10}
                    onChange={(e) => setPhone(e.target.value.replace(/\D/g, ''))}
                    data-testid="phone-input" />
                </div>
                <button className="login-btn btn-primary" onClick={handleSendOtp} disabled={loading} data-testid="send-otp-btn">
                  {loading ? 'Sending...' : 'Send OTP'} {!loading && <ArrowRight size={18} />}
                </button>
              </>
            ) : (
              <>
                <div className="otp-info">
                  <ShieldCheck size={20} className="otp-icon" />
                  <span>6-digit OTP sent via SMS to +91 {phone}</span>
                </div>
                <div className="otp-inputs" data-testid="otp-inputs">
                  {[0, 1, 2, 3, 4, 5].map((i) => (
                    <input key={i} type="text" maxLength={1} className="otp-digit"
                      value={otp[i] || ''}
                      onKeyDown={(e) => {
                        if (e.key === 'Backspace' && !otp[i] && e.target.previousSibling) {
                          e.target.previousSibling.focus();
                        }
                      }}
                      onChange={(e) => {
                        const val = e.target.value.replace(/\D/g, '');
                        const newOtpArr = otp.split('');
                        newOtpArr[i] = val;
                        const newOtp = newOtpArr.join('');
                        setOtp(newOtp);
                        if (val && e.target.nextSibling) e.target.nextSibling.focus();
                      }}
                      data-testid={`otp-digit-${i}`} />
                  ))}
                </div>
                <button className="login-btn btn-primary" onClick={handleVerifyOtp} disabled={loading} data-testid="verify-otp-btn">
                  {loading ? 'Verifying...' : 'Verify & Login'}
                </button>
                <div className="otp-footer-actions">
                  {timer > 0 ? (
                    <span className="otp-timer">Resend OTP in {timer}s</span>
                  ) : (
                    <button className="login-resend" onClick={handleSendOtp}>Resend OTP</button>
                  )}
                  <button className="login-resend" onClick={() => setOtpSent(false)}>Change number</button>
                </div>
              </>
            )}

            <div className="login-divider">
              <span>or continue with</span>
            </div>

            <div className="google-login-wrapper" data-testid="google-login">
              {/* REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH */}
              <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
                <GoogleLogin
                  onSuccess={handleGoogleSuccess}
                  onError={() => setError('Google login failed')}
                  width="100%"
                  theme="outline"
                  size="large"
                  text="continue_with"
                  shape="pill"
                />
              </GoogleOAuthProvider>
            </div>
          </div>

          <p className="login-terms">
            By continuing, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
