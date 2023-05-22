import pandas as pd
import collections

# Set up Global Variables
path = "./new_transactions.csv"


# Popularity Based Recommendations
class PopularityRecommender:
    def __init__(self, transaction_path=path, sort_col="article_id", transaction_date_col="t_dat"):
        """
        This class is used to recommend most popular products.
        It uses a transaction path which is the path of the csv
        containing the transaction data. And the column containing the
        items

        :param transaction_path: path of the transaction data csv
        :param sort_col: name of the column to be recommended
        :param transaction_date_col: name of the column containng transaction dates
        """

        self.df = pd.read_csv(transaction_path)
        self.df[transaction_date_col] = pd.to_datetime(self.df[transaction_date_col])

        self.col = sort_col

        self.count_dict = collections.Counter(list(self.df[self.col]))
        self.sorted_count_df = sorted(self.count_dict.items(), key=lambda x: x[1], reverse=True)

    def recommend(self, n):
        """
        Gets top n recommendations
        :param n: number of top items to be recommended
        :return: array of top n recommendations
        """
        top_n_items = [item[0] for item in self.sorted_count_df[:n]]
        return top_n_items


