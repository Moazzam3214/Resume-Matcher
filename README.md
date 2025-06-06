# Resume Matcher 🚀

An AI-powered web application that matches candidate resumes to job descriptions using advanced NLP, semantic similarity, and LLM feedback. Upload resumes and a job description to instantly get ranked matches, skill analysis, and actionable feedback—all in a beautiful web interface.

---

## 🎯 Features

- **AI-Powered Resume Matching:** Uses sentence embeddings and semantic similarity to rank resumes against job descriptions.
- **Skill Extraction:** Identifies and matches technical and soft skills using spaCy and custom skill lists.
- **LLM Feedback:** Integrates Google Gemini to provide concise, actionable resume feedback.
- **Batch Resume Upload:** Upload multiple PDF resumes at once for bulk matching.
- **Excel Export:** Download ranked results as an Excel file for further analysis.
- **Modern Web Interface:** FastAPI backend with a Tailwind CSS-powered frontend.

---

## 📁 Project Structure

```
resume-matcher/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint
│   ├── api/
│   │   └── routes.py            # API and web routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Environment and API key config
│   │   └── skills_list.py       # List of skills for matching
│   ├── services/
│   │   ├── __init__.py
│   │   └── matcher.py           # Resume matching pipeline
│   ├── static/
│   │   └── styles.css           # (Optional) Custom styles
│   ├── templates/
│   │   └── index.html           # Jinja2 web template
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # NLP, skill extraction, Excel export
├── .gitignore
├── requirements.txt
├── expirements.ipynb            # Experiments and prototyping
```

---

## 🛠️ Installation

Clone the repository:

```sh
git clone https://github.com/moazzam3214/resume-matcher.git
cd resume-matcher
```

Create a virtual environment (recommended):

```sh
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Download spaCy model:

```sh
python -m spacy download en_core_web_sm
```

Set up your `.env` file with your Google Gemini API key:

```
GOOGLE_API_KEY=your-gemini-api-key
```

---

## 🚀 Quick Start

### Using the Web Application

Run the FastAPI app:

```sh
uvicorn app.main:app --reload
```

Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

- Paste a job description and upload one or more PDF resumes.
- Click "Match Resumes" to see ranked results, skill matches, and LLM feedback.
- Download the results as an Excel file.

---

## 🧠 How It Works

- **Skill Extraction:** Uses spaCy PhraseMatcher and semantic similarity to extract and match skills from resumes and job descriptions.
- **Semantic Matching:** Computes cosine similarity between sentence embeddings (via Sentence Transformers) of resumes and job descriptions.
- **LLM Feedback:** Sends resume and job description to Gemini for brief, actionable feedback.
- **Excel Export:** Results are saved as `ranked_resumes.xlsx` for download.

---

## 🎮 Usage Example (Python)

You can use the core pipeline directly in Python:

```python
from app.services.matcher import run_resume_match_pipeline

job_description = open("job.txt").read()
results_df = run_resume_match_pipeline(job_description, resume_folder="resumes")
print(results_df)
```

---

## 📋 Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- spaCy (`en_core_web_sm`)
- sentence-transformers
- openpyxl
- pandas
- google-generativeai
- Jinja2

See `requirements.txt` for details.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

**Areas for Improvement:**

- Add more advanced skill extraction (NER, custom models)
- Support for DOCX resumes
- Add authentication and user management
- Improve LLM prompt engineering
- Add REST API endpoints for programmatic access

---

## 📈 Future Enhancements

- Multi-language support
- Customizable skill lists per job
- Real-time feedback and analytics dashboard
- Integration with ATS and HR platforms
- Enhanced LLM feedback with scoring

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [spaCy](https://spacy.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Gemini](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- Open source community

---

## 📞 Contact

GitHub: [@Moazzam3214](https://github.com/Moazzam3214)
Email: moazzamaleem786@gmail.com
LinkedIn: [Muhammad Moazzam](https://www.linkedin.com/in/muhammad-moazzam-492b0724b/)

⭐ Star this repository if you found it helpful!

Made with ❤️ and lots of ☕
