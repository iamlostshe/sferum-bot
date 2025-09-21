"""Get info about user."""

from loguru import logger

from sferum_bot import config
from sferum_bot.vk.vk_types import UserCredentials


async def get_user_credentials() -> UserCredentials:
    """Get info about user."""
    async with config.session.get(
        url="https://web.vk.me/",
        params={
            "act": "web_token",
            "app_id": 8202606,
        },
        cookies={
            "remixdsid": config.config.auth_cookie,
        },
        allow_redirects=False,
    ) as r:
        req = await r.json()

    logger.debug(req)
    return UserCredentials(**req[1])
