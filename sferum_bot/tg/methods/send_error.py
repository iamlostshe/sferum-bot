"""Send msg to telegram."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot


async def send_error(
    bot: Bot,
    tg_chat_id: int,
    tg_topic_id: str | None = None,
) -> None:
    """Send error notify to telegram."""
    await bot.send_message(
        text="Сообщение из сферума не смогло обработаться\\.\\.\\.",
        chat_id=tg_chat_id,
        message_thread_id=tg_topic_id,
    )
