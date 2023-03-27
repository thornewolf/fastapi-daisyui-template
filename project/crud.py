from sqlalchemy.orm import Session

from . import models, schemas


def save_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_log(db: Session, log_id: int):
    return db.query(models.Log).filter(models.Log.id == log_id).first()
