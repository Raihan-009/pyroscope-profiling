from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import pyroscope
import os

from app.database import engine, SessionLocal
from app import models, schemas, crud

# Initialize Pyroscope profiling
pyroscope.configure(
    application_name=os.getenv("PYROSCOPE_APP_NAME", "fastapi-app"),
    server_address=os.getenv("PYROSCOPE_SERVER", "http://pyroscope:4040"),
    tags={
        "environment": os.getenv("ENVIRONMENT", "development"),
        "language": "python",
        "app": "fastapi",
    },
    enable_logging=True,
)

app = FastAPI(
    title="FastAPI Pyroscope Profiling Demo",
    description="A FastAPI application with PostgreSQL and Pyroscope profiling",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Pyroscope Profiling Demo",
        "endpoints": {
            "health": "/health",
            "users": "/users",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "pyroscope": "configured"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)
    return {"message": "User deleted successfully"}


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
async def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    """Create a post for a specific user"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all posts with pagination"""
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/compute/fibonacci/{n}")
async def compute_fibonacci(n: int):
    """Compute Fibonacci number - CPU intensive task for profiling"""
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    if n > 40:
        raise HTTPException(status_code=400, detail="n must be <= 40 to prevent timeout")
    
    def fibonacci(num):
        if num <= 1:
            return num
        return fibonacci(num - 1) + fibonacci(num - 2)
    
    result = fibonacci(n)
    return {"n": n, "fibonacci": result, "message": "CPU intensive computation completed"}


@app.get("/compute/sum/{n}")
async def compute_sum(n: int):
    """Compute sum of numbers - CPU intensive task for profiling"""
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    if n > 10000000:
        raise HTTPException(status_code=400, detail="n must be <= 10000000")
    
    total = sum(range(n + 1))
    return {"n": n, "sum": total, "message": "Computation completed"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

