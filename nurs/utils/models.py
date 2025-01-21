from dataclasses import dataclass

@dataclass
class Nilam:
    user: int
    author: str
    category: str
    date: str
    language: str
    provider: str
    publishedYear: str
    publisher: str
    rating: int
    review: str
    reviewIsVideo: bool
    summary: str
    title: str
    type: str
    websiteLink: str