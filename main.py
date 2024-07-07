import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from typing import List, Dict, Any, Optional

FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
MONGODB_URI = os.environ.get('MONGODB_URI')

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsItem(BaseModel):
    image: str
    heading: str
    heading_text: str
    short_view: str

uri = MONGODB_URI
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['news_database']
collection = db['news_collection']

def get_news():
    url = 'https://kathmandupost.com/politics/'
    response = requests.get(url)
    news_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all(class_='article-image')

        for article in articles:
            image_tag = article.find('img')
            image = image_tag['data-src'] if image_tag else None

            heading_tag = article.find('a', href=True)
            heading = heading_tag['href'] if heading_tag else None
            full_heading_url = 'https://kathmandupost.com' + heading

            heading_text_tag = article.find('h3')
            heading_text = heading_text_tag.get_text(strip=True) if heading_text_tag else None

            short_view_tag = article.find('p')
            short_view = short_view_tag.get_text(strip=True) if short_view_tag else None

            article_response = requests.get(full_heading_url)

            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                elements = article_soup.find_all(class_='updated-time')

                if elements:
                    for element in elements:
                        if "Updated at" in element.text:
                            updated_time_str = element.text.strip().replace('Updated at : ', '')
                            updated_time = datetime.strptime(updated_time_str, '%B %d, %Y %H:%M')

                            existing_article = collection.find_one({'heading': full_heading_url})

                            if existing_article:
                                existing_time = datetime.strptime(existing_article['updated_time'], '%B %d, %Y %H:%M')
                                if updated_time > existing_time:
                                    collection.update_one(
                                        {'heading': full_heading_url},
                                        {'$set': {'updated_time': updated_time_str}}
                                    )
                                    print(f"Updated article: {full_heading_url}")
                                else:
                                    print("Already exists")
                                    return news_data
                            else:
                                collection.insert_one({
                                    'image': image,
                                    'heading': full_heading_url,
                                    'heading_text': heading_text,
                                    'short_view': short_view,
                                    'updated_time': updated_time_str
                                })
                                print(f"Inserted new article: {full_heading_url}")

                            news_data.append({
                                'image': image,
                                'heading': full_heading_url,
                                'heading_text': heading_text,
                                'short_view': short_view,
                                'updated_time': updated_time_str
                            })

            break

    return news_data

def thumbnail_image(url: str, output_dir: str = "images") -> str:
    os.makedirs(output_dir, exist_ok=True)
    image_number = len(os.listdir(output_dir)) + 1
    filename = f"picture{image_number}.png"
    filepath = os.path.join(output_dir, filename)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath
    except requests.exceptions.RequestException:
        return None

def facebook_post(page_id: str, access_token: str, message: str, image_path: str):
    url = f"https://graph.facebook.com/{page_id}/photos"
    payload = {
        "message": message,
        "access_token": access_token,
    }

    with open(image_path, "rb") as image_file:
        files = {"source": (image_path, image_file, "image/png")}
        response = requests.post(url, data=payload, files=files)

    if response.status_code != 200:
        raise Exception(f"Error posting image: {response.json()}")
    else:
        print("Image downloaded successfully!")

if __name__ == "__main__":
    import uvicorn
    news_data = get_news()

    if news_data:
        news_item = news_data[0]
        image_url = news_item['image']
        message = f"{news_item['heading_text']} {news_item['short_view']} Read more: {news_item['heading']}"

        thumbnail_path = thumbnail_image(image_url)
        if thumbnail_path:
            facebook_post(FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN, message, thumbnail_path)
            print(f"Facebook Post Has Been Posted!")
        else:
            print("Failed to download image.")
    else:
        print("Failed to fetch news data.")
