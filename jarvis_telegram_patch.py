import asyncio
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
INBOX    = BASE_DIR / "telegram_inbox.json"
OUTBOX   = BASE_DIR / "telegram_outbox.json"


class TelegramBridge:
    def __init__(self, jarvis):
        self.jarvis = jarvis
        print("[Telegram] Bridge watching for inbox messages...")

    def _read_inbox(self):
        """Check if there's a new command from Telegram."""
        if not INBOX.exists():
            return None
        try:
            data = json.loads(INBOX.read_text(encoding="utf-8"))
            if not data.get("processed"):
                return data
        except Exception:
            pass
        return None

    def _mark_processed(self):
        """Mark inbox message as processed."""
        if INBOX.exists():
            try:
                data = json.loads(INBOX.read_text(encoding="utf-8"))
                data["processed"] = True
                INBOX.write_text(json.dumps(data), encoding="utf-8")
            except Exception:
                pass

    def write_outbox(self, response: str):
        """Write Jarvis's response for Telegram bot to pick up."""
        data = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "ready": True
        }
        OUTBOX.write_text(json.dumps(data), encoding="utf-8")
        print(f"[Telegram] Response sent: {response[:80]}")

    async def poll(self):
        """Continuously check for incoming Telegram commands."""
        print("[Telegram] Polling for commands...")
        while True:
            try:
                inbox = self._read_inbox()
                if inbox:
                    text = inbox.get("text", "")
                    print(f"[Telegram] Command received: {text}")
                    self._mark_processed()

                    # Send to Jarvis as if the user typed it
                    if self.jarvis.session:
                        await self.jarvis.session.send_client_content(
                            turns={"parts": [{"text": text}]},
                            turn_complete=True
                        )
                        # Wait a moment for Jarvis to process
                        await asyncio.sleep(3)
                        self.write_outbox("Command sent to Jarvis! Check your laptop.")
                    else:
                        self.write_outbox("Jarvis is not connected yet. Try again in a moment.")

            except Exception as e:
                print(f"[Telegram] Poll error: {e}")

            await asyncio.sleep(0.5)  # check every 0.5 seconds