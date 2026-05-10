from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)


def embedding_agent(text):

    embedding = model.encode(text)

    return embedding