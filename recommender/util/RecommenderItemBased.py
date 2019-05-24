import pandas as pd
import numpy as np


class RecommenderItemBased(object):
    def __init__(self):
        self.path = '/home/docker/recommender/processed_data/'
        self.q_movies = pd.read_pickle(self.path + 'q_movies.pkl')
        self.cosine_sim_overview = np.load(self.path + 'cosine_sim_overview.npy')
        self.cosine_sim_keywords = np.load(self.path + 'cosine_sim_keywords.npy')
        self.indices = pd.Series(self.q_movies.index, index=self.q_movies['title'])

    def get_recommendations_by_ratings(self, title, k=5):
        # return self.q_movies[['title', 'vote_average', 'overview', 'genres']].iloc[0:k].astype(str).values.tolist()
        # Get index by title
        
        res_array = self.q_movies[['title', 'vote_average', 'overview', 'genres']].iloc[0:k].astype(str).values.tolist()
        
        # Handle empty string
        if title == "":
            for ele in res_array:
                ele.append("0")
        else:
            idx = self.indices[title]
            for ele in res_array:
                res_title = ele[0]
                res_idx = self.indices[res_title]
                score = self.cosine_sim_keywords[idx][res_idx]
                ele.append(str(round(score*100)))
        return res_array

    def get_recommendations_by_items(self, title, mode, k=5):
        return {
            'content': self._recommendation_by_items(title, self.cosine_sim_overview, k),
            'keyword': self._recommendation_by_items(title, self.cosine_sim_keywords, k),
        }[mode]

    def _recommendation_by_items(self, title, cosin_sim, k=5):
        # Get index by title
        idx = self.indices[title]
        # Get the similarity scores of all movies with this movie
        sim_scores = list(enumerate(cosin_sim[idx]))
        # Sort the similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get score of top K most similar to specified movie
        sim_scores = sim_scores[0:k]
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        # Return top K related movies
        # return self.q_movies[['title', 'vote_average', 'overview', 'genres']].iloc[movie_indices].astype(str).values.tolist()
        res_array = self.q_movies[['title', 'vote_average', 'overview', 'genres']].iloc[movie_indices].astype(str).values.tolist()
        for ele in res_array:
            res_title = ele[0]
            res_idx = self.indices[res_title]
            score = cosin_sim[idx][res_idx]
            if isinstance(score, np.ndarray):
                score = score[0]
            ele.append(int(round(score*100)))
        return res_array
