# **AI News Feed**

## Overview

The **newsPulse** is a FastAPI-based application designed to automate news curation, summarization, and social media posting. It scrapes news articles from a specified source, uses Google's Generative AI (Gemini) to summarize the content, and then posts both the summaries and associated images to Facebook and Instagram. The system also integrates MongoDB Atlas to track posted news articles, preventing duplicates and ensuring that only unique content is shared.

- Scrapes news articles from a specified source (e.g., BBC).
- Summarizes the content using Google's Generative AI (Gemini).
- Posts summaries and images to Facebook and Instagram.
- Utilizes MongoDB Atlas to prevent duplicate postings.

```
newsPulse/
    ├── app/
    │   ├── main.py                   # Main FastAPI app and API logic
    │   ├── config.py                 # Configuration and environment variables
    │   ├── services/
    │   │   ├── news_fetcher.py       # Functions for fetching and parsing news articles
    │   │   ├── image_handler.py      # Functions for downloading and saving images
    │   │   ├── summarizer.py         # Function for summarizing articles using Gemini API
    │   │   ├── social_media.py       # Functions for posting on Instagram and Facebook
    │   ├── models/
    │   │   └── news_item.py          # Pydantic model for NewsItem
    ├── requirements.txt              # List of dependencies
    ├── .env                          # Environment variables (not committed to version control)
    ├── README.md                     # Project overview and instructions
    ├── images/                       # Folder for saved images (make sure to ignore this folder in `.gitignore`)
    └── run.py                        # Script to start the FastAPI app
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

## Contributing

We welcome contributions to improve this project. If you have suggestions or would like to report an issue, please feel free to open an issue or submit a pull request.

---