import asyncio
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
import datetime

API_ID = 9309709
API_HASH = 'cba32691d5804bc435725c6ce0a3c27c'

SOURCE_CHANNEL_ID = '@MTP_roto'
DESTINATION_CHANNEL_ID = '@proxy1321'

SCHEDULED_TIMES = ["09:00", "13:30", "18:00", "22:00"]

# PROXY = {
#     'proxy_type': 'socks5',
#     'addr': '127.0.0.1',
#     'port': 10808
# }

SESSION_NAME = 'my_telegram_account'

lock = asyncio.Lock()


async def forward_last_message(client):
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
            await client.forward_messages(destination_entity, last_message)

            print(f"پیام با آیدی {last_message.id} با موفقیت فوروارد شد.")

        except FloodWaitError as e:
            print(f"خطای FloodWait: {e.seconds} ثانیه صبر می‌کنیم.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"خطا: {e}")


async def scheduler():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("کلاینت تلگرام متصل شد.")
        print("شروع برنامه‌ریزی...")

        while True:
            now = datetime.datetime.now().strftime("%H:%M")

            if now in SCHEDULED_TIMES:
                print(f"\n[{now}] زمان‌بندی رسید، اجرای وظیفه...")
                await forward_last_message(client)
                await asyncio.sleep(60)  # جلوگیری از اجرای دوباره در همان دقیقه

            await asyncio.sleep(1)


if __name__ == "__main__":
    print("ربات شروع شد. Ctrl+C برای توقف.")
    asyncio.run(scheduler())
