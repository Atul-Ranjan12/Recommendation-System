import pandas as pd
from ContentBasedRecommender import ContentBasedRecommender

# Set up paths
transaction_path = "./new_transactions.csv"
path_to_article = "./articles.csv"

ARTICLE = pd.read_csv(path_to_article)


def make_soup(purchases):
    soup = ""
    for item in purchases:
        ff = ARTICLE.loc[ARTICLE["article_id"] == item]
        if type(ff["detail_desc"].values[0]) == str:
            soup += str(ff["detail_desc"].values[0])  # Extract the column value using .values[0]
    return soup


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
    def __init__(self):
        self.df = pd.read_csv("./user_similarity_soup.csv")