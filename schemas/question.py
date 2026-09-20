from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuestionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1)
    category_id: int | None = None

class QuestionResponse(BaseModel):
    id: int
    title: str
    text: str
    category_id: int | None
    category: CategoryResponse | None = None
    model_config = ConfigDict(from_attributes=True)
