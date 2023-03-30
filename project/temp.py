import httpx
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
import asyncio


class Tool(BaseModel):
    _createdAt: str
    _id: str
    _rev: str
    _type: str
    _updatedAt: str
    defunct: dict = Field(None)
    duplicate: bool
    favCount: int
    id: str
    mainImage: dict
    newFeatures: List[str] = Field(None)
    pricing: List[str]
    publishedAt: str
    publishedAt_timestamp: int
    slug: dict
    slugIndex: str
    socialLinks: List[str] = Field(None)
    startingPrice: str = Field(None)
    status: str
    tagsIndex: List[str]
    toolCategories: List[dict]
    toolDescription: str
    toolName: str
    toolRichTextDescription: List[dict] = Field(None)
    toolShortDescription: str
    verified: bool
    verifiedReason: str = Field(None)
    websiteUrl: str
    youtubeUrl: str = Field(None)


async def fetch_tools(page_num: int) -> List[Tool]:
    url = f"https://www.futurepedia.io/api/tools?page={page_num}&sort=verified"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        tools_json = response.json()
        return [Tool(**tool) for tool in tools_json]


async def fetch_all_tools(num_pages: int) -> List[Tool]:
    tasks = [fetch_tools(page_num) for page_num in range(1, num_pages + 1)]
    tools_lists = await asyncio.gather(*tasks)
    all_tools = []
    for tools in tools_lists:
        all_tools.extend(tools)
    return all_tools


import json

result = asyncio.run(fetch_all_tools(165))
with open("tools.json", "w") as f:
    f.write(json.dumps([tool.dict() for tool in result]))
print(len(result))
