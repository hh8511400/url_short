from sqlmodel import SQLModel, create_engine  #type:ignore

DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
# init_db()