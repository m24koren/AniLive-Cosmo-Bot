"""🔑 Sirlarni yangilash yordamchisi: yangi kuchli kalit yaratadi va hozirgilarini tekshiradi.

Hech narsani faylga yozmaydi va hech qayerga yubormaydi: yangi qiymatlar faqat ekranga chiqadi,
siz ularni Render -> Environment ga qo'lda kiritasiz.

    python scripts/rotate_secrets.py --check            # hozirgi sozlamalar yetarlicha kuchlimi?
    python scripts/rotate_secrets.py --emergency-key    # yangi EMERGENCY_RESET_KEY
    python scripts/rotate_secrets.py --secret-key       # yangi SECRET_KEY
    python scripts/rotate_secrets.py --webhook-secret   # yangi WEBHOOK_SECRET
    python scripts/rotate_secrets.py --encryption-key   # yangi ENCRYPTION_KEY (ehtiyot bo'ling!)
    python scripts/rotate_secrets.py --all              # to'rttasini birdan

⚠️ Chiqqan qiymatlarni chatga, GitHub'ga yoki skrinshotga tushirmang.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cryptography.fernet import Fernet  # noqa: E402

MIN_LEN = 32

# nom -> (qiymat yaratuvchi, yangilangandan keyingi oqibat)
GENERATORS = {
    "EMERGENCY_RESET_KEY": (
        lambda: secrets.token_urlsafe(48),
        "Eski kalit shu zahoti yaroqsiz bo'ladi. Yangisini parol menejerida saqlang: "
        "Telegram yo'qolganda faqat shu kalit sizni qutqaradi.",
    ),
    "SECRET_KEY": (
        lambda: secrets.token_urlsafe(48),
        "Barcha stream havolalari va taklif tokenlari yaroqsiz bo'ladi "
        "(foydalanuvchilar sahifani yangilasa kifoya).",
    ),
    "WEBHOOK_SECRET": (
        lambda: secrets.token_urlsafe(32),
        "Qayta deploydan keyin API webhook'ni yangi maxfiy token bilan o'zi qayta o'rnatadi.",
    ),
    "ENCRYPTION_KEY": (
        lambda: Fernet.generate_key().decode(),
        "XAVFLI: eski kalit bilan shifrlangan ma'lumotlar (masalan TOTP sirlari) o'qilmay qoladi. "
        "Faqat bazada shifrlangan ma'lumot yo'q bo'lsa yoki qayta shifrlashga tayyor bo'lsangiz "
        "almashtiring.",
    ),
}
FLAGS = {
    "emergency_key": "EMERGENCY_RESET_KEY",
    "secret_key": "SECRET_KEY",
    "webhook_secret": "WEBHOOK_SECRET",
    "encryption_key": "ENCRYPTION_KEY",
}


def fingerprint(value: str) -> str:
    """Qiymatni oshkor qilmay, ikki kalitni solishtirish uchun qisqa iz (SHA-256 boshi)."""
    return hashlib.sha256(value.encode()).hexdigest()[:8]


def _valid_fernet(key: str) -> bool:
    try:
        Fernet(key.encode())
        return True
    except Exception:  # noqa: BLE001
        return False


def check_current() -> int:
    """Hozirgi muhit o'zgaruvchilarini tekshiradi. Qiymatlarning o'zini ko'rsatmaydi."""
    from shared.config.settings import settings

    env = os.environ.get
    rows: list[tuple[str, bool, str]] = [
        ("BOT_TOKEN", bool(settings.BOT_TOKEN), "o'rnatilgan" if settings.BOT_TOKEN else "YO'Q"),
        ("SUPER_ADMIN_IDS", bool(settings.SUPER_ADMIN_IDS),
         f"{len(settings.SUPER_ADMIN_IDS)} ta" if settings.SUPER_ADMIN_IDS else "YO'Q"),
    ]
    sk = settings.SECRET_KEY
    weak_sk = sk in ("", "change-me") or len(sk) < MIN_LEN
    rows.append(("SECRET_KEY", not weak_sk,
                 f"{len(sk)} belgi" if not weak_sk else "zaif yoki standart qiymat"))
    wh = settings.WEBHOOK_SECRET
    rows.append(("WEBHOOK_SECRET", len(wh) >= 16,
                 f"{len(wh)} belgi" if len(wh) >= 16 else "yo'q yoki juda qisqa"))
    ek = settings.ENCRYPTION_KEY
    rows.append(("ENCRYPTION_KEY", _valid_fernet(ek),
                 "to'g'ri Fernet kaliti" if _valid_fernet(ek)
                 else "yo'q (SECRET_KEY'dan hosil qilinadi) yoki noto'g'ri"))
    em = env("EMERGENCY_RESET_KEY", "")
    rows.append(("EMERGENCY_RESET_KEY", len(em) >= MIN_LEN,
                 f"{len(em)} belgi" if len(em) >= MIN_LEN else "yo'q yoki juda qisqa"))

    bad = 0
    for name, ok, note in rows:
        bad += 0 if ok else 1
        print(f"  {'✅' if ok else '⚠️ '} {name:<20} {note}")
    print("\n🎉 Hammasi joyida." if not bad else f"\n⚠️  {bad} ta sozlamani kuchaytirish kerak.")
    return 0 if not bad else 1


def generate(names: list[str]) -> None:
    print("🔑 Yangi qiymatlar (faqat bir marta ko'rsatiladi, hech qayerga saqlanmadi):\n")
    for name in names:
        make, effect = GENERATORS[name]
        value = make()
        print(f"{name}={value}")
        print(f"   🔎 iz: {fingerprint(value)}  |  ℹ️  {effect}\n")
    print("📋 Keyingi qadamlar:")
    print("  1. Render -> streambot-api -> Environment ga yuqoridagi qiymatlarni kiriting.")
    print("  2. Saqlang: Render o'zi qayta deploy qiladi.")
    print("  3. /health va botga /start bilan tekshiring.")
    print("  4. Eski qiymatlarni parol menejeridan o'chiring.")
    print("⚠️  Bu qiymatlarni chatga yoki GitHub'ga tashlamang.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--check", action="store_true", help="hozirgi sirlar kuchini tekshirish")
    ap.add_argument("--all", action="store_true", help="to'rtala sirni yaratish")
    for flag in FLAGS:
        ap.add_argument(f"--{flag.replace('_', '-')}", dest=flag, action="store_true")
    args = ap.parse_args()

    if args.check:
        print("🔍 Sirlar tekshiruvi:\n")
        return check_current()
    names = list(GENERATORS) if args.all else [n for f, n in FLAGS.items() if getattr(args, f)]
    if not names:
        ap.print_help()
        return 0
    generate(names)
    return 0


if __name__ == "__main__":
    sys.exit(main())
