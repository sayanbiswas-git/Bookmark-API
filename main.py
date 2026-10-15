from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from google import genai 
import os 
from dotenv import load_dotenv

load_dotenv()

# Gimini AI setup 
GIMINI_API_KEY = os.getenv("GIMINI_API_KEY")
ai_client = genai.Client(api_key=GIMINI_API_KEY)

# Database Setup 
SQLALCHEMY_DATABASE_URL = "sqlite:///./bookmarks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookmarkDB(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    ai_summary = Column(Text, nullable=True)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = "Bookmark API",
    description = "First REST API - Phase 1",
    version= "0.2.0",
)

# what a bookmark looks like using pydantic
class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str
    description: Optional[str] = None

class BookmarkResponse(BookmarkCreate):
    id: int
    ai_summary: Optional[str] = None 
    class Config:
        from_attributes = True

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Bookmark API is running"}
@app.get("/health")
def health():
    return {"status": "ok"}

# The CRUD endpoints
@app.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(bookmark: BookmarkCreate, db: Session = Depends(get_db)):
    try:
        prompt =( 
            f"Generate a single, concice one-sentence summary for a bookmark "
            f"with the title '{bookmark.title}' and URL '{bookmark.url}'."
            f"Return only the summary, no extra text."
        )
        ai_response = ai_client.models.generate_content(
            model = "gemini-3.8-flash",
            contents = prompt,
        )
        ai_summary = ai_response.text.strip() if ai_response.text else None
    except Exception as e:
        print(f"Gimini api error: {e}")
        ai_summary = None

    new_bookmark = BookmarkDB(
        url= str(bookmark.url),
        title= bookmark.title,
        description= bookmark.description,
        ai_summary= ai_summary
    )
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

 
@app.get("/bookmarks", response_model=List[BookmarkResponse])
def get_all_bookmarks(db: Session = Depends(get_db)):
    return db.query(BookmarkDB).all()

@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.query(BookmarkDB).filter(BookmarkDB.id == bookmark_id).first()
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark

@app.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.query(BookmarkDB).filter(BookmarkDB.id == bookmark_id).first()
    if bookmark is None:
        raise HTTPException(status_code=404, detail= "Bookmark not found")
    db.delete(bookmark)
    db.commit()
    return None