from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

app = FastAPI(
    title = "Bookmark API",
    description = "First REST API - Phase 1",
    version= "0.1.0",
)
# what a bookmark looks like using pydantic
class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str
    description: Optional[str] = None

class BookmarkResponse(BookmarkCreate):
    id: int

# Fake database
bookmarks_db = {}
current_id = 1

@app.get("/")
def home():
    return {"message": "Bookmark API is running"}
@app.get("/health")
def health():
    return {"status": "ok"}

# The CRUD endpoints
@app.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(bookmark: BookmarkCreate):
    global current_id
    new_bookmark = {
        "id": current_id,
        "url": str(bookmark.url),
        "title": bookmark.title,
        "description": bookmark.description
    }
    bookmarks_db[current_id] = new_bookmark
    current_id += 1
    return new_bookmark

@app.get("/bookmarks", response_model=List[BookmarkResponse])
def get_all_bookmarks():
    return list(bookmarks_db.values())

@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
def get_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks_db:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks_db[bookmark_id]

@app.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks_db:
        raise HTTPException(status_code=404, detail= "Bookmark not found")
    del bookmarks_db[bookmark_id]
    return None