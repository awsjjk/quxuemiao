import json
import yaml
import numpy as np
import requests
from pathlib import Path
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

ai_assistant_bp = Blueprint('ai_assistant', __name__)

_CONFIG_PATH = Path(__file__).parent.parent.parent / 'ai_assistant_config.yaml'
with open(_CONFIG_PATH, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_FAQ_PATH = Path(__file__).parent.parent.parent / _config['faq']['faq_data_path']
with open(_FAQ_PATH, 'r', encoding='utf-8') as f:
    _faq_list = json.load(f)

_threshold = _config['faq']['similarity_threshold']

_llm_cfg = _config['llm']
_api_url = f"{_llm_cfg['base_url']}/v1/chat/completions"
_api_key = _llm_cfg['api_key']
_model = _llm_cfg['model']
_temperature = _llm_cfg.get('temperature', 0.1)
_max_tokens = _llm_cfg.get('max_tokens', 300)
_top_p = _llm_cfg.get('top_p', 0.9)


SYSTEM_PROMPT = (
    "你是趣学喵家教平台的AI客服助手。你只回答与平台使用、家教服务、学习辅导相关的问题。"
    "如果用户询问无关话题（如编程、娱乐、政治等），请礼貌回复："
    "'抱歉，我只擅长解答平台使用和家教相关的问题，您可以尝试其他问题。'"
    "回复使用中文，不超过200字，不使用Markdown格式和代码块。"
)


def _embed_text(text):
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'ai_module'))
    from embedding import embed
    return embed(text)[0]


def _call_llm(user_message):
    resp = requests.post(
        _api_url,
        headers={
            "Authorization": f"Bearer {_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": _model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "temperature": _temperature,
            "max_tokens": _max_tokens,
            "top_p": _top_p
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


@ai_assistant_bp.route('/faq_list', methods=['GET'])
@jwt_required()
def faq_list():
    faqs = [{"id": f["id"], "question": f["question"], "category": f["category"]} for f in _faq_list]
    return jsonify({"code": 200, "data": faqs}), 200


@ai_assistant_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({"code": 400, "msg": "消息不能为空"}), 400

    faq_id = data.get('faq_id', '').strip()
    if faq_id:
        for faq in _faq_list:
            if faq['id'] == faq_id:
                return jsonify({
                    "code": 200,
                    "data": {"reply": faq['answer'], "source": "faq_click", "faq_id": faq_id}
                }), 200

    user_vec = _embed_text(user_message)
    best_score = -1
    best_faq = None
    for faq in _faq_list:
        question_vec = _embed_text(faq['question'])
        score = np.dot(user_vec, question_vec)
        if score > best_score:
            best_score = score
            best_faq = faq

    if best_score >= _threshold and best_faq:
        return jsonify({
            "code": 200,
            "data": {"reply": best_faq['answer'], "source": "faq_match", "faq_id": best_faq['id'], "score": float(best_score)}
        }), 200

    try:
        reply = _call_llm(user_message)
        return jsonify({
            "code": 200,
            "data": {"reply": reply, "source": "llm"},
        }), 200
    except Exception as e:
        return jsonify({
            "code": 200,
            "data": {"reply": "抱歉，我暂时无法处理您的问题，请稍后再试或联系人工客服。", "source": "error"}
        }), 200
