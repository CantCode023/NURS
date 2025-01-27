import os, sys, requests, json, random, time
from rich import print as rprint
from rich.pretty import pprint
from bs4 import BeautifulSoup
from rich.prompt import Prompt
from pathlib import Path
from colorama import Fore, init
from datetime import datetime
init(autoreset=True)

from nurs import NURS
from nurs import load_config, parse_text
from nurs.summarizer import Summarizer
from nurs.encryption import Encryption
from nurs.utils.models import Nilam
from nurs.utils.logger import Logger
logger = Logger()

def save_api(gemini_api_key, jb_app_token):
    with open(Path(__file__).parent / ".env", "w") as f:
        f.write(f'GEMINI_API_KEY="{gemini_api_key}"\njb_app_token="{jb_app_token}"')

def api_key_not_found() -> dict[str, dict[str, str]]:
    logger.error("API keys not found! Retrieving from input.")
    logger.log("Please refer the documentation if you do not know how to retrieve your API keys.\n")
    
    gemini_api_key = Prompt.ask("Please enter your Gemini API key", password=True)
    jb_app_token = Prompt.ask("Please enter your jb_app_token", password=True)
    
    save_api(gemini_api_key, jb_app_token)
        
    return {"API_KEYS": {"GEMINI_API_KEY": gemini_api_key, "jb_app_token": jb_app_token}}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(text:str=f"{Fore.WHITE}[1] Upload NILAM\n[2] Update API Keys\n[3] Exit"):
    clear()
    
    TITLE = f"""[royal_blue1] ██████   █████ █████  █████ ███████████    █████████ 
░░██████ ░░███ ░░███  ░░███ ░░███░░░░░███  ███░░░░░███
 ░███░███ ░███  ░███   ░███  ░███    ░███ ░███    ░░░ 
 ░███░░███░███  ░███   ░███  ░██████████  ░░█████████ 
 ░███ ░░██████  ░███   ░███  ░███░░░░░███  ░░░░░░░░███
 ░███  ░░█████  ░███   ░███  ░███    ░███  ███    ░███
 █████  ░░█████ ░░████████   █████   █████░░█████████ 
░░░░░    ░░░░░   ░░░░░░░░   ░░░░░   ░░░░░  ░░░░░░░░░  
[italic][/royal_blue1][white]
> NILAM Unsupervised Reasoning Summarizer 
[/white][/italic][bright_black]
Author: CantCode023 (bd.)
Github: https://github.com/CantCode023/NURS
Discord: bd8344[/bright_black]"""
    rprint(TITLE)
    
    print(f"\n{text}")
    
def upload_cli(api:dict[str, str]):
    show_menu("")
    url = Prompt.ask("Please enter the URL of the article")
    r = requests.get(url)
    logger.success("URL exists")
    soup = BeautifulSoup(r.text, "html.parser")
    logger.success("Successfully parsed HTML")
    
    source = soup.find("meta", {"property": "og:site_name"})
    if source and source.get("content") == "Medium":
        logger.log("Extracting data from HTML...")
        title = soup.find("meta", {"property": "og:title"}).get("content")
        logger.success(f"Extracted title: {title}")
        author = soup.find("meta", {"name": "author"}).get("content")
        logger.success(f"Extracted author: {author}")
        
        json_script = soup.find('script', {'type': 'application/ld+json'})
        json_data = json.loads(json_script.string)
        date_published = json_data['datePublished']
        logger.success(f"Extracted date: {date_published[:4]}")
        
        logger.warn("Paywal detected, bypassing...")
        no_paywall_url = "https://freedium.cfd/" + url
        logger.success("Paywall bypassed")
        
        text = parse_text(no_paywall_url)
        logger.success("Successfully extracted content")
        
        logger.log("Summarizing content, this might take a while...")
        summarizer = Summarizer(api["GEMINI_API_KEY"])
        result = json.loads(summarizer.summarize(text))
        logger.success("Summarization complete")
        pprint(result)
        
        logger.log("Encrypting data to generate bearer token...")
        bearer = Encryption().get_bearer_authorization(api["jb_app_token"])
        logger.success(f"Bearer token generated: {bearer}")
        
        logger.log("Uploading data to AINS...")
        nurs = NURS(api["GEMINI_API_KEY"], bearer)
        nilam = Nilam(
            title=title,
            author=author,
            publisher="Medium.com",
            summary=result["summarize"],
            review=result["review"],
            rating=5,
            websiteLink=url,
            publishedYear=date_published[:4],
            date=datetime.now().strftime("%Y-%m-%d"),
            language="en",
            category="blog",
            type="digitalSource",
            reviewIsVideo=False,
            provider=None,
            user=1
        )
        print(nilam.date)
        pprint(nilam.json())
        response = nurs.upload(nilam)
        logger.success("Successfully uploaded data to AINS!")
        logger.info(response)
        logger.log("All tasks complete.")
        logger.info("Press enter to continue...")
        input()
        return True
    else:
        logger.error("NURS currently does not support URLs from other sources!")
        logger.info("Press enter to continue...")
        input()
        
def update_api(api:dict[str,str]):
    while True:
        show_menu(text=f"{Fore.WHITE}[1] Update Gemini API Key\n[2] Update jb_app_token\n[3] Exit")
        option = int(input("[:] "))
        if option == 1:
            gemini_api_key = Prompt.ask("Please enter your Gemini API key", password=True)
            save_api(gemini_api_key, api["jb_app_token"])
            logger.success("Gemini API key updated!")
            logger.info("Press enter to continue...")
            input()
        elif option == 2:
            jb_app_token = Prompt.ask("Please enter your jb_app_token", password=True)
            save_api(api["GEMINI_API_KEY"], jb_app_token)
            logger.success("jb_app_token updated!")
            logger.info("Press enter to continue...")
            input()
        elif option == 3:
            break
    
if __name__ == "__main__":
    config = load_config()
    if config is None:
        config = api_key_not_found()
    api = config["API_KEYS"]
    
    last_upload_time = 0
    while True:
        show_menu()
        try:
            option = int(input("[:] "))
            
            if option == 1:
                cooldown_finished = time.time() - last_upload_time > 30
                if not cooldown_finished:
                    remaining_time = int(30 - (time.time() - last_upload_time))
                    logger.warn(f"Please wait {remaining_time} seconds before uploading again!")
                    logger.info("Press enter to continue...")
                    input()
                    continue
                response = upload_cli(api)
                if response:
                    last_upload_time = time.time()
            elif option == 2:
                update_api(api)
            elif option == 3:
                break
            else:
                logger.error("Invalid option!")
                logger.info("Press enter to continue...")
                input()
        except ValueError:
            logger.error("Invalid option!")
            logger.info("Press enter to continue...")
            input()