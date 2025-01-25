import requests
from typing import Optional
from .utils.models import Nilam
from .encryption import Encryption
from .utils.logger import Logger
logger = Logger()

class NURS:
    def __init__(self, gemini_api_key, bearer):
        self.gemini_api_key = gemini_api_key
        self.bearer = bearer
        self.API_ENDPOINT = "https://ains-api.moe.gov.my/api"
        self.encryption = Encryption()

    def _request_api(self, url:str, method:str="GET", data:Optional[Nilam]=None):
        parsed_url = url[1:] if url.startswith('/') else url
        url = f"{self.API_ENDPOINT}/{parsed_url}"

        option_headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Access-Control-Request-Headers': 'authorization' if method == "GET" else 'authorization,content-type',
            'Access-Control-Request-Method': method,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://ains.moe.gov.my',
            'Pragma': 'no-cache',
            'Referer': 'https://ains.moe.gov.my/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0'
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': self.bearer,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://ains.moe.gov.my',
            'Pragma': 'no-cache',
            'Referer': 'https://ains.moe.gov.my/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
            'sec-ch-ua': '"Chromium";v="130", "Opera GX";v="115", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
        }

        requests.options(url, headers=option_headers)
        if data is not None:
            post_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': self.bearer,
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://ains.moe.gov.my',
                'Pragma': 'no-cache',
                'Referer': 'https://ains.moe.gov.my/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0',
                'sec-ch-ua': '"Chromium";v="130", "Opera GX";v="115", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            json_data = {"data": data.json()}
            response = requests.request(method=method, url=url, headers=post_headers, json=json_data)
            return response.json()
        response = requests.request(method=method, url=url, headers=headers)
        return response.json()

    def _get_id(self) -> int:
        URL = "/users/me?populate=*"
        logger.log("Requesting user ID...")
        response = self._request_api(URL, "GET")
        return response["id"]

    def upload(self, nilam:Nilam):
        URL = "/nilam-records/submit"
        logger.log("Fetching user ID...")
        nilam.user = self._get_id()
        logger.success(f"User ID fetched: {nilam.user}")
        logger.log("Encrypting data to generate provider...")
        nilam.provider = self.encryption.get_provider(nilam.get_provider_parameter())
        logger.success(f"Successfully generated provider: {nilam.provider}")

        response = self._request_api(URL, method="POST", data=nilam)
        return response