import requests
from .utils.models import Nilam
from .encryption import Encryption

class NURS:
    def __init__(self, gemini_api_key, jb_app_token):
        self.gemini_api_key = gemini_api_key
        self.jb_app_token = jb_app_token
        self.API_ENDPOINT = "https://ains.gov.my/api"
        self.encryption = Encryption()
        self.headers = {
            'Access-Control-Request-Headers': 'authorization',
            'Access-Control-Request-Method': 'GET',
            'Connection': 'keep-alive',
            'Referer': 'https://ains.moe.gov.my/',
            'User-Agent': 'Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/533.47 (KHTML, like Gecko) Chrome/49.0.3858.378 Safari/601',
        }
        
    def _update_headers(self):
        new_header = self.headers
        del new_header['Access-Control-Request-Headers']
        del new_header['Access-Control-Request-Method']
        new_header["Authorization"] = self.encryption.get_bearer_authorization(self.jb_app_token)
        return new_header
        
    def _request_api(self, url:str):
        requests.options(url, headers=self.headers)
        new_header = self._update_headers()
        response = requests.get(url, headers=new_header).json()
        return response

    def _get_id(self) -> int:
        URL = f"{self.API_ENDPOINT}/users/me?populate=*"
        response = self._request_api(URL)
        return response["id"]

    def upload(self, nilam:Nilam):
        return