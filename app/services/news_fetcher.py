import requests
from bs4 import BeautifulSoup
from app.services.summarizer import summarize_with_gemini

def get_image_link(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        img_element = soup.find('img', class_='sc-13b8515c-0 hbOWRP')
        return img_element['src'].replace("480", "800") if img_element else "Image not found"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_internal_article_links(url: str, limit: int = 1) -> list:
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

def fetch_news_content() -> dict:
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
        return {}
