from enum import Enum

import httpx
import chardet
from pydantic import BaseModel

__userAgentText = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
header = {"User-Agent": __userAgentText}


def autodetect(content):
    return chardet.detect(content).get("encoding")


async def async_get(
    url: str, headers: str = header, params: dict = {}, cookies: str | None = None
):
    async with httpx.AsyncClient(default_encoding=autodetect) as client:
        res = await client.get(url, headers=headers, params=params, cookies=cookies)
        if res.status_code == 200:
            return True, res
        else:
            return False, str(res.status_code)


async def async_post(
    url: str, headers: str = header, data: dict = {}, cookies: str | None = None
):
    async with httpx.AsyncClient(default_encoding=autodetect) as client:
        res = await client.post(url, headers=headers, data=data, cookies=cookies)
        if res.status_code == 200:
            return True, res
        else:
            return False, str(res.status_code)


class DownloadType(Enum):
    POST = "POST"
    GET = "GET"


class DownloadCommand(BaseModel):
    url: str
    downloadtype: DownloadType
    cookies: str | None = None
    headers: dict = header
    params: dict = {}


async def async_download_text(command: DownloadCommand) -> str:
    if command.downloadtype == DownloadType.GET:
        ok, ret = await async_get(
            url=command.url,
            headers=command.headers,
            cookies=command.cookies,
            params=command.params,
        )
    elif command.downloadtype == DownloadType.POST:
        ok, ret = await async_post(
            url=command.url,
            headers=command.headers,
            cookies=command.cookies,
            data=command.params,
        )
    if ok:
        return ret.text
    return ret
