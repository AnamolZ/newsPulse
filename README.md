---

# AI-Enhanced News Feed

This project is a FastAPI application that scrapes news articles, summarizes them, downloads the images, and posts the news to both Facebook and Instagram. It uses MongoDB Atlas to store and check if news articles have already been posted to avoid duplicates.

*This project demonstrates how to build a FastAPI application with web scraping, image handling, and integration with external APIs. It also showcases using MongoDB Atlas for data storage.*

## Features

- Scrapes the latest news articles from a specified website.
- Downloads images associated with the news articles.
- Summarizes article content using Google's Generative AI.
- Posts the news articles and images to a specified Facebook page and Instagram account.
- Uses MongoDB Atlas to store posted news URLs to prevent duplicate postings.

## Requirements

- Python 3.x
- MongoDB Atlas account
- Facebook page and access token
- Instagram account and access token

## Setup

1. **Clone the repository**:

    ```sh
    git clone https://github.com/AnamolZ/NewsBridge.git
    cd NewsBridge
    ```

2. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the root directory

4. **Run the application**:

    ```sh
    uvicorn main:app --reload
    ```

## Project Structure

- `main.py`: The main FastAPI application file.
- `requirements.txt`: The Python dependencies.
- `.env`: Environment variables file (not included in the repository).

## Usage

### Local Testing

1. Start the FastAPI server:

    ```sh
    uvicorn main:app --reload
    ```

2. Access the news scraping endpoint (if implemented):

    ```sh
    http://localhost:8000/news
    ```

## Dependencies

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `requests`: A simple, yet elegant HTTP library.
- `beautifulsoup4`: A library for parsing HTML and XML documents.
- `pydantic`: Data validation and settings management using Python type annotations.
- `pymongo`: A Python driver for MongoDB.
- `google-generativeai`: A library for accessing Google's generative AI models.
- `Pillow`: The Python Imaging Library adds image processing capabilities to your Python interpreter.
- `uvicorn`: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Google Generative AI](https://cloud.google.com/ai/generative-ai)

---
