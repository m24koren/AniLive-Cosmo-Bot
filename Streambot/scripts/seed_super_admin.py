"""👑 Bosh adminlarni bazaga yozish va boshqarish.

Odatda kerak emas: API ishga tushganda `SUPER_ADMIN_IDS` dagi adminlar o'zi yoziladi.
Bu skript qo'lda tekshirish yoki tuzatish uchun.

    python scripts/seed_super_admin.py                  # SUPER_ADMIN_IDS dagilarni yozish
    python scripts/seed_super_admin.py --id 111 222     # qo'shimcha ID'larni ham qo'shish
    python scripts/seed_super_admin.py --list           # adminlar ro'yxati
    python scripts/seed_super_admin.py --revoke 222     # rolni oddiy foydalanuvchiga tushirish
    python scripts/seed_super_admin.py --dry-run        # hech narsa yozmasdan ko'rsatish

Chiqish kodi: 0 — hammasi joyida, 1 — xato.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.cache.redis_client import close_redis  # noqa: E402
from shared.config.constants import ROLE_SUPER_ADMIN, ROLE_USER  # noqa: E402
from shared.config.settings import settings  # noqa: E402
from shared.database.engine import dispose_engine  # noqa: E402
from shared.utils.validators import is_valid_telegram_id  # noqa: E402

ROLE_ICONS = {
    "super_admin": "👑", "admin": "🛡", "content_manager": "🎬",
    "moderator": "🚨", "support": "💬", "vip": "💎", "user": "👤",
}


def _icon(role: str) -> str:
    return ROLE_ICONS.get(role, "👤")


def _collect_ids(extra: list[str] | None) -> tuple[list[int], list[str]]:
    """SUPER_ADMIN_IDS + --id qiymatlari. (to'g'ri ID'lar, noto'g'ri qiymatlar)"""
    seen: dict[int, None] = {i: None for i in settings.SUPER_ADMIN_IDS}
    bad: list[str] = []
    for raw in extra or []:
        for part in raw.replace(",", " ").split():
            if is_valid_telegram_id(part):
                seen[int(part)] = None
            else:
                bad.append(part)
    return list(seen), bad


async def _print_staff() -> None:
    from modules.users import public as users

    staff = await users.list_staff()
    if not staff:
        print("📭 Hozircha xodimlar yo'q.")
        return
    print(f"👥 Xodimlar ({len(staff)} ta):")
    for c in staff:
        name = c["full_name"] or (f"@{c['username']}" if c["username"] else "—")
        flag = "  🚫 bloklangan" if c["is_banned"] else ""
        print(f"  {_icon(c['role'])} {c['tg_id']:<14} {c['role']:<16} {name}{flag}")


async def _seed(ids: list[int], dry_run: bool) -> int:
    from modules.users import public as users

    if not ids:
        print("⚠️  Adminlar ro'yxati bo'sh. `SUPER_ADMIN_IDS` ni yozing yoki --id bering.")
        return 1
    for tg_id in ids:
        profile = await users.get_profile(tg_id)
        was = f"{_icon(profile.role)} {profile.role}" if profile else "yangi"
        if profile and profile.role == ROLE_SUPER_ADMIN and not profile.is_banned:
            print(f"✅ {tg_id}: allaqachon 👑 bosh admin")
            continue
        if dry_run:
            print(f"🔎 {tg_id}: {was} → 👑 super_admin bo'lardi (dry-run)")
            continue
        await users.ensure_super_admin(tg_id)
        print(f"👑 {tg_id}: {was} → super_admin")
    return 0


async def _revoke(ids: list[int], dry_run: bool) -> int:
    from modules.users import public as users

    code = 0
    for tg_id in ids:
        if tg_id in settings.SUPER_ADMIN_IDS:
            print(f"⛔ {tg_id}: SUPER_ADMIN_IDS da turibdi — avval Render env'dan olib tashlang")
            code = 1
            continue
        profile = await users.get_profile(tg_id)
        if profile is None:
            print(f"❔ {tg_id}: bazada topilmadi")
            continue
        if profile.role == ROLE_USER:
            print(f"✅ {tg_id}: allaqachon oddiy foydalanuvchi")
            continue
        if dry_run:
            print(f"🔎 {tg_id}: {profile.role} → user bo'lardi (dry-run)")
            continue
        old = await users.set_role(tg_id, ROLE_USER)
        print(f"👤 {tg_id}: {_icon(old)} {old} → user")
    return code


async def main(args: argparse.Namespace) -> int:
    if args.revoke:
        ids, bad = _collect_ids(args.revoke)
        ids = [i for i in ids if i not in settings.SUPER_ADMIN_IDS or i in _only_explicit(args.revoke)]
    else:
        ids, bad = _collect_ids(args.id)
    for b in bad:
        print(f"⚠️  '{b}' — noto'g'ri Telegram ID, o'tkazib yuborildi")

    try:
        if not args.dry_run and not args.list:
            from apps.bot_app.bootstrap import create_missing_tables

            await create_missing_tables()  # jadvallar yo'q bo'lsa yaratadi
        if args.list:
            await _print_staff()
            return 0
        code = await (_revoke(ids, args.dry_run) if args.revoke else _seed(ids, args.dry_run))
        if not args.dry_run:
            print()
            await _print_staff()
        return code
    except Exception as exc:  # noqa: BLE001 — skript foydalanuvchiga tushunarli xabar beradi
        print(f"❌ Xato: {type(exc).__name__}: {exc}")
        return 1
    finally:
        await close_redis()
        await dispose_engine()


def _only_explicit(raw: list[str]) -> set[int]:
    out: set[int] = set()
    for r in raw:
        out |= {int(p) for p in r.replace(",", " ").split() if is_valid_telegram_id(p)}
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--id", nargs="+", metavar="ID", help="qo'shimcha bosh admin ID'lari")
    ap.add_argument("--revoke", nargs="+", metavar="ID", help="rolni oddiy foydalanuvchiga tushirish")
    ap.add_argument("--list", action="store_true", help="xodimlar ro'yxatini ko'rsatish")
    ap.add_argument("--dry-run", action="store_true", help="hech narsa yozmasdan ko'rsatish")
    sys.exit(asyncio.run(main(ap.parse_args())))
      
