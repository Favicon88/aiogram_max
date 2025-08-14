from pydantic import BaseModel, Field


class Image(BaseModel):
    url: str = Field(description="URL изображения")
