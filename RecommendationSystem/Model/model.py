import os
import sys
from typing import List

import torch
from sentence_transformers import SentenceTransformer
from torch import nn

from RecommendationSystem.API.RESTApi.abstract_model import AbstractModel
from RecommendationSystem.DB.db_models.article import Article
from RecommendationSystem.DB.db_models.comment import Comment
from RecommendationSystem.DB.utils import get_all_article, get_all_comments_for_given_article


class Model(AbstractModel):
    """
    Recommendation model to extract the recommendations from the database.
    """
    def __init__(self):
        self.model = SentenceTransformer("stsb-roberta-base-v2")

    def get_recommendations(self, comment_data: dict) -> List[str]:
        """
        Interface method for the REST API view
        :param comment_data: Dict with all information the model needs to extract the recommendations from the database
        :return: List of recommendations
        """
        if len(comment_data.keys()) == 0:
            return []

        # Add model here
        article_candidates = self.__find_article_candidates(comment_data["keywords"])

        return self.__get_comments_for_article(article_candidates)[:6]

    def __find_article_candidates(self, keywords) -> list[Article]:
        keyword_embeddings = self.model.encode(keywords, convert_to_tensor=True)
        all_article: List[Article] = get_all_article()

        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        candidates = []
        for article in all_article:
            score = cos(torch.Tensor(article.embedding), keyword_embeddings)
            candidates.append([article, score])
        candidates.sort(key=lambda x: x[1], reverse=True)
        print([candidate[1] for candidate in candidates[:5]])
        return [candidate[0] for candidate in candidates[:3]]

    def __get_comments_for_article(self, articles: List[Article]) -> List[Comment]:
        candidates = []
        for article in articles:
            comments = get_all_comments_for_given_article(article)
            for comment in comments:
                if comment.up_votes is not None:
                    candidates.append({"comment": comment, "article": article})
        candidates.sort(key=lambda x: x["comment"].up_votes, reverse=True)
        return [[candidate["comment"].text, candidate["article"].news_agency, candidate["article"].article_title,
                 candidate["article"].url] for candidate in candidates[:6]]