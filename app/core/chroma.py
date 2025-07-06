import chromadb
from chromadb.utils import embedding_functions
from app.core.config import CHROMA_PATH, COLLECTION_NAME, EMBED_MODEL

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
