"""Глобальные настройки бота."""

from __future__ import annotations

import aiohttp
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings


async def init_session() -> None:
    """Инициализация сессии aiohttp."""
    global session  # noqa: PLW0603
    session = aiohttp.ClientSession(
        trust_env=True,
        connector=aiohttp.TCPConnector(ssl=False),
    )


class Config(BaseSettings):
    """Глобальные настройки бота."""

    auth_cookie: str
    bot_token: str
    tg_chat_id: str | None
    vk_chat_ids: str


# Препарируем данные из конфига
config: Config = Config(_env_file=".env")

if not config.vk_chat_ids:
    config.vk_chat_ids = "all"
elif config.vk_chat_ids != "all":
    config.vk_chat_ids = "".join(
        config.vk_chat_ids.split(),
    ).split(",")

# Инициализируем бота
bot = Bot(
    token=config.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
)
