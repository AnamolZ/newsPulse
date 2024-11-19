from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.news_fetcher import fetch_news_content
from app.services.image_handler import save_image
from app.services.social_media import post_to_instagram, post_to_facebook
import os

# FastAPI app setup
app = FastAPI()

# CORS setup for frontend communication
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fetch-and-post")
async def fetch_and_post():
    news_data = fetch_news_content()
    if news_data:
        image_url = news_data['image_link']
        message = news_data['summarized_content']

        thumbnail_path = save_image(image_url)
        if thumbnail_path:
            post_to_facebook(os.getenv('PAGE_ID'), os.getenv('FACEBOOK_ACCESS_TOKEN'), thumbnail_path, message)
            post_to_instagram(os.getenv('INSTAGRAM_ID'), os.getenv('INSTAGRAM_ACCESS_TOKEN'), image_url, message)
            return {"message": "Post Has Been Posted!"}
        else:
            return {"error": "Failed to download image."}
    else:
        return {"error": "Failed to fetch news data."}
