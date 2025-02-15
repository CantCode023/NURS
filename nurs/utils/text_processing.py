from bs4 import BeautifulSoup
from bs4.element import Comment
from better_profanity import profanity
from .exceptions import HasProfanity
from seleniumbase import SB
from .logger import Logger
logger = Logger()

def get_page_source(url):
    logger.log("Getting page content...")
    with SB(uc=True, headless=False) as sb:
        logger.warn("Captcha detected, bypassing...")
        sb.activate_cdp_mode(url)
        sb.uc_gui_click_captcha()
        logger.success("Bypassed captcha")
        while not sb.is_element_visible("body > div.fixed.bottom-4.left-4"):
            sb.sleep(1)
        html = sb.get_page_source()
        logger.success("Successfully scraped page content")
    return html

def tag_visible(element):
    if element.parent and element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
    
def has_profanity(text) -> bool:
    if any(word in text.lower() for word in ["javascript", "cookie"]):
        return True
    return profanity.contains_profanity(text)
    
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    
    logger.info("Checking if text is safe...")
    title = soup.find("title").text.split(" |")[0]
    print(title)
    filtered = has_profanity(title)
    if filtered:
        raise HasProfanity("Bad words found in title! Please try with another article.")
        
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return ' '.join(' '.join(t.strip() for t in visible_texts).split())
    
def parse_text(url) -> str:
    logger.info("Getting text from URL...")
    html = get_page_source(url)
    return text_from_html(html)