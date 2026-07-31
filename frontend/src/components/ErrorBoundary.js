import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Grovia ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          fontFamily: "'Manrope', sans-serif",
          backgroundColor: '#F4F7F5',
          color: '#1A1D1A',
          textAlign: 'center'
        }}>
          <div style={{
            background: '#FFFFFF',
            padding: '40px 32px',
            borderRadius: '20px',
            boxShadow: '0 12px 40px rgba(11, 140, 76, 0.1)',
            maxWidth: '480px',
            width: '100%'
          }}>
            <h1 style={{ fontFamily: "'Outfit', sans-serif", color: '#0B8C4C', fontSize: '2rem', marginBottom: '12px' }}>
              Grovia
            </h1>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', color: '#333' }}>
              Something went wrong loading the page
            </h2>
            <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '24px' }}>
              {this.state.error?.toString() || 'An unexpected runtime error occurred.'}
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.href = '/';
              }}
              style={{
                background: '#0B8C4C',
                color: 'white',
                border: 'none',
                padding: '14px 28px',
                borderRadius: '12px',
                fontWeight: '600',
                fontSize: '0.95rem',
                cursor: 'pointer'
              }}
            >
              Reload Grovia App
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
