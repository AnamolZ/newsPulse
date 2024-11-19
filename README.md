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
    │   ├── main.py
    │   ├── config.py               
    │   ├── services/
    │   │   ├── news_fetcher.py      
    │   │   ├── image_handler.py     
    │   │   ├── summarizer.py    
    │   │   ├── social_media.py     
    │   ├── models/
    │   │   └── news_item.py       
    ├── requirements.txt           
    ├── .env                       
    ├── README.md                
    ├── images/                   
    └── run.py                   
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

## Contributing

We welcome contributions to improve this project. If you have suggestions or would like to report an issue, please feel free to open an issue or submit a pull request.

---
