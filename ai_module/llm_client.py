"""统一 LLM 调用接口 — 读取 config.yaml 配置"""
import yaml
import json
from pathlib import Path
from openai import OpenAI

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_llm_config = _config['llm']
_client = OpenAI(
    api_key=_llm_config['api_key'],
    base_url=_llm_config['base_url']
)
_model = _llm_config['model']
_temperature = _llm_config.get('temperature', 0.3)
_max_tokens = _llm_config.get('max_tokens', 2000)


class LLMClient:

    def chat(self, system_prompt, user_prompt, response_format=None):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        kwargs = dict(
            model=_model,
            messages=messages,
            temperature=_temperature,
            max_tokens=_max_tokens
        )
        if response_format == 'json':
            kwargs['response_format'] = {"type": "json_object"}

        response = _client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def chat_json(self, system_prompt, user_prompt):
        text = self.chat(system_prompt, user_prompt, response_format='json')
        return json.loads(text)
