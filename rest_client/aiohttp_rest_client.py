import aiohttp
import json

from .base_rest_client import RestClient


class AioHttpRestClient(RestClient):

    def __init__(self, base_url: str, headers: dict | None = None, raise_for_status: bool = False):
        super().__init__(base_url, headers, raise_for_status)

    async def get(self, url: str):
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=self.raise_for_status) as session:
            async with session.get(url=self.base_url + url, headers=self.headers) as response:
                json_data = await response.json()
                status = response.status
                return json_data, status

    async def delete(self, url: str):
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=self.raise_for_status) as session:
            async with session.delete(url=self.base_url + url, headers=self.headers) as response:
                status = response.status
                if status == 200:
                    json_data = await response.json()
                else:
                    json_data = None
                return json_data, status

    async def post(self, url: str, data: dict | None | list = None):
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=self.raise_for_status) as session:
            data = json.dumps(data) if data else None
            async with session.post(url=self.base_url + url, data=data, headers=self.headers) as response:
                json_data = await response.json()
                status = response.status
                return json_data, status

    async def put(self, url: str, data: dict | None | list = None):
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=self.raise_for_status) as session:
            data = json.dumps(data) if data else None
            async with session.put(url=self.base_url + url, data=data, headers=self.headers) as response:
                json_data = await response.json()
                status = response.status
                return json_data, status

    async def patch(self, url: str, data: dict | None | list = None):
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=self.raise_for_status) as session:
            data = json.dumps(data) if data is not None else None
            async with session.patch(url=self.base_url + url, data=data, headers=self.headers) as response:
                json_data = await response.json()
                status = response.status
                return json_data, status
