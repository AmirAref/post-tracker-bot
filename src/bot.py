from post_tracker.utils import get_tracking_post
from post_tracker.errors import TrackingNotFoundError
from httpx import AsyncClient
import asyncio


async def main():
    code = input("Enter the code : ")
    async with AsyncClient() as client:
        try:
            data = await get_tracking_post(client=client, tracking_code=code)
            print(data)
        except TrackingNotFoundError as e:
            print(e)


asyncio.run(main())

