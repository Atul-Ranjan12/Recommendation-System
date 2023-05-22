import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Set up File Paths
articles = "./articles.csv"
columns = ["prod_name",
           "product_type_name",
           "product_group_name",
           "graphical_appearance_name",
           "colour_group_name",
           "perceived_colour_value_name",
           "department_name",
           "index_group_name",
           "section_name",
           "garment_group_name",
           "detail_desc"]


class ContentBasedRecommender:
    def __init__(self, article_path=articles, soup_col=columns, title_col="article_id"):
        """
        This class initializes the content based filtering recommendation system.
        It finds similar products in a company's product line and uses distance
        metrics to find the most similar contents.

        :param article_path: Path of the file containing information about the contenst
        :param soup_col: Columns to be included for the similarity metric
        :param title_col: Name of the column containing the articles
        """
        self.df = pd.read_csv(article_path)
        self.initialize_df(soup_col)
        self.count = TfidfVectorizer(analyzer="word",
                                     ngram_range=(1, 2),
                                     min_df=0.003,
                                     max_df=0.5,
                                     max_features=5000,
                                     stop_words="english",
                                     use_idf=False,
                                     norm=None,  # Disable normalization for sparse representation
                                     binary=True)  # Use binary representation for sparse matrix
        self.count_matrix = self.fit()
        self.df = self.df.reset_index()
        self.titles = self.df[title_col]
        self.indices = pd.Series(self.df.index, index=self.df[title_col])

    def initialize_df(self, cols):
        """
        This function creates a soup column for the dataframe
        :param cols: Columns to be included in the soup
        :return: Null
        """
        self.df["soup"] = self.df[cols].apply(lambda row: ''.join(str(cell) for cell in row), axis=1)

    def fit(self):
        """
        Fits the count matrix
        :return: Returns the count matrix
        """
        return self.count.fit_transform(self.df["soup"])

    def get_recommendations(self, title, topn):
        """
        Recommends products according to the given title
        :param title: Product for which recommendations are required (product id)
        :param topn:  Top n Most similar products
        :return:
        """
        idx = self.indices[title]
        sim_scores = linear_kernel(self.count_matrix[idx], self.count_matrix).flatten()
        sim_scores_indices = list(enumerate(sim_scores))
        sim_scores_indices = sorted(sim_scores_indices, key=lambda x: x[1], reverse=True)
        sim_scores_indices = sim_scores_indices[1:31]
        article_indices = [i[0] for i in sim_scores_indices]
        return list(self.titles.iloc[article_indices])[:topn]
