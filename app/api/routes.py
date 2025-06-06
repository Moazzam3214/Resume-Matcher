from fastapi.responses import FileResponse
from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import File
import shutil
import os
import pandas as pd
from app.services.matcher import run_resume_match_pipeline
from app.utils.helpers import save_results_to_excel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/match")
async def match_resumes(
    request: Request,
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...)
):
    # Save uploaded resumes
    os.makedirs("resumes", exist_ok=True)
    for resume in resumes:
        file_path = f"resumes/{resume.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)

    # Run pipeline
    results_df = run_resume_match_pipeline(
        job_description, resume_folder="resumes")
    save_results_to_excel(results_df)

    # Convert DataFrame to list of dicts for template rendering
    results = results_df.to_dict(orient="records")
    columns = list(results_df.columns)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Matching complete! Results saved to ranked_resumes.xlsx.",
        "results": results,
        "columns": columns
    })

# Route to download the Excel file


@router.get("/download")
async def download_excel():
    file_path = "ranked_resumes.xlsx"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="ranked_resumes.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return {"error": "File not found. Please run a match first."}
