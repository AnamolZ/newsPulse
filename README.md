# FastAPI News Scraper and Facebook Poster

This project is a FastAPI application that scrapes news articles from the Kathmandu Post website, downloads the images, and posts the news to a Facebook page. It uses MongoDB Atlas to store and check if news articles have already been posted to avoid duplicates.

*This project was developed to demonstrate how to build a FastAPI application with web scraping, image handling, and integration with external APIs. It also showcases using MongoDB Atlas for data storage and GitHub Actions for CI/CD automation.*

## Features

- Scrapes the latest news articles from the Kathmandu Post politics section.
- Downloads images associated with the news articles.
- Posts the news articles and images to a specified Facebook page.
- Uses MongoDB Atlas to store posted news URLs to prevent duplicate postings.
- Automatically triggers every 5 minutes using GitHub Actions.

## Requirements

- Python 3.x
- MongoDB Atlas account
- Facebook page and access token
- GitHub repository for running GitHub Actions

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

    Create a `.env` file in the root directory and add the following:

    ```env
    FACEBOOK_ACCESS_TOKEN=facebook_access_token
    MONGODB_URI=mongodb+srv://mongodb_atlas_id:mongodb_atlas_password@cluster0.cfalpt9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
    ```

4. **Run the application**:

    ```sh
    uvicorn main:app --reload
    ```

## Project Structure

- `main.py`: The main FastAPI application file.
- `requirements.txt`: The Python dependencies.
- `.env`: Environment variables file (not included in the repository).
- `.github/workflows/main.yml`: GitHub Actions workflow file to schedule the scraping and posting job.

## Usage

### Local Testing

1. Start the FastAPI server:

    ```sh
    uvicorn main:app --reload
    ```

2. Access the news scraping endpoint:

    ```sh
    http://localhost:8000/news
    ```

### GitHub Actions

This project uses GitHub Actions to run the news scraping and posting job every 5 minutes. Ensure you have the following secrets set in your GitHub repository:

- `FACEBOOK_ACCESS_TOKEN`
- `MONGODB_URI`

The GitHub Actions workflow file `.github/workflows/main.yml` is configured to:

- Check out the repository.
- Set up Python.
- Install dependencies.
- Run the FastAPI script.
- Upload the log file as an artifact.

### Setting up Secrets

1. Go to your GitHub repository.
2. Navigate to `Settings` > `Secrets` > `Actions`.
3. Add the following secrets:
    - `FACEBOOK_ACCESS_TOKEN`
    - `MONGODB_URI`

## Dependencies

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `requests`: A simple, yet elegant HTTP library.
- `beautifulsoup4`: A library for parsing HTML and XML documents.
- `pydantic`: Data validation and settings management using Python type annotations.
- `pymongo`: A Python driver for MongoDB.
- `python-dotenv`: Reads key-value pairs from a `.env` file and can set them as environment variables.
- `uvicorn`: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)

---
