import asyncio
from app.db import AsyncSessionLocal 
from app.integration.gmail.application_tracker import sync_gmail_applications


async def run_test():
    async with AsyncSessionLocal() as session:
        await sync_gmail_applications(
            session=session,
            user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )


asyncio.run(run_test())