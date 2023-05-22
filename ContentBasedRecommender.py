import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Set up File Paths
articles = "./articles.csv"


class ContentBasedRecommender:
    def __init__(self, article_path=articles):
        self.df = pd.read_csv(article_path)
        self.initialize_df(["prod_name",
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
                          )
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
        self.titles = self.df["article_id"]
        self.indices = pd.Series(self.df.index, index=self.df["article_id"])

    def initialize_df(self, columns):
        self.df["soup"] = self.df[columns].apply(lambda row: ''.join(str(cell) for cell in row), axis=1)

    def fit(self):
        return self.count.fit_transform(self.df["soup"])

    def get_recommendations(self, title, topn):
        idx = self.indices[title]
        sim_scores = linear_kernel(self.count_matrix[idx], self.count_matrix).flatten()
        sim_scores_indices = list(enumerate(sim_scores))
        sim_scores_indices = sorted(sim_scores_indices, key=lambda x: x[1], reverse=True)
        sim_scores_indices = sim_scores_indices[1:31]
        article_indices = [i[0] for i in sim_scores_indices]
        return list(self.titles.iloc[article_indices])[:topn]
