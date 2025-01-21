from bs4 import BeautifulSoup
from bs4.element import Comment
import requests

def tag_visible(element):
    if element.parent and element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return ' '.join(' '.join(t.strip() for t in visible_texts).split())
    
def parse_text(url):
    html = requests.get(url).text
    return text_from_html(html)