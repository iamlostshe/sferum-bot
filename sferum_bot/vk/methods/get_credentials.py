"""Get server info."""

from loguru import logger

from sferum_bot import config
from sferum_bot.vk.vk_types import ServerCredentials

from .consts import LP_VERSION, V


async def get_credentials(
    access_token: str,
) -> ServerCredentials:
    """Get server info."""
    async with config.session.post(
        "https://api.vk.me/method/messages.getLongPollServer",
        data={
            "need_pts": 1,
            "group_id": 0,
            "LP_VERSION": LP_VERSION,
            "access_token": access_token,
        },
        params={
            "v": V,
        },
    ) as r:
        req = await r.json()

    logger.debug(req)
    return ServerCredentials(**req["response"])
