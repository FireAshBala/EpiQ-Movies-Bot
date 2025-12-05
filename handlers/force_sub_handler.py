import asyncio
from typing import (
    Union
)
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)


async def handle_force_sub(bot: Client, cmd: Message):
    if Config.UPDATES_CHANNEL and Config.UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(Config.UPDATES_CHANNEL)
    elif Config.UPDATES_CHANNEL and (not Config.UPDATES_CHANNEL.startswith("-100")):
        channel_chat_id = Config.UPDATES_CHANNEL
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=-1003093316288, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥](https://t.me/+jzT1Tp8lB8w4ZDFl).",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=-1003093316288)
        except Exception as err:
            print(f"Unable to do Force Subscribe to {Config.UPDATES_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**ᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ!✨**\n\n"
                 "ᴅᴜᴇ ᴛᴏ ᴏᴠᴇʀʟᴏᴀᴅ, ᴏɴʟʏ ᴄʜᴀɴɴᴇʟ ꜱᴜʙꜱᴄʀɪʙᴇʀꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ!😄",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 ʀᴇꜰʀᴇꜱʜ 🔄", url=f"https://t.me/{Config.BOT_USERNAME}?start={cmd.command[1]}")
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Thank you [𝖧𝖺𝗏𝖾 𝖽𝗈𝗎𝖻𝗍𝗌? 𝖥𝖾𝖾𝗅 𝖿𝗋𝖾𝖾 𝗍𝗈 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗈𝗎𝗋 𝖺𝖽𝗆𝗂𝗇 𝗍𝖾𝖺𝗆 𝖶𝖾'𝗋𝖾 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗁𝖾𝗅𝗉!](https://t.me/+jzT1Tp8lB8w4ZDFl).",
            disable_web_page_preview=True
        )
        return 200
    return 200
