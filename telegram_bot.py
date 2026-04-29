import asyncio
import json
import httpx
from pathlib import Path
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN = "your_telegram_bot_token_here"
ALLOWED_USER = your_telegram_user_id
# ──────────────────────────────────────────────────────────────────────────────

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
BASE_DIR = Path(__file__).resolve().parent
INBOX    = BASE_DIR / "telegram_inbox.json"
OUTBOX   = BASE_DIR / "telegram_outbox.json"


def write_inbox(text: str):
    data = {
        "text": text,
        "timestamp": datetime.now().isoformat(),
        "processed": False
    }
    INBOX.write_text(json.dumps(data), encoding="utf-8")


def read_outbox() -> str | None:
    if not OUTBOX.exists():
        return None
    try:
        data = json.loads(OUTBOX.read_text(encoding="utf-8"))
        if data.get("ready"):
            OUTBOX.unlink()
            return data.get("response", "Done.")
    except Exception:
        pass
    return None


async def send_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })


async def wait_for_response(timeout: int = 20) -> str:
    for _ in range(timeout * 10):
        response = read_outbox()
        if response:
            return response
        await asyncio.sleep(0.1)
    return "Jarvis didn't respond in time!"


async def main():
    print("[Telegram] Bot starting...")
    offset = 0

    # First clear any old pending updates
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(f"{BASE_URL}/getUpdates", params={"offset": -1, "limit": 1})
            updates = r.json().get("result", [])
            if updates:
                offset = updates[-1]["update_id"] + 1
                print(f"[Telegram] Cleared old updates, starting from offset {offset}")
        except Exception as e:
            print(f"[Telegram] Could not clear updates: {e}")

    print("[Telegram] Bot is running! Text your bot on Telegram.")

    while True:
        try:
            async with httpx.AsyncClient(timeout=35) as client:
                r = await client.get(f"{BASE_URL}/getUpdates", params={
                    "offset": offset,
                    "timeout": 25,
                    "allowed_updates": ["message"]
                })
                data = r.json()

                if not data.get("ok"):
                    print(f"[Telegram] API error: {data}")
                    await asyncio.sleep(2)
                    continue

                updates = data.get("result", [])

                for update in updates:
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    user_id = message.get("from", {}).get("id")
                    text    = message.get("text", "")

                    if not text:
                        continue

                    print(f"[Telegram] Message from {user_id}: {text}")

                    if user_id != ALLOWED_USER:
                        await send_message(chat_id, "Unauthorized.")
                        continue

                    if text == "/start":
                        await send_message(chat_id,
                            "🤖 Jarvis is online!\nText me any command and I'll forward it to your laptop.")
                        continue

                    write_inbox(text)
                    await send_message(chat_id, "⚡ Sending to Jarvis...")

                    response = await wait_for_response(timeout=20)
                    await send_message(chat_id, f"🤖 {response}")
                    print(f"[Telegram] Replied: {response}")

        except httpx.TimeoutException:
            pass  # normal, just means no new messages
        except Exception as e:
            print(f"[Telegram] Error: {e}")
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())