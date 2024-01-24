import os

import torch
from sentence_transformers import SentenceTransformer

from RecommendationSystem.Embedder.abstract_embedding_model import AbstractEmbeddingModel


class EmbeddingModel(AbstractEmbeddingModel):
    def __init__(self):
        self.model = SentenceTransformer("stsb-roberta-base-v2")

    def embed(self, text: str) -> torch.Tensor:
        """
        Computes the vector representation of the given text
        :param text: Text that should be embedded
        :return: Torch tensor with embedding of the given text
        """
        embedding_vector = self.model.encode(text, convert_to_tensor=True)
        # Implement embedding method here

        return embedding_vector