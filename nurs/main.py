import requests
from .utils.models import Nilam
from .encryption import Encryption

class NURS:
    def __init__(self, gemini_api_key, jb_app_token):
        self.gemini_api_key = gemini_api_key
        self.jb_app_token = jb_app_token
        self.API_ENDPOINT = "https://ains-api.moe.gov.my/api"
        self.encryption = Encryption()
        self.option_headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Access-Control-Request-Headers': 'authorization',
            'Access-Control-Request-Method': 'GET',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://ains.moe.gov.my',
            'Pragma': 'no-cache',
            'Referer': 'https://ains.moe.gov.my/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0',
        }
        
    def _request_api(self, url:str):
        parsed_url = url[1:] if url.startswith('/') else url
        url = f"{self.API_ENDPOINT}/{parsed_url}"
        
        requests.options(url, headers=self.option_headers)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': self.encryption.get_bearer_authorization(self.jb_app_token),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://ains.moe.gov.my',
            'Pragma': 'no-cache',
            'Referer': 'https://ains.moe.gov.my/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0',
            'sec-ch-ua': '"Chromium";v="130", "Opera GX";v="115", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = requests.get(url, headers=headers).json()
        return response

    def _get_id(self) -> int:
        URL = "/users/me?populate=*"
        response = self._request_api(URL)
        return response["id"]

    def upload(self, nilam:Nilam):
        return