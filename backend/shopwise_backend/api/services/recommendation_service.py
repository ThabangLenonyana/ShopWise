from django.db.models import Count
from ..models import Products, Favourite
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    @staticmethod
    def get_recommendations(user, limit=5):
        # Get collaborative filtering recommendations
        collab_recs = RecommendationService._get_collaborative_recommendations(user)
        
        # Get content-based recommendations
        content_recs = RecommendationService._get_content_recommendations(user)
        
        # Combine both recommendation sets with weights
        combined_recs = RecommendationService._combine_recommendations(
            collab_recs, 
            content_recs,
            limit
        )
        
        return combined_recs

    @staticmethod
    def _get_collaborative_recommendations(user):
        # Find products favorited by users with similar taste
        user_favorites = Favourite.objects.filter(user=user)
        similar_users = (
            Favourite.objects.filter(
                product__in=user_favorites.values('product')
            )
            .exclude(user=user)
            .values('user')
            .annotate(common_count=Count('user'))
            .order_by('-common_count')
        )

        return Products.objects.filter(
            favourites__user__in=similar_users.values('user')
        ).exclude(
            favourites__user=user
        ).annotate(
            rec_score=Count('favourites')
        ).order_by('-rec_score')

    @staticmethod 
    def _get_content_recommendations(user):
        # Get user's favorite products
        user_favorites = Products.objects.filter(favourites__user=user)
        
        if not user_favorites.exists():
            return Products.objects.none()

        # Create feature vectors from product attributes
        all_products = Products.objects.all()
        
        # Combine text features
        product_texts = [
            f"{p.name} {p.description} {p.category.name if p.category else ''}"
            for p in all_products
        ]
        
        # Calculate TF-IDF
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(product_texts)
        
        # Calculate similarity with user's favorites
        user_product_indices = [
            i for i, p in enumerate(all_products) 
            if p in user_favorites
        ]
        
        similarity_scores = cosine_similarity(
            tfidf_matrix[user_product_indices],
            tfidf_matrix
        ).mean(axis=0)
        
        # Get recommendations sorted by similarity
        product_scores = list(zip(all_products, similarity_scores))
        sorted_products = sorted(
            product_scores,
            key=lambda x: x[1],
            reverse=True
        )
        
        # Filter out products user already favorited
        recommendations = [
            p[0] for p in sorted_products 
            if p[0] not in user_favorites
        ]
        
        return recommendations

    @staticmethod
    def _combine_recommendations(collab_recs, content_recs, limit):
        # Weight the recommendations (60% collaborative, 40% content-based)
        weighted_products = {}
        
        for i, product in enumerate(collab_recs):
            weighted_products[product.id] = 0.6 * (1.0 / (i + 1))
            
        for i, product in enumerate(content_recs):
            if product.id in weighted_products:
                weighted_products[product.id] += 0.4 * (1.0 / (i + 1))
            else:
                weighted_products[product.id] = 0.4 * (1.0 / (i + 1))
        
        # Sort by final weights
        sorted_products = sorted(
            weighted_products.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top N recommendations
        recommended_ids = [p[0] for p in sorted_products[:limit]]
        return Products.objects.filter(id__in=recommended_ids)
