# CLI coming soon
from nurs import NURS
from nurs.utils import parse_text, load_config
from nurs.summarizer import Summarizer
from nurs.encryption import Encryption
from nurs.utils.models import Nilam
import json
api = load_config()["API_KEYS"]

text = parse_text("https://freedium.cfd/https://medium.com/science-spectrum/how-hard-is-the-math-problem-in-good-will-hunting-76e4cb00b6f9")

summarizer = Summarizer(api["GEMINI_API_KEY"])
result = json.loads(summarizer.summarize(text))
print(result)

bearer = Encryption().get_bearer_authorization(api["jb_app_token"])
nurs = NURS(api["GEMINI_API_KEY"], bearer)
nilam = Nilam(
    user=1,
    title="How Hard is the Math Problem in Good Will Hunting?",
    author="Cole Frederick",
    publisher="Medium.com",
    summary=result["summarize"],
    review=result["review"],
    rating=5,
    websiteLink="https://freeedium.cfd/https://medium.com/science-spectrum/how-hard-is-the-math-problem-in-good-will-hunting-76e4cb00b6f9",
    publishedYear='2024',
)
nurs.upload(nilam)