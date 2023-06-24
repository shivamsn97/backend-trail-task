from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from database import InMemoryDB
from feedgen.feed import FeedGenerator

app = FastAPI()
db = InMemoryDB()

@app.get("/")
async def root():
    return {"status": "ok"}

from fastapi import HTTPException

from fastapi import Request, HTTPException

@app.post("/submit")
async def submit(request: Request, submission: dict):
    title = submission.get('title')
    author = submission.get('author')
    text = submission.get('text')
    url = submission.get('url')
    if not title or not author or not text or not url:
        raise HTTPException(status_code=422, detail="Missing required fields")
    submitted_by = request.headers.get('User-Agent')
    sub = db.add_submission(title, author, text, url, submitted_by)
    return JSONResponse({"status": "ok", "submission": sub.as_dict()}, status_code=201)

@app.get("/search")
async def search(title: str|None = None, author: str|None = None, size: int = 50):
    subs = db.search_submissions(title, author, size)
    return [s.as_dict() for s in subs]
    
@app.get("/item/{id}")
async def item(id: int):
    sub = db.get_submission(id)
    if not sub:
        return {"status": "not found"}, 404
    return sub.as_dict(full = True)

@app.get("/rss")
async def rss(title: str|None = None, author: str|None = None, size: int = 50):
    subs = db.search_submissions(title, author, size)
    feed = FeedGenerator()
    feed.title('RSS feed')
    feed.description('This is a RSS feed')
    feed.link(href='http://localhost:8000/rss', rel='self')
    for s in subs:
        entry = feed.add_entry()
        entry.id(s.url)
        entry.title(s.title)
        entry.author(name=s.author)
        entry.link(href=s.url)
        entry.pubDate(s.created_at)
    return Response(content=feed.rss_str(pretty=True), media_type="application/rss+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

