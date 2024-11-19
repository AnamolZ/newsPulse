from pydantic import BaseModel

class NewsItem(BaseModel):
    image: str
    heading: str
    heading_text: str
    short_view: str
