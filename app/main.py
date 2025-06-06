from fastapi import FastAPI
from app.api.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Resume Matcher API",
    version="1.0.0",
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
