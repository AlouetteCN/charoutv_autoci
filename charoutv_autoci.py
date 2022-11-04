import os
import re
import sys
import telethon
from qrcode import QRCode
from telethon import TelegramClient, events

from utils.debug import dn
from utils.config_loader import ProfileLoader
from utils.captcha import captcha_solver, handle_captcha_solved_result
from constants import base


# Load profile
main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
pl = ProfileLoader(main_dir)
conf = pl.conf

# Starting telethon
client = TelegramClient(conf['base']['client_name'], conf['telegram_api']['api_id'], conf['telegram_api']['api_hash'])


async def _qrlogin():
    # should be continue
    if not client.is_connected():
        await client.connect()

    print(f"- User login status: {await client.is_user_authorized()}")
    if not await client.is_user_authorized():
        print("- Trying to login...")
        qr = QRCode()

        def display_url_as_qr(url):
            print(url)
            qr.clear()
            qr.add_data(url)
            qr.print_ascii()

        qr_login = await client.qr_login()
        is_login = False
        while not is_login:
            display_url_as_qr(qr_login.url)
            try:
                is_login = await qr_login.wait(15)
                print("- Login successed!")
            except Exception:
                await qr_login.recreate()


async def send_checkin_msg():
    if not client.is_connected():
        await client.connect()

    await client.send_message(base.CHANNEL_ID, base.CHECKIN_MSG)


@client.on(events.NewMessage(chats=base.CHANNEL_ID))
async def handler(event: telethon.events):
    global RETRY_TERMS
    # 根据button count 区分消息类型``
    if re.match(pattern="签到(.*)获得", string=event.message.text) is not None:
        dn("Succeed to checkin!")
        # 结束异步任务
        await client.disconnect()
    elif re.match(pattern="(.*)已经签", string=event.message.text) is not None:
        dn("Already checkined!")
        await client.disconnect()
    elif re.match(pattern="(.*)输入验证码", string=event.message.text) is not None:
        await client.download_media(event.message.photo, "captcha.jpg")
        solved_result = captcha_solver("captcha.jpg", conf)
        if "result" not in solved_result:
            await client.send_message(base.CHANNEL_ID, "114514")
            return
        captcha_code = handle_captcha_solved_result(solved_result)
        await client.send_message(event.message.chat_id, captcha_code)
        os.remove("captcha.jpg")
    elif re.match(pattern="(.*)(错误|不正确)", string=event.message.text) is not None:
        dn(f"Invalid captcha code! Retrying at {RETRY_TERMS}")
        RETRY_TERMS -= 1
        if RETRY_TERMS == 0:
            dn("Failed to varify captcha code, exit.")
            dn(f"captcha id: {conf['captcha_api']['id']}", f"captcha key: {conf['captcha_api']['apikey']}")
            await client.disconnect()
        await client.send_message(event.message.chat_id, base.CHECKIN_MSG)


client.start()
client.loop.create_task(send_checkin_msg())
client.run_until_disconnected()
