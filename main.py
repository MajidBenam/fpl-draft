from fpl import FPL
import aiohttp
import asyncio
async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        gameweek = await fpl.get_gameweek(1)
    print(gameweek)
# Python 3.7+
asyncio.run(main())