"""Webhook'ni qo'lda boshqarish (odatda kerak emas: API ishga tushganda o'zi o'rnatadi).

    python scripts/set_webhook.py            # o'rnatish
    python scripts/set_webhook.py --info     # holatni ko'rish
    python scripts/set_webhook.py --delete   # o'chirish
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aiogram import Bot  # noqa: E402

from shared.config.settings import settings  # noqa: E402


async def main(action: str) -> int:
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN o'rnatilmagan")
        return 1
    bot = Bot(settings.BOT_TOKEN)
    try:
        if action == "delete":
            await bot.delete_webhook(drop_pending_updates=False)
            print("Webhook o'chirildi")
        elif action == "set":
            if not settings.BASE_URL:
                print("BASE_URL (yoki RENDER_EXTERNAL_URL) kerak")
                return 1
            from apps.bot_app.dispatcher import get_dispatcher

            await bot.set_webhook(
                settings.webhook_url, secret_token=settings.WEBHOOK_SECRET or None,
                allowed_updates=get_dispatcher().resolve_used_update_types(),
                drop_pending_updates=False)
            print(f"Webhook o'rnatildi: {settings.webhook_url}")
        info = await bot.get_webhook_info()
        print(f"url={info.url or '—'} pending={info.pending_update_count} "
              f"last_error={info.last_error_message or '—'}")
        return 0
    finally:
        await bot.session.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--info", action="store_true")
    g.add_argument("--delete", action="store_true")
    a = ap.parse_args()
    sys.exit(asyncio.run(main("delete" if a.delete else "info" if a.info else "set")))
