from fastapi import FastAPI, Depends, HTTPException #type:ignore
from sqlmodel import Session #type:ignore
from database import init_db, engine
from crud import (
    create_short_url,
    get_original_url,
    update_short_url,
    delete_short_url,
    increment_access_count,
)
from models import URL

app = FastAPI()

# Dependency
def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/shorten/")
def shorten_url(original_url: str, short_url: str, db: Session = Depends(get_session)):
    existing = get_original_url(db, short_url)
    if existing:
        raise HTTPException(status_code=400, detail="Short URL already exists")
    return create_short_url(db, original_url, short_url)

@app.get("/get/")
def redirect_to_url(short_url: str, db: Session = Depends(get_session)):
    url_entry = increment_access_count(db, short_url)
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url_entry.original_url}

@app.put("/update/")
def update_url(short_url: str, new_short_url: str, db: Session = Depends(get_session)):
    return update_short_url(db, short_url, new_short_url)

@app.delete("/delete/")
def delete_url(short_url: str, db: Session = Depends(get_session)):
    return delete_short_url(db, short_url)

@app.get("/stat/")
def get_url_stats(short_url: str, db: Session = Depends(get_session)):
    url_entry = get_original_url(db, short_url)
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url_entry.original_url, "accessed_count": url_entry.accessed_count}
