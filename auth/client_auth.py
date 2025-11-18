import aiohttp
from config import API_BASE

class AuthClient:
    def __init__(self, token=None):
        self.token = token

    @property
    def headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    async def login(self, username, password):
        url = f"{API_BASE}/auth/login"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"username": username, "password": password}) as resp:
                if resp.status != 200:
                    return False, await resp.text()
                data = await resp.json()
                self.token = data["access_token"]
                return True, self.token
