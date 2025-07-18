import asyncio
from telethon import TelegramClient, Button
from telethon.errors.rpcerrorlist import FloodWaitError
import datetime
import re
import pytz  

API_ID = 9309709
API_HASH = 'cba32691d5804bc435725c6ce0a3c27c'

SOURCE_CHANNEL_ID = '@MTP_roto'
DESTINATION_CHANNEL_ID = '@AzadvpnPro'

SCHEDULED_TIMES = ["00:30" , "10:30", "11:30", "12:30", "13:30", "14:30",
                   "15:30", "16:30", "17:30", "18:30", "19:30", "20:30",
                   "21:30", "22:30", "23:30"]

SESSION_NAME = 'my_telegram_account'

TIMEZONE = 'Asia/Tehran'  

lock = asyncio.Lock()


def format_proxy_message(text):
    lines = text.splitlines()
    location_line = next((line.replace("**", "").strip() for line in lines if 'Location' in line), '')
    secret_line = next((line for line in lines if 'Secret:' in line), '')
    url_match = re.search(r'(https?://\S+)', secret_line)
    secret_url = url_match.group(1) if url_match else ''
    if secret_url.endswith(')'):
        secret_url = secret_url[:-1]

    formatted_text = (
        "AzadVPNPro | Proxy پروکسی 🔒\n\n"
        f"{location_line}\n"
        "Speed: Ultra Fast⚡️ \n\n"
        f"Connect here:\n\n{secret_url}\n\n\n\n\n"
        "Channel: @AzadvpnPro\n"
        "Support: @Aliwjafari"
    )
    return formatted_text, secret_url


async def copy_and_send_last_message(client):
    async with lock:
        print(f"[{datetime.datetime.now()}] اجرای وظیفه شروع شد...")

        try:
            source_entity = await client.get_entity(SOURCE_CHANNEL_ID)
            destination_entity = await client.get_entity(DESTINATION_CHANNEL_ID)
            messages = await client.get_messages(source_entity, limit=1)

            if not messages:
                print("هیچ پیامی یافت نشد.")
                return

            last_message = messages[0]

            if last_message.text:
                formatted_text, secret_url = format_proxy_message(last_message.text)
                await client.send_message(
                    destination_entity,
                    formatted_text,
                    buttons=[Button.url('Connect here', secret_url)],
                    link_preview=False,
                    parse_mode='md'
                )
                print(f"پیام با آیدی {last_message.id} با فرمت جدید ارسال شد.")
            else:
                print("آخرین پیام متنی نبود و ارسال نشد.")

        except FloodWaitError as e:
            print(f"خطای FloodWait: {e.seconds} ثانیه صبر می‌کنیم.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"خطا: {e}")


async def scheduler():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("کلاینت تلگرام متصل شد.")
        print("شروع برنامه‌ریزی...")

        timezone = pytz.timezone(TIMEZONE)

        await copy_and_send_last_message(client)

        while True:
            now = datetime.datetime.now(timezone).strftime("%H:%M")

            if now in SCHEDULED_TIMES:
                print(f"\n[{now}] زمان‌بندی رسید، اجرای وظیفه...")
                await copy_and_send_last_message(client)
                await asyncio.sleep(60)

            await asyncio.sleep(1)


if __name__ == "__main__":
    print("ربات شروع شد. Ctrl+C برای توقف.")
    asyncio.run(scheduler())
