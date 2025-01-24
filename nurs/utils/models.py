from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import requests, json
from bs4 import BeautifulSoup

@dataclass
class Nilam:
    user: int
    title: str
    author: str
    publisher: str
    summary: str
    review: str
    rating: int
    websiteLink: str
    provider: Optional[str]=None
    reviewIsVideo: bool=False
    language: str="en"
    category: str="blog"
    date: str=datetime.now().strftime("%Y-%m-%d")
    type: str="digitalSource"
    publishedYear: str=datetime.now().strftime("%Y")
    
    def __post_init__(self):
        self.publisher = "Medium.com" if "medium.com" in self.websiteLink else self.publisher
        self.websiteLink = self.websiteLink.replace("https://freedium.cfd/", "") if "freedium.cfd" in self.websiteLink else self.websiteLink

    def json(self):
        return {
            "user": self.user,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "summary": self.summary,
            "review": self.review,
            "language": self.language,
            "category": self.category,
            "date": self.date,
            "type": self.type,
            "provider": self.provider,
            "reviewIsVideo": self.reviewIsVideo,
            "websiteLink": self.websiteLink,
            "rating": self.rating,
            "publishedYear": self.publishedYear
        }
        
    def get_provider_parameter(self):
        """Return only paramters that are required to be encrypted."""
        return {
            "user": self.user,
            "type": self.type,
            "date": self.date,
            "title": self.title,
            "category": self.category,
            "author": self.author,
            "publisher": self.publisher,
            "language": self.language,
            "summary": self.summary,
            "review": self.review,
        }