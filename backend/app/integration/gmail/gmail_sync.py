from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import async_session_maker
from app.models import JobSeeker
from app.integration.gmail.application_tracker import sync_gmail_applications


scheduler = AsyncIOScheduler()


async def sync_all_users():
    async with async_session_maker() as session:

        result = await session.execute(select(JobSeeker.user_id))
        users = result.scalars().all()

        for user_id in users:
            await sync_gmail_applications(session, user_id)


def start_scheduler():
    scheduler.add_job(sync_all_users, "interval", minutes=5)
    scheduler.start()