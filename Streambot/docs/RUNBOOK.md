# Runbook: nosozliklarni bartaraf etish

## Tez tekshiruv

| Tekshiruv | Qanday | Kutilgan natija |
|---|---|---|
| Servis tirikmi | `https://<servis>.onrender.com/health` | `{"status":"ok"}` |
| Baza va Redis | `https://<servis>.onrender.com/health/deep` | baza va Redis holati "ok" |
| Webhook | `make webhook` (yoki `python scripts/set_webhook.py --info`) | URL to'g'ri, `last_error` bo'sh |
| Loglar | Render -> servis -> Logs | ERROR qatorlari yo'q |

## 1. Bot javob bermayapti

1. `/health` ni oching. Ochilmasa, servis uxlagan yoki yiqilgan: Render -> Logs ga qarang.
2. Servis tirik bo'lsa, webhook holatini tekshiring: `python scripts/set_webhook.py --info`.
   - `last_error_message` bor bo'lsa, shu xatoga qarab ish tuting (quyida).
   - URL noto'g'ri yoki bo'sh bo'lsa: `python scripts/set_webhook.py` bilan qayta o'rnating.
3. `BOT_TOKEN` to'g'riligini tekshiring (Render -> Environment). Token almashtirilgan bo'lsa, yangisini yozib qayta deploy qiling.
4. Bir vaqtda ham webhook, ham polling ishlamasligi kerak. Lokal polling bot yoqilgan bo'lsa, o'chiring.

## 2. Servis uxlab qoladi (Render bepul reja)

Bepul web servis trafiksiz qolsa uxlaydi, birinchi so'rov sekin bo'ladi.

- `streambot-keepalive` (Cron Job) har 10 daqiqada `/health` ni chaqiradi.
- `KEEPALIVE_URL` to'g'ri yozilganini tekshiring: `https://<servis>.onrender.com/health`.
- Cron Job pullik bo'lsa: uni o'chirib, UptimeRobot yoki cron-job.org dan har 5-10 daqiqada `/health` ga ping qo'ying.

## 3. Xotira yoki disk to'lib borayapti

Xotira va disk **85%** da adminlarga ogohlantirish, **90%** da kritik ogohlantirish va avtomatik tozalash ishlaydi (`MEMORY_WARN_PERCENT`, `MEMORY_CRIT_PERCENT`, `DISK_WARN_PERCENT`, `DISK_CRIT_PERCENT`).

Agar ogohlantirish tez-tez kelsa:

1. Render -> Metrics da xotira grafigini ko'ring.
2. `DISABLED_MODULES` orqali og'ir, kerak bo'lmagan modullarni o'chiring.
3. `TMP_MAX_AGE_HOURS` ni kamaytiring (vaqtinchalik fayllar tezroq tozalanadi).
4. `OUTBOX_KEEP_DAYS` ni kamaytiring (eski hodisalar tezroq o'chadi).
5. Baribir yetmasa, reja (plan) ni kattaroqqa o'tkazing.

## 4. Baza bilan muammo

- `/health/deep` da baza "xato" bo'lsa: `DATABASE_URL` to'g'riligini va baza provayderi (Neon, Supabase) ishlayotganini tekshiring.
- Bepul bazalar ba'zan "uxlaydi", birinchi ulanish sekin bo'lishi mumkin.
- Migratsiya xatosi: Logs da `alembic` xatosini toping. Lokal tekshirish: `make migrate`.
- Zaxira nusxa olish: `make backup` (`scripts/backup_database.py`). Katta o'zgarishdan oldin zaxira oling.

## 5. Redis bilan muammo

- `REDIS_URL` bo'sh bo'lsa, xotiradagi kesh ishlaydi: bu normal, lekin faqat bitta nusxa uchun.
- Redis ulanmasa, kesh va lock vaqtincha ishlamaydi. Fon vazifalari o'tkazib yuboriladi, bot ishlashda davom etadi.
- `streambot-redis` servisi holatini Render'da tekshiring.

## 6. Web App ochilmayapti yoki "avtorizatsiya xatosi"

1. Web App faqat Telegram ichidan ochilganda ishlaydi (`initData` kerak).
2. `BOT_TOKEN` o'zgargan bo'lsa, eski `initData` yaroqsiz: ilovani yopib qayta oching.
3. Vaqt farqi: server soati to'g'ri bo'lishi kerak (`INIT_DATA_TTL_SECONDS`).
4. `WEBAPP_URL` va BotFather'dagi Mini App manzili mos bo'lishi kerak.

## 7. Video ochilmayapti

- `STORAGE_BACKEND=telegram` bo'lsa, 20 MB dan katta videoni Web App'da oqimlab bo'lmaydi: `r2` yoki `s3` ga o'ting.
- Stream havolasi muddati tugagan bo'lishi mumkin (`STREAM_TOKEN_TTL_SECONDS`): sahifani yangilang.
- "Qurilmalar limiti" xatosi: foydalanuvchi limitdan ko'p qurilmada ko'rmoqda (`DEVICE_LIMIT_DEFAULT`).

## 8. Fon vazifalari ishlamayapti

- `WORKER_EMBEDDED=true` bo'lsa, vazifalar `api` ichida ishlaydi. Logs da `worker` yoki `scheduler` qatorlarini qidiring.
- Vazifa Redis lock bilan himoyalangan. Yiqilgan vazifa lock'ni ushlab qolsa, lock muddati tugagach o'zi bo'shaydi.
- Bitta vazifaning xatosi boshqalariga ta'sir qilmaydi, adminlarga ogohlantirish yuboriladi.

## 9. Modul yuklanmadi

Ishga tushishda Logs da `module load failed: <nom>` qatori chiqadi, adminlarga xabar boradi. Qolgan modullar ishlayveradi.

- Sababni logdan toping, kodni tuzating, qayta deploy qiling.
- Vaqtincha o'chirish: `DISABLED_MODULES=<nom>`.

## 10. Yangi versiyani chiqarish (deploy)

1. O'zgarishni GitHub'ga yuklang (`main` branch). `autoDeploy` yoqilgan bo'lsa, Render o'zi deploy qiladi.
2. Deploy tugagach: `/health`, keyin botga `/start`.
3. Muammo bo'lsa: Render -> Deploys -> oldingi muvaffaqiyatli deploy -> **Rollback**.

## 11. Token yoki kalit sizib chiqdi

`docs/SECURITY.md` dagi "Token sizib chiqsa" bo'limini bajaring: `/revoke`, Render'da yangilash, qayta deploy, webhook'ni qayta o'rnatish.

## 12. Foydali buyruqlar

```bash
make webhook      # webhook holati
make backup       # baza zaxirasi
make seed-admin   # bosh adminni bazaga yozish
make migrate      # migratsiyani qo'llash
make parity       # bot va Web App tengligini tekshirish
```

Xato kodlari ma'nosi: `docs/ERROR_CODES.md`.
