import pandas as pd
from ContentBasedRecommender import ContentBasedRecommender
from PopularityRecommender import PopularityRecommender

# Set up paths
transaction_path = "./new_transactions.csv"
path_to_article = "./articles.csv"

ARTICLE = pd.read_csv(path_to_article)


def make_soup(purchases):
    soup = ""
    for item in purchases:
        ff = ARTICLE.loc[ARTICLE["article_id"] == item]
        if type(ff["detail_desc"].values[0]) == str:
            soup += ff["detail_desc"].values[0] # Extract the column value using .values[0]
    return soup


def convert_to_list(string):
    # Remove the brackets at the beginning and end of the string
    string = string.strip('[]')

    # Split the string by the delimiter (e.g., space or comma)
    # and convert each element to an integer
    return [int(item) for item in string.split()]


# Initializer Class to Recommend Articles on the basis of Similar users
class UserSimilarityRecommenderInitializer:
    def __init__(self, transaction=transaction_path, user_id="customer_id", article_id="article_id"):
        self.user_id = user_id
        self.article_id = article_id

        self.df = pd.read_csv(transaction)
        self.df = self.df.groupby(user_id)[article_id].unique().reset_index()

        self.initialize()
        self.save_soup_df()

    def initialize(self):
        self.df["soup"] = self.df[self.article_id].apply(make_soup)

    def save_soup_df(self):
        self.df.to_csv("./user_similarity_soup.csv")


class UserSimilarityRecommender:
    def __init__(self, path="./user_similarity_soup.csv", customer_id="customer_id", article_id="article_id"):
        self.ctr = None
        self.path = path
        self.df = pd.read_csv(path)
        self.customer_id = customer_id
        self.user_article_id = article_id

        self.popularity_recommender = PopularityRecommender()

    def recommend_new_user(self, items, topn):
        soup = make_soup(items)
        new_row = {"customer_id": "001", "article_id": str(items).replace(",", ""), "soup": soup}
        new_row_df = pd.DataFrame(new_row, index=[0])
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)
        self.ctr = ContentBasedRecommender(article_path="", soup_col=[], title_col="customer_id", is_df=True, df=self.df)
        recs = self.recommend("001", topn, new=True)
        return recs

    def get_topn_similar_users(self, user_id, topn):
        return self.ctr.get_recommendations(user_id, topn)

    def get_similar_items(self, user_id):
        """
        Gets similar items of the current user
        :param user_id: user id of the suer
        :return: a tuple (current_user_items, all_similar_user_items)
        """
        # Get the current users articles
        current_user_items = self.get_current_user_articles(user_id)
        # Get all the similar users items
        similar_users = self.get_topn_similar_users(user_id, 3)
        all_similar_user_items = []
        for user in similar_users:
            items = self.get_current_user_articles(user)
            all_similar_user_items.extend(items)

        return current_user_items, all_similar_user_items

    def get_current_user_articles(self, user_id):
        user_articles = self.df.loc[self.df[self.customer_id] == user_id].copy()
        user_articles["article_list"] = user_articles[self.user_article_id].apply(convert_to_list)
        return list(user_articles["article_list"])[0]

    def recommend(self, user_id, topn, new=False):
        if not new:
            self.ctr = ContentBasedRecommender(article_path=self.path, soup_col=[], title_col="customer_id")
        current_user_items, all_similar_items = self.get_similar_items(user_id)
        current_item_set = set(current_user_items)
        recommendations = []
        for item in all_similar_items:
            if item not in current_item_set:
                recommendations.append(item)

        # Sort according to popularity
        top_recommendations = self.get_top_items(self.popularity_recommender.get_count_dict(), recommendations, topn)
        return top_recommendations

    @staticmethod
    def get_top_items(dictionary, items, topn):
        top_items = []

        for item in items:
            if item in dictionary:
                value = dictionary[item]
                top_items.append((item, value))

        top_items.sort(key=lambda x: x[1], reverse=True)
        result = [item for item, _ in top_items[:topn]]

        return result
