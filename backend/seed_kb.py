"""将学科知识点向量化写入 ChromaDB"""
import sys
import os

# 确保 ai_module 在路径中
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_module'))

from ai_module.rag import KnowledgeBase

kb = KnowledgeBase()

# 学科知识点文档 — 用于 RAG 检索增强匹配上下文
docs = [
    ("subj_math_primary", "小学数学知识点：四则运算、分数与小数、几何初步、应用题解题技巧、逻辑思维训练", {"subject": "数学", "grade": "小学"}),
    ("subj_math_junior", "初中数学知识点：代数基础、几何证明、函数入门、方程与不等式、统计与概率", {"subject": "数学", "grade": "初中"}),
    ("subj_math_senior", "高中数学知识点：函数与导数、解析几何、数列与极限、概率统计、向量与立体几何", {"subject": "数学", "grade": "高中"}),
    ("subj_eng_primary", "小学英语知识点：字母与发音、基础词汇、简单对话、自然拼读、绘本阅读", {"subject": "英语", "grade": "小学"}),
    ("subj_eng_junior", "初中英语知识点：语法体系、完形填空、阅读理解、书面表达、听力训练", {"subject": "英语", "grade": "初中"}),
    ("subj_eng_senior", "高中英语知识点：高级语法、长难句分析、写作模板、翻译技巧、真题训练", {"subject": "英语", "grade": "高中"}),
    ("subj_chn_primary", "小学语文知识点：拼音与识字、阅读理解、作文基础、古诗词背诵、成语故事", {"subject": "语文", "grade": "小学"}),
    ("subj_chn_junior", "初中语文知识点：文言文阅读、现代文阅读、议论文写作、语法修辞、名著导读", {"subject": "语文", "grade": "初中"}),
    ("subj_chn_senior", "高中语文知识点：文言文翻译、论述文写作、诗歌鉴赏、文学常识、语言文字运用", {"subject": "语文", "grade": "高中"}),
    ("subj_phy_junior", "初中物理知识点：力学基础、电学入门、光学、热学、声现象", {"subject": "物理", "grade": "初中"}),
    ("subj_phy_senior", "高中物理知识点：牛顿力学、电磁学、热力学、光学与原子物理、实验专题", {"subject": "物理", "grade": "高中"}),
    ("subj_chem_junior", "初中化学知识点：物质构成、化学方程式、溶液、酸碱盐、金属活动性", {"subject": "化学", "grade": "初中"}),
    ("subj_chem_senior", "高中化学知识点：物质结构、化学反应原理、有机化学、电化学、化学实验", {"subject": "化学", "grade": "高中"}),
]

kb.add_batch(docs)
print(f"知识库初始化完成，共 {kb.count()} 条记录")
