import httpx
from hashlib import md5

from .base import AMLProvider


class RealAMLProvider(AMLProvider):
    def __init__(self, api_url: str, api_access_key: str, api_access_id: str):
        self.api_url = api_url
        self.api_access_key = api_access_key
        self.api_access_id = api_access_id

    async def get_aml_data(self, post_data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            req_data = post_data.copy()
            token_string = f"{req_data.get('hash')}{self.api_access_key}{self.api_access_id}"
            req_data.update(
                accessId=self.api_access_id,
                token=md5(token_string.encode()).hexdigest(),
            )
            response = await client.post(
                self.api_url,
                data=req_data,
            )
            response.raise_for_status()
            return response.json()
