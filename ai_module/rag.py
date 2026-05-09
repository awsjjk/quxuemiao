"""ChromaDB 向量检索 + 知识库管理"""
import yaml
import chromadb
from pathlib import Path
from embedding import embed

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_rag_config = _config['rag']
_persist_dir = Path(__file__).parent / _rag_config['persist_dir']
_collection_name = _rag_config['collection_name']
_top_k = _rag_config.get('top_k', 10)

_client = chromadb.PersistentClient(path=str(_persist_dir))


class RAGRetriever:

    def __init__(self):
        self.collection = _client.get_or_create_collection(
            name=_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def search(self, query, top_k=None):
        """向量检索 — 返回最相关的 top_k 个文档
        Args:
            query: str — 查询文本
            top_k: int — 返回数量
        Returns:
            list[dict] — [{id, text, metadata, distance}, ...]
        """
        if top_k is None:
            top_k = _top_k
        query_vec = embed(query)
        results = self.collection.query(
            query_embeddings=query_vec,
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        docs = []
        ids = results.get('ids', [[]])[0]
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]
        for i in range(len(ids)):
            docs.append({
                'id': ids[i],
                'text': documents[i] if documents else '',
                'metadata': metadatas[i] if metadatas else {},
                'distance': distances[i] if distances else 0
            })
        return docs


class KnowledgeBase:

    def __init__(self):
        self.collection = _client.get_or_create_collection(
            name=_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, doc_id, text, metadata=None):
        vec = embed(text)
        self.collection.add(
            ids=[doc_id],
            embeddings=vec,
            documents=[text],
            metadatas=[metadata or {}]
        )

    def add_batch(self, items):
        """items: [(doc_id, text, metadata), ...]"""
        if not items:
            return
        ids = [it[0] for it in items]
        texts = [it[1] for it in items]
        vecs = embed(texts)
        metas = [it[2] if len(it) > 2 else {} for it in items]
        self.collection.add(
            ids=ids,
            embeddings=vecs,
            documents=texts,
            metadatas=metas
        )

    def delete(self, doc_id):
        self.collection.delete(ids=[doc_id])

    def count(self):
        return self.collection.count()
