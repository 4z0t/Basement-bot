import json
import urllib.request
import requests
import aiohttp
import asyncio


HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://yandex.ru",
    "Referer": "https://yandex.ru/",
}

API_URL = "https://zeapi.yandex.net/lab/api/yalm/text3"


async def balaboba_text(text):
    payload = {"query": text, "intro": 0, "filter": 1}
    params = json.dumps(payload).encode("utf8")

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.post(API_URL, data=params) as resp:
            response: dict = await resp.json(content_type=None)
            return response.get("text", "")


async def main():
    return await balaboba_text("Привет всем")


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
