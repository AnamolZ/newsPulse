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

# Environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
INSTAGRAM_ID = os.getenv('INSTAGRAM_ID')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

# FastAPI app setup
app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client['news_database']
collection = db['news_collection']

class NewsItem(BaseModel):
    image: str
    heading: str
    heading_text: str
    short_view: str

def get_image_link(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        img_element = soup.find('img', class_='sc-13b8515c-0 hbOWRP')
        return img_element['src'].replace("480", "800") if img_element else "Image not found"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_internal_article_links(url: str, limit: int = 1) -> List[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', attrs={'data-testid': 'internal-link'})
        article_links = ["https://www.bbc.com" + link.get('href') for link in links if '/news/articles/' in link.get('href')]
        return article_links[:limit]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_article_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article_paragraphs = soup.find_all('p')
        return '\n'.join([paragraph.get_text() for paragraph in article_paragraphs])
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def summarize_with_gemini(text: str) -> str:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = f"Summarize the following text:\n{text}"
    response = model.generate_content([prompt])
    return response.text.strip()

def fetch_news_content() -> Dict[str, Any]:
    url = "https://www.bbc.com/business/technology-of-business"
    article_links = get_internal_article_links(url)
    
    if article_links:
        article_url = article_links[0]
        image_link = get_image_link(article_url)
        article_content = get_article_content(article_url)
        summarized_content = summarize_with_gemini(article_content)

        return {
            'image_link': image_link,
            'article_url': article_url,
            'summarized_content': summarized_content.replace('\n', ''),
        }
    else:
        print("No article links found.")
        return {}

def save_image(url: str, output_dir: str = "images") -> Optional[str]:
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

def post_to_instagram(account_id: str, access_token: str, image_url: str, caption: str):
    media_url = f"https://graph.facebook.com/v12.0/{account_id}/media"
    payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }

    response = requests.post(media_url, data=payload)
    response_json = response.json()

    if 'id' in response_json:
        container_id = response_json['id']
        publish_url = f"https://graph.facebook.com/v12.0/{account_id}/media_publish"
        publish_payload = {
            'creation_id': container_id,
            'access_token': access_token
        }

        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response_json = publish_response.json()
        
        if publish_response.status_code == 200:
            print("Posted on Instagram")
        else:
            raise Exception(f"Error publishing media: {publish_response_json}")
    else:
        raise Exception(f"Error creating media container: {response_json}")

def post_to_facebook(page_id: str, access_token: str, image_path: str, caption: str):
    photo_url = f"https://graph.facebook.com/{page_id}/photos"
    payload = {
        "message": caption,
        "access_token": access_token,
    }

    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        response = requests.post(photo_url, data=payload, files=files)

    if response.status_code == 200:
        print("Posted on Facebook")
    else:
        raise Exception(f"Error posting image: {response.json()}")

if __name__ == "__main__":
    news_data = fetch_news_content()
    if news_data:
        image_url = news_data['image_link']
        message = news_data['summarized_content']

        thumbnail_path = save_image(image_url)
        if thumbnail_path:
            post_to_facebook(PAGE_ID, FACEBOOK_ACCESS_TOKEN, thumbnail_path, message)
            post_to_instagram(INSTAGRAM_ID, INSTAGRAM_ACCESS_TOKEN, image_url, message)
            print("Post Has Been Posted!")
        else:
            print("Failed to post.")
    else:
        print("Failed to fetch news data.")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)