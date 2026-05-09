"""匹配决策 Agent — 规则初筛 + RAG 检索 + LLM 打分"""
import yaml
import json
from pathlib import Path
from llm_client import LLMClient
from rag import RAGRetriever

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_match_config = _config['matching']

_PROMPT_PATH = Path(__file__).parent / 'data' / 'prompts' / 'match_scoring.txt'
with open(_PROMPT_PATH, 'r', encoding='utf-8') as f:
    _MATCH_PROMPT_TEMPLATE = f.read()

_SUBJECTS_PATH = Path(__file__).parent / 'data' / 'subjects.json'
with open(_SUBJECTS_PATH, 'r', encoding='utf-8') as f:
    _SUBJECTS = json.load(f)


class MatchAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.rag = RAGRetriever()

    def match(self, demand, candidates):
        """执行 AI 匹配
        Args:
            demand: dict — 需求信息 (subject, grade, location, budget, time_slots, description, requirements, tags)
            candidates: list[dict] — 候选家教列表, 每个 dict 含 id, real_name, school, major, skills, teaching_exp,
                        introduction, location, available_time, hourly_rate, verification_status
        Returns:
            list[dict] — [{tutor_id, total_score, subject_match, experience_match, location_time_match, value_match, reason}, ...]
        """
        top_n = _match_config.get('top_n', 5)

        # 1. RAG 检索 — 获取学科知识点作为上下文
        subject = demand.get('subject', '')
        grade = demand.get('grade', '')
        query = f"{subject} {grade} 家教 辅导"
        rag_docs = self.rag.search(query, top_k=5)

        knowledge_points = []
        if subject in _SUBJECTS:
            for level, points in _SUBJECTS[subject].items():
                knowledge_points.append(f"- {level}: {', '.join(points)}")

        # 2. 构造候选家教文本
        candidates_text = []
        for i, t in enumerate(candidates):
            skills = ', '.join(t.get('skills', [])) if isinstance(t.get('skills'), list) else t.get('skills', '')
            available = t.get('available_time', '')
            if isinstance(available, list):
                available = '; '.join(available)
            candidates_text.append(
                f"[{t.get('id')}] {t.get('real_name', '未知')} | "
                f"学校: {t.get('school', '')} | 专业: {t.get('major', '')} | "
                f"学历: {t.get('education', '')} | 年级: {t.get('grade', '')} | "
                f"技能: {skills} | "
                f"教学经验: {t.get('teaching_exp', 0)}年 | "
                f"地区: {t.get('location', '')} | "
                f"可用时间: {available} | "
                f"时薪: {t.get('hourly_rate', 0)}元 | "
                f"简介: {t.get('introduction', '')}"
            )

        rag_context = '\n'.join(
            f"[RAG {d['distance']:.3f}] {d['text'][:200]}" for d in rag_docs
        )

        # 3. 构造 Prompt
        user_prompt = _MATCH_PROMPT_TEMPLATE.format(
            subject=subject,
            grade=grade,
            location=demand.get('location', ''),
            budget=demand.get('budget', 0),
            time_slots=json.dumps(demand.get('time_slots', []), ensure_ascii=False),
            requirements=demand.get('requirements', '无'),
            description=demand.get('description', ''),
            knowledge_points='\n'.join(knowledge_points),
            candidates='\n'.join(candidates_text)
        )

        system_prompt = f"你是一个家教匹配专家。结合以下 RAG 知识库参考信息辅助判断：\n{rag_context}"

        # 4. LLM 调用
        result = self.llm.chat_json(system_prompt, user_prompt)

        # 5. 取 top_n
        if isinstance(result, list):
            return result[:top_n]
        return []
