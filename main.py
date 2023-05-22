from PopularityRecommender import PopularityRecommender
from ContentBasedRecommender import ContentBasedRecommender
import streamlit as st

# Set up recommenders
popularity_recommender = PopularityRecommender()
content_based_recommender = ContentBasedRecommender()

popularity_recommendations = popularity_recommender.recommend(5)
similarity_recommendations = content_based_recommender.get_recommendations(108775015, 5)

st.write("""
    # Recommendation System Try
""")

st.write(f"""
### Popularity Recommendations: 
{str(popularity_recommendations)}
### Content Based Recommendations:
{str(similarity_recommendations)}
""")
