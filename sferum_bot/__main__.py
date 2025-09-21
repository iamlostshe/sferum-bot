"""Bot startup module."""

import asyncio

from loguru import logger

from sferum_bot import config
from sferum_bot.main import main as _main
from sferum_bot.vk.methods import get_credentials, get_user_credentials


async def main() -> None:
    """Bot startup function."""
    logger.add("sferum.log")
    logger.info("Bot was started")

    await config.init_session()

    try:
        user = await get_user_credentials()
        access_token = user.access_token
        creds = await get_credentials(access_token)

        await _main(
            creds.server,
            creds.key,
            creds.ts,
            access_token,
            creds.pts,
        )

    except KeyboardInterrupt:
        logger.info("Bot was stoped")
        await config.bot.close()
        await config.session.close()

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
