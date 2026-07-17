from pydantic import BaseModel


#Input Schemas
class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

#Output Schemas
class BlogResponse(BlogCreate):
    id: int
    title: str
    content: str
    author: str

    class Config:
        from_attributes = True
