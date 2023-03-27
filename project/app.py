from dotenv import load_dotenv

load_dotenv()

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


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
    background_tasks.add_task(write_notification, message=message)
    return {"message": "Notification sent in the background"}
