import numpy as np
from InstructorEmbedding import INSTRUCTOR


# HOW EMBEDDINGS WORK (in a nutshell)
# an embedding function takes a string and then figures out how to represent the meaning of that string as a vector. A vector is just a bunch of floating-point numbers. If we had a vector that had 2 values then that would be a point on a cartesian plane. If the vector had 3 values it would be a point in 3 dimensional space. Our "meaning vectors" have quite a lot of dimensions.
# once we have the "meanings" of multiple sentences as vectors we can calculate the distance between them. If they are close together then they mean the same thing. If they are far apart they mean different things.


_embedding_model = INSTRUCTOR("hkunlp/instructor-large", device="cpu")
embedding_function = lambda texts: _embedding_model.encode(texts).tolist()


# distance calculation functions shamelessly lifted from chromadb
# https://github.com/chroma-core/chroma.git
# chromadb/test/property/invariants.py
NORM_EPS = 1e-30
distance_functions = {
    "l2": lambda x, y: np.linalg.norm(x - y) ** 2,  # type: ignore
    "cosine": lambda x, y: 1 - np.dot(x, y) / ((np.linalg.norm(x) + NORM_EPS) * (np.linalg.norm(y) + NORM_EPS)),  # type: ignore
    "ip": lambda x, y: 1 - np.dot(x, y),  # type: ignore
}


def similarity_distance(sentence1: str, sentence2: str) -> float:
    """Get the distance between two vectors representing the meaning of two sentences"""
    embedding1 = np.array(embedding_function(sentence1))
    embedding2 = np.array(embedding_function(sentence2))
    return distance_functions["l2"](embedding1, embedding2)
