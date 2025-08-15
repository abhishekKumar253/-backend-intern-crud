from fastapi import FastAPI
from src.database import engine, Base
from src.routers import users,posts, likes, comments

app = FastAPI(title="LawVriksh Blog API")

Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(comments.router)

@app.get("/")
def root():
    return {"message": "Welcome to the LawVriksh Blog API"}