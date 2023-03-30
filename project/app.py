from dotenv import load_dotenv

load_dotenv()

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from absl import logging

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils import time_cache
from .scraping.common import ScrapedLink

logging.set_verbosity(logging.INFO)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
templates = Jinja2Templates(directory="project/templates")
app.mount("/static", StaticFiles(directory="project/static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/logs/")
async def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.save_log(db=db, log=log)


@app.get("/logs/{log_id}", response_model=schemas.Log)
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


def write_notification(message=""):
    httpx.post(f"https://ntfy.sh/thornewolf", data={"message": message})


@app.post("/notify/")
async def send_notification(
    message: str,
    background_tasks: BackgroundTasks,
):
    """
    Notify the developer of any issues with the service
    """
    background_tasks.add_task(write_notification, message=message)
    return {"message": "Notification sent in the background"}


@app.get("/articles/", summary="Get articles")
async def articles(sources="", word_filter: str | None = None) -> list[ScrapedLink]:
    """
    Fetch article titles and links from various sources.

    - **sources**: Comma-separated list of sources to fetch from. If empty, fetch from all sources.
    - **word_filter**: Filter results by word. Only articles with this word in the title will be returned.

    The following sources are available:

    `skimfeed,68k,cnn,cbc`
    """
    from .scraping import skimfeed, _68k, cnn, cbc

    if sources == "":
        sources = "skimfeed,68k,cnn,cbc"
    sources = sources.split(",")
    result = []
    for source in sources:
        if source == "skimfeed":
            result += skimfeed.scrape_skimfeed()
        elif source == "68k":
            result += _68k.scrape_68k()
        elif source == "cnn":
            result += cnn.scrape_cnn()
        elif source == "cbc":
            result += cbc.scrape_cbc()
    if word_filter:
        result = [
            result for result in result if word_filter.lower() in result.title.lower()
        ]
    return list(set(result))
