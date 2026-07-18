from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine
import models
import schemas
from auth import create_access_token, verify_token



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB Dependency
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


#Login API
@app.post("/login")
def login():
    return {
        "access_token": create_access_token({"user": "admin"}),
        "token_type": "bearer"
    }    



# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the first page Home Blog API!"}




#create Blog (protected route)
@app.post("/blogs/", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = models.Blog(title=blog.title, content=blog.content, author=blog.author)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#Read all blogs (protected route)
@app.get("/blogs/")
def get_blogs(page: int = 1,
              limit: int = 5,
              search: str = Query(default=""),
              db: Session = Depends(get_db), user = Depends(verify_token)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))
    total = query.count()
    start = (page - 1) * limit
    blogs = query.offset(start).limit(limit).all()
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "blogs": blogs
    }


#Read a single blog by ID (protected route)
@app.get("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db), user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

#update a blog by ID (protected route)
@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, updated_blog: schemas.BlogCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog.title = updated_blog.title
    blog.content = updated_blog.content
    blog.author = updated_blog.author
    db.commit()
    db.refresh(blog)
    return blog

#delete a blog by ID (protected route)
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
