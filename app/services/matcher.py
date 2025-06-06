import os
import pandas as pd
from sentence_transformers import util
from app.utils.helpers import (
    get_embedding,
    extract_skills,
    get_resume_embeddings,
    get_feedback_via_gemini,
)
from app.core.skills_list import SKILLS


def run_resume_match_pipeline(job_description_text: str, resume_folder: str = "resumes"):
    job_skills = extract_skills(job_description_text, SKILLS)
    job_description_embeddings = get_embedding(job_description_text)
    resume_files = [f for f in os.listdir(resume_folder) if f.endswith(".pdf")]
    results = []
    for resume_file in resume_files:
        resume_path = os.path.join(resume_folder, resume_file)
        resume_embeddings, resume_cleaned_text = get_resume_embeddings(
            resume_path)
        resume_skills = extract_skills(resume_cleaned_text, SKILLS)
        matched_skills = resume_skills & job_skills
        missing_skills = job_skills - resume_skills
        similarity_score = util.pytorch_cos_sim(
            resume_embeddings, job_description_embeddings).item()
        feedback = get_feedback_via_gemini(
            resume_cleaned_text, job_description_text)
        results.append({
            "candidate": resume_file,
            "match_score": round(similarity_score, 2),
            "skills_matched": ", ".join(matched_skills).title() or "None",
            "skills_missing": ", ".join(missing_skills).title() or "None",
            "feedback": feedback.replace("*", "")
        })
    df_results = pd.DataFrame(results)
    return df_results.sort_values(by="match_score", ascending=False)
