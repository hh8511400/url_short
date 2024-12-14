from sqlmodel import Session, select #type:ignore
from models import URL

def create_short_url(db: Session, original_url: str, short_url: str):
    url_entry = URL(original_url=original_url, short_url=short_url)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)
    return url_entry

def get_original_url(db: Session, short_url: str):
    return db.exec(select(URL).where(URL.short_url == short_url)).first()

def update_short_url(db: Session, short_url: str, new_short_url: str):
    url_entry = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if url_entry:
        url_entry.short_url = new_short_url
        db.commit()
        db.refresh(url_entry)
    return url_entry

def delete_short_url(db: Session, short_url: str):
    url_entry = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if url_entry:
        db.delete(url_entry)
        db.commit()
    return url_entry

def increment_access_count(db: Session, short_url: str):
    url_entry = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if url_entry:
        url_entry.accessed_count += 1
        db.commit()
        db.refresh(url_entry)
    return url_entry
