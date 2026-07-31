"""
Grovia ML Recommendation Engine
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import pickle
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroviaRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.user_ids = []
        self.product_ids = []
        self.is_trained = False
        
    def build_user_item_matrix(self, interactions, products):
        """Build user-item interaction matrix"""
        logger.info("Building user-item interaction matrix...")
        
        self.user_ids = list(set([i['user_id'] for i in interactions]))
        self.product_ids = list(set([p['id'] for p in products]))
        
        self.user_item_matrix = {}
        for interaction in interactions:
            user = interaction['user_id']
            product = interaction['product_id']
            rating = interaction.get('rating', 1)
            
            if user not in self.user_item_matrix:
                self.user_item_matrix[user] = {}
            self.user_item_matrix[user][product] = rating
        
        logger.info(f"Users: {len(self.user_ids)}, Products: {len(self.product_ids)}")
        return self.user_item_matrix
    
    def get_user_based_recommendations(self, user_id, n=10):
        """Get recommendations based on similar users"""
        if user_id not in self.user_item_matrix:
            return []
        
        user_products = set(self.user_item_matrix[user_id].keys())
        product_scores = defaultdict(float)
        
        for other_user, products in self.user_item_matrix.items():
            if other_user == user_id:
                continue
            
            other_products = set(products.keys())
            common = user_products & other_products
            
            if len(common) > 0:
                similarity = len(common) / len(user_products | other_products)
                
                for product, rating in products.items():
                    if product not in user_products:
                        product_scores[product] += similarity * rating
        
        sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for product_id, score in sorted_products[:n]:
            recommendations.append({
                'product_id': product_id,
                'score': round(score, 4),
                'type': 'user_based'
            })
        
        return recommendations
    
    def get_hybrid_recommendations(self, user_id, product_id=None, n=12):
        """Get hybrid recommendations"""
        recommendations = self.get_user_based_recommendations(user_id, n)
        
        for rec in recommendations:
            rec['final_score'] = rec['score']
            rec['confidence'] = 'medium'
        
        return recommendations
    
    def train(self, interactions, products, categories, n_components=10):
        """Train the model"""
        logger.info("Training Grovia Recommendation Engine...")
        
        self.build_user_item_matrix(interactions, products)
        
        if len(self.user_ids) < 2:
            logger.warning("Not enough users for training")
            self.is_trained = False
            return False
        
        self.is_trained = True
        logger.info(" Model training complete!")
        
        self.save_model()
        return True
    
    def save_model(self, path=None):
        """Save model to file"""
        if path is None:
            path = Path(__file__).parent / 'grovia_model.pkl'
        
        with open(path, 'wb') as f:
            pickle.dump({
                'user_item_matrix': self.user_item_matrix,
                'user_ids': self.user_ids,
                'product_ids': self.product_ids,
                'is_trained': self.is_trained
            }, f)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path=None):
        """Load model from file"""
        if path is None:
            path = Path(__file__).parent / 'grovia_model.pkl'
        
        if path.exists():
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.user_item_matrix = data['user_item_matrix']
                self.user_ids = data['user_ids']
                self.product_ids = data['product_ids']
                self.is_trained = data['is_trained']
            logger.info("Model loaded successfully")
            return True
        
        return False

recommender = GroviaRecommender()
