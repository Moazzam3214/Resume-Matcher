from app.core.skills_list import SKILLS
import re
import spacy
import pymupdf
import openpyxl
from openpyxl.styles import Font
import google.generativeai as genai
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

patterns = [nlp(skill) for skill in SKILLS]
matcher.add("SKILLS", patterns)


def extract_text_from_pdf(pdf_path: str):
    text = ""
    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def clean_text(text: str):
    return re.sub(r'\s+', ' ', text.lower()).strip()


def get_embedding(text: str):
    return model.encode(text, convert_to_tensor=True)


def get_resume_embeddings(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    return get_embedding(cleaned_text), cleaned_text


def extract_skills(text: str, skill_list=SKILLS):
    return set(skill for skill in skill_list if skill in text.lower())


def extract_skills_with_matcher(text):
    doc = nlp(text.lower())
    matches = matcher(doc)
    return set(doc[start:end].text.lower() for _, start, end in matches)


def semantic_skill_match(text, skills, threshold=0.6):
    text_embedding = model.encode(text, convert_to_tensor=True)
    matched = set()
    for skill in skills:
        skill_embedding = model.encode(skill, convert_to_tensor=True)
        if util.cos_sim(text_embedding, skill_embedding).item() > threshold:
            matched.add(skill)
    return matched


def extract_skills_combined(text, all_skills=SKILLS, threshold=0.6):
    exact_matches = extract_skills_with_matcher(text)
    semantic_matches = semantic_skill_match(
        text, set(all_skills) - exact_matches, threshold)
    return exact_matches.union(semantic_matches)


def get_feedback_via_gemini(resume_text, job_text):
    prompt = f"""
You are an AI resume reviewer. The job description is:

{job_text}

The resume content is:

{resume_text}

in 2-3 sentences, provide feedback on the resume.
Keep it brief and useful.
"""
    response = genai.GenerativeModel(
        "gemini-1.5-flash-latest").generate_content(prompt)
    return response.text


def save_results_to_excel(df, filename="ranked_resumes.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resume Ranking"
    headers = list(df.columns)
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in df.itertuples(index=False):
        ws.append(list(row))
    wb.save(filename)
