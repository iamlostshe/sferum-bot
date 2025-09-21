"""Main cycle module."""

from asyncio import sleep

from loguru import logger

from sferum_bot import config
from sferum_bot.tg.methods import send_error, send_message
from sferum_bot.vk.methods import get_credentials, get_message, get_user_credentials
from sferum_bot.vk.vk_types import EventMessage, Message


async def main(
    server: str,
    key: str,
    ts: int,
    access_token: str,
    pts: int,
    # TODO(@iamlostshe): Допилить работу в супергруппах  # noqa: FIX002, TD003
    # tg_topic_id=None,  # noqa: ERA001
) -> None:
    """Cycle function."""
    data = {
        "act": "a_check",
        "key": key,
        "ts": ts,
        "wait": 10,
    }

    while True:
        await sleep(0.2)
        try:
            async with config.session.post(f"https://{server}", data=data) as r:
                req = await r.json()

            logger.debug(req)

            if req.get("updates"):
                data["ts"] += 1
                event = req["updates"][0]

                if event[0] == 4:
                    raw_msg = EventMessage(*event)
                    logger.info(f"[MAIN] raw_msg: {raw_msg}")

                    if (
                        config.config.vk_chat_ids == "all"
                        or str(raw_msg.chat_id) in config.config.vk_chat_ids
                    ):
                        logger.debug("[MAIN] allowed chat")

                        _message = await get_message(access_token, pts)

                        if _message.get("error"):
                            access_token = (await get_user_credentials()).access_token
                            credentials = await get_credentials(access_token)
                            data["ts"] = credentials.ts
                            data["key"] = credentials.key

                            _message = await get_message(access_token, pts)

                            logger.error(_message)
                        else:
                            logger.debug(_message)

                        pts += 1

                        message = _message["items"]
                        profile = _message["profiles"]
                        chat_title = _message["title"]

                        chat_title = "" if not chat_title else f"{chat_title}"

                        msg = Message()
                        await msg.async_init(
                            **message[-1],
                            profiles=profile,
                            chat_title=chat_title,
                        )
                        await send_message(
                            config.bot,
                            msg,
                            config.config.tg_chat_id,
                            # TODO(@iamlostshe): Допилить работу в супергруппах  # noqa: E501, FIX002, TD003
                            tg_topic_id=None,
                        )
                    else:
                        pts += 1

            is_failed = req.get("failed")

            if is_failed == 1:
                data["ts"] = req["ts"]

            elif is_failed == 2:
                access_token = (await get_user_credentials()).access_token
                credentials = await get_credentials(access_token)
                data["ts"] = credentials.ts
                data["key"] = credentials.key
        except Exception as e:
            await send_error(
                config.bot,
                config.config.tg_chat_id,
                config.config.tg_topic_id,
            )
            logger.exception(e)
