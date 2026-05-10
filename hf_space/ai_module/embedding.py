"""本地 embedding 模块 — 使用 BAAI/bge-small-zh-v1.5"""
import yaml
import os
from pathlib import Path

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_model_name = _config['embedding']['model']
_device = _config['embedding'].get('device', 'cpu')

_encoder = None

def _get_encoder():
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer
        _encoder = SentenceTransformer(_model_name, device=_device)
    return _encoder

def embed(texts):
    """文本列表 → 向量列表
    Args:
        texts: str or list[str]
    Returns:
        list[list[float]]
    """
    if isinstance(texts, str):
        texts = [texts]
    encoder = _get_encoder()
    embeddings = encoder.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
