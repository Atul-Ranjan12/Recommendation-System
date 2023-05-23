from PopularityRecommender import PopularityRecommender
from ContentBasedRecommender import ContentBasedRecommender
from UserSimilarityRecommender import UserSimilarityRecommender
import streamlit as st

# Set up recommenders
popularity_recommender = PopularityRecommender()
content_based_recommender = ContentBasedRecommender()
user_similarity_recommender = UserSimilarityRecommender()

popularity_recommendations = popularity_recommender.recommend(5)
similarity_recommendations = content_based_recommender.get_recommendations(108775015, 5)
# user_similarity_recommendations = user_similarity_recommender.recommend_new_user([865799006, 706016003, 914805002, 706016002, 785034009])

st.write(f"""
### Popularity Recommendations:
{popularity_recommendations}
### Similarity Recommendations:
{similarity_recommendations}

""")


