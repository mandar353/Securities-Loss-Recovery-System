from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.upload import router as upload_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(upload_router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})