import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navigation, X, MapPin, Store, Clock, Star, Loader2, Search, ShoppingCart, ArrowLeft } from 'lucide-react';
import axios from 'axios';
import './StoreMap.css';

function StoreMap({ isOpen, onClose, onSelectStore }) {
  const [userLocation, setUserLocation] = useState(null);
  const [nearbyStores, setNearbyStores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [searchRadius, setSearchRadius] = useState(5000);
  const [selectedStore, setSelectedStore] = useState(null);
  const [searchLocation, setSearchLocation] = useState('');
  const [locationError, setLocationError] = useState('');
  const [showProducts, setShowProducts] = useState(false);
  const [storeProducts, setStoreProducts] = useState([]);
  const [productsLoading, setProductsLoading] = useState(false);
  
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const markersRef = useRef([]);
  const circleRef = useRef(null);
  const searchInputRef = useRef(null);
  const autocompleteRef = useRef(null);
  const navigate = useNavigate();

  const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

  // Load Google Maps script with Places API
  useEffect(() => {
    if (window.google && window.google.maps) {
      setMapsLoaded(true);
      return;
    }
    
    const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
    if (!apiKey) return;
    
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.async = true;
    script.defer = true;
    script.onload = () => setMapsLoaded(true);
    document.head.appendChild(script);
  }, []);

  // Initialize autocomplete for location search
  useEffect(() => {
    if (mapsLoaded && searchInputRef.current && !autocompleteRef.current) {
      autocompleteRef.current = new window.google.maps.places.Autocomplete(searchInputRef.current, {
        types: ['(cities)', 'locality', 'sublocality'],
        componentRestrictions: { country: 'in' }
      });
      
      autocompleteRef.current.addListener('place_changed', () => {
        const place = autocompleteRef.current.getPlace();
        if (place && place.geometry) {
          const location = {
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng()
          };
          setUserLocation(location);
          fetchNearbyStores(location);
          setSearchLocation(place.formatted_address);
          setLocationError('');
        } else {
          setLocationError('Please select a location from the dropdown suggestions');
        }
      });
    }
  }, [mapsLoaded]);

  // Reverse geocode to get address from coordinates
  const reverseGeocode = async (location) => {
    if (!window.google) return;
    try {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ location: location }, (results, status) => {
        if (status === 'OK' && results[0]) {
          setSearchLocation(results[0].formatted_address);
        }
      });
    } catch (error) {
      console.error('Reverse geocoding error:', error);
    }
  };

  // Get user's current location
  const getUserLocation = () => {
    setLoading(true);
    setLocationError('');
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(location);
          await fetchNearbyStores(location);
          reverseGeocode(location);
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationError('Unable to get your location. Please search for a location manually.');
          setLoading(false);
          const defaultLocation = { lat: 12.9352, lng: 77.6245 };
          setUserLocation(defaultLocation);
          fetchNearbyStores(defaultLocation);
          setSearchLocation('Bangalore, Karnataka');
        }
      );
    } else {
      setLocationError('Geolocation not supported. Please search for a location.');
      setLoading(false);
    }
  };

  // Calculate distance between two points in km
  const calculateDistance = (lat1, lng1, lat2, lng2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return Math.round(R * c * 10) / 10;
  };

  // Fetch nearby stores from backend API
  const fetchNearbyStores = async (location) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/stores/nearby-real`, {
        params: {
          lat: location.lat,
          lng: location.lng,
          radius: searchRadius
        }
      });
      
      if (response.data.stores && response.data.stores.length > 0) {
        setNearbyStores(response.data.stores);
      } else {
        const fallbackResponse = await axios.get(`${API}/stores`);
        const storesWithDistance = fallbackResponse.data.stores.map(store => ({
          ...store,
          distance: calculateDistance(location.lat, location.lng, store.lat, store.lng)
        }));
        storesWithDistance.sort((a, b) => a.distance - b.distance);
        setNearbyStores(storesWithDistance);
      }
    } catch (error) {
      console.error('Error fetching stores:', error);
      try {
        const fallbackResponse = await axios.get(`${API}/stores`);
        setNearbyStores(fallbackResponse.data.stores);
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError);
        setNearbyStores([]);
      }
    }
    setLoading(false);
  };

  // Fetch products for selected store
  const fetchStoreProducts = async (store) => {
    setProductsLoading(true);
    setShowProducts(true);
    try {
      const response = await axios.get(`${API}/stores/${store.id}/products`);
      setStoreProducts(response.data.products || []);
    } catch (error) {
      console.error('Error fetching store products:', error);
      setStoreProducts([]);
    }
    setProductsLoading(false);
  };

  // Handle store selection
  const handleSelectStore = (store) => {
    setSelectedStore(store);
    fetchStoreProducts(store);
  };

  // Confirm store selection and close
  const confirmStoreSelection = () => {
    if (selectedStore && onSelectStore) {
      onSelectStore(selectedStore);
    }
    onClose();
  };

  const handleRadiusChange = (radius) => {
    setSearchRadius(radius);
    if (userLocation) {
      fetchNearbyStores(userLocation);
    }
  };

  const handleLocationSearch = (e) => {
    e.preventDefault();
    if (searchInputRef.current && autocompleteRef.current) {
      const place = autocompleteRef.current.getPlace();
      if (!place || !place.geometry) {
        setLocationError('Please select a location from the dropdown');
      }
    }
  };

  // Initialize map
  useEffect(() => {
    if (!mapsLoaded || !userLocation || !mapRef.current) return;
    
    try {
      const map = new window.google.maps.Map(mapRef.current, {
        center: userLocation,
        zoom: 13,
        styles: [
          { featureType: 'poi', stylers: [{ visibility: 'off' }] },
          { featureType: 'water', elementType: 'geometry.fill', stylers: [{ color: '#e3f2fd' }] }
        ],
        disableDefaultUI: false,
        zoomControl: true,
        mapTypeControl: false,
        streetViewControl: false
      });
      
      mapInstance.current = map;
      
      markersRef.current.forEach(marker => marker.setMap(null));
      markersRef.current = [];
      
      new window.google.maps.Marker({
        position: userLocation,
        map,
        title: searchLocation || 'Your Location',
        icon: {
          url: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
          scaledSize: new window.google.maps.Size(40, 40)
        }
      });
      
      if (circleRef.current) {
        circleRef.current.setMap(null);
      }
      circleRef.current = new window.google.maps.Circle({
        center: userLocation,
        radius: searchRadius,
        map,
        fillColor: '#2e7d32',
        fillOpacity: 0.1,
        strokeColor: '#2e7d32',
        strokeOpacity: 0.3,
        strokeWeight: 1
      });
      
      nearbyStores.forEach(store => {
        if (store.lat && store.lng) {
          const marker = new window.google.maps.Marker({
            position: { lat: store.lat, lng: store.lng },
            map,
            title: store.name,
            icon: {
              url: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
              scaledSize: new window.google.maps.Size(36, 36)
            }
          });
          
          const infoWindow = new window.google.maps.InfoWindow({
            content: `
              <div style="padding: 12px; max-width: 250px;">
                <strong style="font-size: 14px;">${store.name}</strong><br/>
                <span style="font-size: 12px; color: #666;">${store.address}</span><br/>
                ${store.rating ? `<span style="font-size: 12px;">⭐ ${store.rating}</span><br/>` : ''}
                ${store.distance_km ? `<span style="font-size: 12px; color: #2e7d32;">📍 ${store.distance_km} km away</span><br/>` : ''}
              </div>
            `
          });
          
          marker.addListener('click', () => {
            infoWindow.open(map, marker);
            handleSelectStore(store);
          });
          
          markersRef.current.push(marker);
        }
      });
      
    } catch (err) {
      console.error('Map initialization error:', err);
    }
  }, [mapsLoaded, userLocation, nearbyStores, searchRadius, searchLocation]);

  useEffect(() => {
    if (isOpen) {
      getUserLocation();
    } else {
      setShowProducts(false);
      setSelectedStore(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="store-map-modal">
      <div className="store-map-overlay" onClick={onClose}></div>
      <div className="store-map-content">
        <div className="store-map-header">
          <h2>{showProducts ? 'Store Products' : 'Select a Store'}</h2>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {!showProducts ? (
          <>
            <div className="store-map-controls">
              <div className="location-search">
                <form onSubmit={handleLocationSearch} className="search-form">
                  <div style={{ position: 'relative', flex: 1 }}>
                    <Search size={18} className="search-icon" />
                    <input
                      ref={searchInputRef}
                      type="text"
                      placeholder="Search for a city or area..."
                      className="location-input"
                    />
                  </div>
                  <button type="submit" className="search-btn">Search</button>
                </form>
              </div>
              
              <div className="location-actions">
                <button className="current-location-btn" onClick={getUserLocation}>
                  <Navigation size={16} />
                  Use my current location
                </button>

                <div className="radius-control">
                  <span>Radius:</span>
                  <div className="radius-buttons">
                    <button className={searchRadius === 1000 ? 'active' : ''} onClick={() => handleRadiusChange(1000)}>1km</button>
                    <button className={searchRadius === 2000 ? 'active' : ''} onClick={() => handleRadiusChange(2000)}>2km</button>
                    <button className={searchRadius === 3000 ? 'active' : ''} onClick={() => handleRadiusChange(3000)}>3km</button>
                    <button className={searchRadius === 5000 ? 'active' : ''} onClick={() => handleRadiusChange(5000)}>5km</button>
                    <button className={searchRadius === 10000 ? 'active' : ''} onClick={() => handleRadiusChange(10000)}>10km</button>
                  </div>
                </div>
              </div>
              
              {locationError && <div className="location-error">{locationError}</div>}
              {searchLocation && (
                <div className="current-location-display">
                  <MapPin size={14} />
                  <span>{searchLocation}</span>
                </div>
              )}
            </div>

            <div className="store-map-layout">
              <div className="store-list-panel">
                <h3>Nearby Stores ({nearbyStores.length})</h3>
                {loading ? (
                  <div className="loading-stores">
                    <Loader2 size={40} className="spinner" />
                    <p>Finding stores near you...</p>
                  </div>
                ) : nearbyStores.length === 0 ? (
                  <div className="no-stores">
                    <Store size={48} />
                    <p>No stores found within {searchRadius/1000}km</p>
                    <p className="hint">Try increasing the search radius</p>
                  </div>
                ) : (
                  <div className="store-list">
                    {nearbyStores.map(store => (
                      <div
                        key={store.id}
                        className={`store-list-item ${selectedStore?.id === store.id ? 'active' : ''}`}
                        onClick={() => handleSelectStore(store)}
                      >
                        <div className="store-list-icon">
                          <MapPin size={18} />
                        </div>
                        <div className="store-list-info">
                          <h4>{store.name}</h4>
                          <p className="store-address">{store.address}</p>
                          <div className="store-meta">
                            {store.rating > 0 && <span><Star size={12} /> {store.rating}</span>}
                            {store.distance_km && <span><Clock size={12} /> {store.distance_km} km</span>}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <div className="store-map-panel">
                <div ref={mapRef} className="store-map-container"></div>
              </div>
            </div>
          </>
        ) : (
          <div className="store-products-panel">
            <div className="products-header">
              <button className="back-btn" onClick={() => setShowProducts(false)}>
                <ArrowLeft size={20} />
                Back to Stores
              </button>
              <h3>{selectedStore?.name}</h3>
              <button className="confirm-store-btn" onClick={confirmStoreSelection}>
                Select This Store
              </button>
            </div>
            
            <div className="products-list">
              {productsLoading ? (
                <div className="loading-products">
                  <Loader2 size={40} className="spinner" />
                  <p>Loading products...</p>
                </div>
              ) : storeProducts.length === 0 ? (
                <div className="no-products">
                  <ShoppingCart size={48} />
                  <p>No products available in this store</p>
                </div>
              ) : (
                <div className="product-grid">
                  {storeProducts.map(product => (
                    <div key={product.id} className="product-item">
                      <img src={product.image} alt={product.name} className="product-image" />
                      <div className="product-info">
                        <h4>{product.name}</h4>
                        <p className="product-price">Rs. {product.store_price || product.base_price}</p>
                        <button 
                          className="add-to-cart-btn"
                          onClick={() => {
                            confirmStoreSelection();
                            navigate(`/product/${product.id}`);
                          }}
                        >
                          View & Add
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default StoreMap;