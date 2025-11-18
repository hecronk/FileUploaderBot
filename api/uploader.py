import aiohttp
import websockets
from config import API_BASE, WS_BASE, FILE_SERVE_BASE


async def upload_file(auth, file_path: str) -> str:
    url = f"{API_BASE}/file/upload"

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            data = aiohttp.FormData()
            data.add_field("upload_file", f, filename=file_path)

            async with session.post(url, data=data, headers=auth.headers) as resp:
                res = await resp.json()
                return res["job_id"]


async def track_job(job_id: str, on_status_update):
    ws_url = f"{WS_BASE}/jobs/ws/{job_id}"

    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            import json
            data = json.loads(message)

            await on_status_update(data)

            if data["status"] == "completed":
                return FILE_SERVE_BASE + data["result"]
