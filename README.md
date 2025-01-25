# NURS
NILAM Unsupervised Reasoning Summarizer, an AINS automation software.

# .env format
```
GEMINI_API_KEY=your_api_key
jb_app_token=your_jb_app_token
```

# TODOLIST
- [x] Add function to scrape website text in text_processing.py
- [x] Make summarizer function using Google Gemini
- [x] Add functions to get provider key and bearer authorization
- [x] Use request to upload nilam
  - Make custom stars (int 1-5) and favourite (bool)
- [x] Add bad words filter in utils, make a custom exception in exceptions.py
  - Add other exceptions like bad api key, etc
- [ ] Make cli
  - add cooldown between requests

# FUTURE TODOLIST
- [ ] Add News API support