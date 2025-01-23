from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Nilam:
    user: str
    title: str
    author: str
    publisher: str
    summary: str
    review: str
    language: str="en"
    category: str="blog"
    date: str=datetime.now().strftime("%Y-%m-%d")
    type: str="digitalSource"