from PopularityRecommender import PopularityRecommender
from ContentBasedRecommender import ContentBasedRecommender
from UserSimilarityRecommender import UserSimilarityRecommenderInitializer
import streamlit as st

# Set up recommenders
popularity_recommender = PopularityRecommender()
content_based_recommender = ContentBasedRecommender()
user_sim_recommender = UserSimilarityRecommenderInitializer()

popularity_recommendations = popularity_recommender.recommend(5)
similarity_recommendations = content_based_recommender.get_recommendations(108775015, 5)


