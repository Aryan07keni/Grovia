"""
Grovia ML Recommendation Engine
Collaborative Filtering using SVD (Matrix Factorization)
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pickle
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroviaRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity_matrix = None
        self.user_similarity_matrix = None
        self.svd_model = None
        self.user_factors = None
        self.item_factors = None
        self.user_ids = []
        self.product_ids = []
        self.product_features = None
        self.is_trained = False
        
    def build_user_item_matrix(self, interactions, products):
        """
        Build user-item interaction matrix
        interactions: list of {'user_id', 'product_id', 'rating', 'action_type'}
        """
        logger.info("Building user-item interaction matrix...")
        
        # Create DataFrame
        df = pd.DataFrame(interactions)
        
        # Weight different actions
        action_weights = {
            'purchase': 5.0,
            'add_to_cart': 3.0,
            'view': 1.0,
            'click': 0.5
        }
        
        if 'action_type' in df.columns:
            df['weight'] = df['action_type'].map(action_weights).fillna(1.0)
        else:
            df['weight'] = 1.0
        
        # If no rating column, use weight as rating
        if 'rating' not in df.columns:
            df['rating'] = df['weight']
        
        # Create pivot table
        self.user_item_matrix = df.pivot_table(
            index='user_id',
            columns='product_id',
            values='rating',
            fill_value=0
        )
        
        self.user_ids = list(self.user_item_matrix.index)
        self.product_ids = list(self.user_item_matrix.columns)
        
        logger.info(f"Matrix shape: {self.user_item_matrix.shape}")
        logger.info(f"Users: {len(self.user_ids)}, Products: {len(self.product_ids)}")
        
        return self.user_item_matrix
    
    def build_item_similarity(self):
        """Calculate item-item similarity using cosine similarity"""
        logger.info("Building item similarity matrix...")
        
        # Transpose to get items as rows
        item_matrix = self.user_item_matrix.T.values
        
        # Calculate cosine similarity
        self.item_similarity_matrix = cosine_similarity(item_matrix)
        
        logger.info(f"Item similarity matrix shape: {self.item_similarity_matrix.shape}")
        return self.item_similarity_matrix
    
    def build_user_similarity(self):
        """Calculate user-user similarity using cosine similarity"""
        logger.info("Building user similarity matrix...")
        
        # Calculate cosine similarity between users
        self.user_similarity_matrix = cosine_similarity(self.user_item_matrix.values)
        
        logger.info(f"User similarity matrix shape: {self.user_similarity_matrix.shape}")
        return self.user_similarity_matrix
    
    def build_svd_model(self, n_components=50):
        """
        Build SVD model for matrix factorization
        Reduces dimensionality for better recommendations
        """
        logger.info(f"Building SVD model with {n_components} components...")
        
        matrix = self.user_item_matrix.values
        
        # Apply SVD
        self.svd_model = TruncatedSVD(n_components=min(n_components, min(matrix.shape) - 1))
        self.user_factors = self.svd_model.fit_transform(matrix)
        self.item_factors = self.svd_model.components_.T
        
        logger.info(f"User factors shape: {self.user_factors.shape}")
        logger.info(f"Item factors shape: {self.item_factors.shape}")
        logger.info(f"Explained variance: {self.svd_model.explained_variance_ratio_.sum():.2%}")
        
        return self.user_factors, self.item_factors
    
    def build_content_features(self, products, categories):
        """Build content-based features using TF-IDF"""
        logger.info("Building content-based features...")
        
        # Create feature text for each product
        features = []
        product_dict = {p['id']: p for p in products}
        category_dict = {c['id']: c['name'] for c in categories}
        
        for product_id in self.product_ids:
            product = product_dict.get(product_id, {})
            category_name = category_dict.get(product.get('category_id', ''), '')
            
            feature_text = f"""
                {product.get('name', '')} 
                {category_name}
                {product.get('description', '')}
                {product.get('weight_options', [''])[0] if product.get('weight_options') else ''}
            """
            features.append(feature_text.lower())
        
        # Convert to TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.product_features = vectorizer.fit_transform(features)
        logger.info(f"Content features shape: {self.product_features.shape}")
        
        return self.product_features
    
    def get_user_based_recommendations(self, user_id, n=10):
        """
        Get recommendations based on similar users (User-Based CF)
        """
        if not self.is_trained:
            logger.warning("Model not trained. Train first.")
            return []
        
        try:
            # Find user index
            user_idx = self.user_ids.index(user_id)
            
            # Get similarity scores for this user
            user_similarities = self.user_similarity_matrix[user_idx]
            
            # Get top similar users (excluding self)
            similar_users = np.argsort(user_similarities)[::-1][1:20]
            
            # Get products liked by similar users
            product_scores = defaultdict(float)
            
            for sim_user_idx in similar_users:
                similarity_score = user_similarities[sim_user_idx]
                if similarity_score <= 0:
                    continue
                    
                user_ratings = self.user_item_matrix.iloc[sim_user_idx]
                
                for product_idx, rating in enumerate(user_ratings):
                    if rating > 0:
                        product_id = self.product_ids[product_idx]
                        product_scores[product_id] += similarity_score * rating
            
            # Remove products already interacted by user
            user_ratings = self.user_item_matrix.iloc[user_idx]
            interacted_products = set(
                self.product_ids[i] for i, rating in enumerate(user_ratings) if rating > 0
            )
            
            # Sort and get top N
            recommendations = []
            for product_id, score in sorted(product_scores.items(), key=lambda x: x[1], reverse=True):
                if product_id not in interacted_products and len(recommendations) < n:
                    recommendations.append({
                        'product_id': product_id,
                        'score': round(score, 4),
                        'type': 'user_based'
                    })
            
            return recommendations
            
        except ValueError:
            logger.warning(f"User {user_id} not found")
            return []
    
    def get_item_based_recommendations(self, product_id, n=10):
        """
        Get recommendations based on similar items (Item-Based CF)
        """
        if not self.is_trained:
            logger.warning("Model not trained. Train first.")
            return []
        
        try:
            # Find product index
            product_idx = self.product_ids.index(product_id)
            
            # Get similarity scores
            similarities = self.item_similarity_matrix[product_idx]
            
            # Get top similar items
            similar_items = np.argsort(similarities)[::-1][1:n+1]
            
            recommendations = []
            for idx in similar_items:
                if similarities[idx] > 0.1:
                    recommendations.append({
                        'product_id': self.product_ids[idx],
                        'score': round(float(similarities[idx]), 4),
                        'type': 'item_based'
                    })
            
            return recommendations
            
        except ValueError:
            logger.warning(f"Product {product_id} not found")
            return []
    
    def get_svd_recommendations(self, user_id, n=10):
        """
        Get recommendations using SVD matrix factorization
        """
        if not self.is_trained or self.svd_model is None:
            logger.warning("SVD model not available")
            return []
        
        try:
            # Find user index
            user_idx = self.user_ids.index(user_id)
            
            # Get user's original ratings
            user_ratings = self.user_item_matrix.iloc[user_idx].values
            
            # Predict ratings using SVD
            user_vector = self.user_factors[user_idx]
            predicted_ratings = self.svd_model.inverse_transform([user_vector])[0]
            
            # Get products user hasn't interacted with
            interacted_indices = set(np.where(user_ratings > 0)[0])
            
            # Create recommendations
            recommendations = []
            for i, predicted_rating in enumerate(predicted_ratings):
                if i not in interacted_indices and predicted_rating > 0:
                    recommendations.append({
                        'product_id': self.product_ids[i],
                        'score': round(float(predicted_rating), 4),
                        'type': 'svd'
                    })
            
            # Sort by predicted rating
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            return recommendations[:n]
            
        except ValueError:
            logger.warning(f"User {user_id} not found")
            return []
    
    def get_content_based_recommendations(self, product_id, n=10):
        """
        Get recommendations based on product content similarity
        """
        if self.product_features is None:
            logger.warning("Content features not built")
            return []
        
        try:
            product_idx = self.product_ids.index(product_id)
            
            # Get similarity scores
            similarities = cosine_similarity(
                self.product_features[product_idx:product_idx+1],
                self.product_features
            )[0]
            
            # Get top similar items
            similar_items = np.argsort(similarities)[::-1][1:n+1]
            
            recommendations = []
            for idx in similar_items:
                if similarities[idx] > 0.1:
                    recommendations.append({
                        'product_id': self.product_ids[idx],
                        'score': round(float(similarities[idx]), 4),
                        'type': 'content_based'
                    })
            
            return recommendations
            
        except ValueError:
            logger.warning(f"Product {product_id} not found")
            return []
    
    def get_hybrid_recommendations(self, user_id, product_id=None, n=12):
        """
        Combine multiple recommendation approaches
        """
        recommendations = {}
        weights = {
            'svd': 0.4,
            'user_based': 0.3,
            'item_based': 0.2,
            'content_based': 0.1
        }
        
        # Get SVD recommendations (best for cold start)
        svd_recs = self.get_svd_recommendations(user_id, n)
        for rec in svd_recs:
            recommendations[rec['product_id']] = {
                'product_id': rec['product_id'],
                'score': rec['score'] * weights['svd'],
                'scores': [rec['score']],
                'types': ['svd']
            }
        
        # Get user-based recommendations
        user_recs = self.get_user_based_recommendations(user_id, n)
        for rec in user_recs:
            if rec['product_id'] in recommendations:
                recommendations[rec['product_id']]['score'] += rec['score'] * weights['user_based']
                recommendations[rec['product_id']]['scores'].append(rec['score'])
                recommendations[rec['product_id']]['types'].append('user_based')
            else:
                recommendations[rec['product_id']] = {
                    'product_id': rec['product_id'],
                    'score': rec['score'] * weights['user_based'],
                    'scores': [rec['score']],
                    'types': ['user_based']
                }
        
        # Get item-based recommendations (if product_id provided)
        if product_id:
            item_recs = self.get_item_based_recommendations(product_id, n)
            for rec in item_recs:
                if rec['product_id'] in recommendations:
                    recommendations[rec['product_id']]['score'] += rec['score'] * weights['item_based']
                    recommendations[rec['product_id']]['scores'].append(rec['score'])
                    recommendations[rec['product_id']]['types'].append('item_based')
                else:
                    recommendations[rec['product_id']] = {
                        'product_id': rec['product_id'],
                        'score': rec['score'] * weights['item_based'],
                        'scores': [rec['score']],
                        'types': ['item_based']
                    }
        
        # Get content-based recommendations
        if product_id:
            content_recs = self.get_content_based_recommendations(product_id, n)
            for rec in content_recs:
                if rec['product_id'] in recommendations:
                    recommendations[rec['product_id']]['score'] += rec['score'] * weights['content_based']
                    recommendations[rec['product_id']]['scores'].append(rec['score'])
                    recommendations[rec['product_id']]['types'].append('content_based')
                else:
                    recommendations[rec['product_id']] = {
                        'product_id': rec['product_id'],
                        'score': rec['score'] * weights['content_based'],
                        'scores': [rec['score']],
                        'types': ['content_based']
                    }
        
        # Sort by final score
        sorted_recs = sorted(recommendations.values(), key=lambda x: x['score'], reverse=True)
        
        # Add final score and confidence
        for rec in sorted_recs[:n]:
            rec['final_score'] = round(rec['score'], 4)
            rec['confidence'] = 'high' if len(rec['types']) >= 2 else 'medium' if rec['score'] > 0.5 else 'low'
        
        return sorted_recs[:n]
    
    def train(self, interactions, products, categories, n_components=50):
        """
        Train the complete recommendation model
        """
        logger.info("=" * 50)
        logger.info("Training Grovia Recommendation Engine")
        logger.info("=" * 50)
        
        # Build user-item matrix
        self.build_user_item_matrix(interactions, products)
        
        # Skip if not enough data
        if len(self.user_ids) < 2 or len(self.product_ids) < 2:
            logger.warning("Not enough data for training")
            self.is_trained = False
            return False
        
        # Build similarity matrices
        self.build_item_similarity()
        self.build_user_similarity()
        
        # Build SVD model
        self.build_svd_model(n_components)
        
        # Build content features
        self.build_content_features(products, categories)
        
        self.is_trained = True
        logger.info("✅ Model training complete!")
        
        # Save model
        self.save_model()
        
        return True
    
    def save_model(self, path=None):
        """Save trained model to file"""
        if path is None:
            path = Path(__file__).parent / 'grovia_model.pkl'
        
        with open(path, 'wb') as f:
            pickle.dump({
                'user_item_matrix': self.user_item_matrix,
                'item_similarity_matrix': self.item_similarity_matrix,
                'user_similarity_matrix': self.user_similarity_matrix,
                'svd_model': self.svd_model,
                'user_factors': self.user_factors,
                'item_factors': self.item_factors,
                'user_ids': self.user_ids,
                'product_ids': self.product_ids,
                'product_features': self.product_features,
                'is_trained': self.is_trained
            }, f)
        
        logger.info(f"💾 Model saved to {path}")
    
    def load_model(self, path=None):
        """Load trained model from file"""
        if path is None:
            path = Path(__file__).parent / 'grovia_model.pkl'
        
        if path.exists():
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.user_item_matrix = data['user_item_matrix']
                self.item_similarity_matrix = data['item_similarity_matrix']
                self.user_similarity_matrix = data['user_similarity_matrix']
                self.svd_model = data['svd_model']
                self.user_factors = data['user_factors']
                self.item_factors = data['item_factors']
                self.user_ids = data['user_ids']
                self.product_ids = data['product_ids']
                self.product_features = data.get('product_features')
                self.is_trained = data['is_trained']
            
            logger.info("✅ Model loaded successfully")
            return True
        
        logger.warning("No saved model found")
        return False

# Initialize global recommender
recommender = GroviaRecommender()