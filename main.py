from PopularityRecommender import PopularityRecommender
from ContentBasedRecommender import ContentBasedRecommender

# Set up recommenders
popularity_recommender = PopularityRecommender()
content_based_recommender = ContentBasedRecommender()

print(popularity_recommender.recommend(5))
print("Now printing content based recommendations=")
print(content_based_recommender.get_recommendations(108775015, 5))
