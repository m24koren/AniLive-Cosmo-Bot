# 🎬 Streambot

Telegram Media Studiosi: **anime, multfilm, kino, donghua va dramalar** uchun bot + Mini App (Web App) + admin paneli.
Bot tugmalari va Web App bir xil servislarni chaqiradi, shuning uchun ikkalasi doim bir xil ishlaydi.

## 🧱 Tizim tuzilmasi

| Jarayon | Vazifasi | Render'da |
|---|---|---|
| **api** | FastAPI + Telegram **webhook** (bot shu yerda) + Web App + fon vazifalari (`WORKER_EMBEDDED=true`) | Web Service |
| **worker** | Faqat fon vazifalari (ixtiyoriy, `WORKER_EMBEDDED=false` bo'lsa) | Worker |
| **bot** | Polling rejimidagi bot (lokal ishlab chiqish uchun) | kerak emas |
| **keepalive** | `/health` ni har 10 daqiqada chaqiradi | Cron Job yoki tashqi ping |

Papkalar:

```
apps/       ishga tushiriladigan jarayonlar (bot_app, api_app, worker_app)
shared/     poydevor: config, database, cache, storage, security, events, i18n, telegram, utils
modules/    funksiyalar (har biri mustaqil "quti"): users, auth, roles, settings, audit,
            catalog, media, player, search, library, subscriptions, vip, payments, support, ...
webapp/     Mini App (foydalanuvchi va admin paneli)
docker/     Dockerfile.api, Dockerfile.bot, Dockerfile.worker
scripts/    set_webhook, keepalive, backup va boshqa yordamchi skriptlar
tests/      avtomatik testlar
docs/       arxitektura, xavfsizlik, runbook, xato kodlari
```

Har modul ichida: `manifest.py`, `public.py` (boshqa modullar faqat shuni import qiladi), `service.py`,
`repository.py`, `domain/`, `adapters/bot`, `adapters/api`, `i18n/`, `tasks.py`, `events.py`.
Bitta modul buzilsa, qolganlari ishlashda davom etadi (`module_loader` har birini alohida yuklaydi).

## ⚙️ Sozlamalar (environment o'zgaruvchilari)

| O'zgaruvchi | Izoh |
|---|---|
| `BOT_TOKEN` | BotFather tokeni. **Faqat Render'da** saqlanadi, kodga yozilmaydi |
| `SUPER_ADMIN_IDS` | Bosh admin Telegram ID (vergul bilan ko'p: `111,222`). Hozir: `8869400604` |
| `DATABASE_URL` | PostgreSQL manzili (`postgresql://...`) |
| `REDIS_URL` | Redis manzili (bo'sh bo'lsa xotiradagi vaqtinchalik kesh ishlaydi) |
| `ENCRYPTION_KEY` | `python -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"` |
| `SECRET_KEY`, `WEBHOOK_SECRET` | Render o'zi yaratadi |
| `BASE_URL`, `WEBAPP_URL` | Render'da **bo'sh** qoldiring, avtomatik olinadi |
| `STORAGE_BACKEND` | `telegram` (file_id), `r2` yoki `s3` |
| `KEEPALIVE_URL` | `https://<servis>.onrender.com/health` |

To'liq ro'yxat: `.env.example`.

## 🚀 Render.com'ga joylash

1. **Tokenni yangilang.** Token ochiq joyda qolgan bo'lsa: @BotFather → `/revoke` → yangi token.
2. **Baza tayyorlang.** Muddatsiz bepul PostgreSQL (masalan Neon yoki Supabase) tavsiya etiladi. Ulanish manzili `DATABASE_URL` ga yoziladi.
3. **GitHub.** Loyihani **private** repo'ga yuklang (`.env` yuklanmaydi, `.gitignore` da).
4. **Blueprint.** Render → New → **Blueprint** → repo'ni tanlang. `render.yaml` Redis, `streambot-api` va `streambot-keepalive` ni yaratadi.
5. **O'zgaruvchilar.** Render sahifasida to'ldiring: `BOT_TOKEN`, `DATABASE_URL`, `ENCRYPTION_KEY`.
6. **Birinchi deploydan keyin** servis URL'ini (`https://xxx.onrender.com`) nusxalab, `KEEPALIVE_URL = https://xxx.onrender.com/health` deb api va keepalive servislariga yozing.
7. Botga `/start` yuboring. Adminlarga "✅ Streambot ishga tushdi" xabari keladi.

Tekshirish: `/health` → `{"status":"ok"}`, `/health/deep` → baza va Redis holati.

### Uxlab qolmaslik
Bepul web servis trafiksiz qolsa uxlaydi. Ikki qatlam bor: (1) `render.yaml` dagi Cron Job har 10 daqiqada `/health` ni chaqiradi
(Render'da cron job pullik bo'lishi mumkin, narxini Render sahifasida tekshiring); (2) servis o'zi ham `KEEPALIVE_URL` ni ping qiladi.
Bepul variant: Cron Job blokini o'chirib, UptimeRobot yoki cron-job.org dan `/health` ga har 5-10 daqiqada ping qo'ying.

## 🛡 Fon vazifalari va monitoring

- Xotira va disk **85% / 90%** ga yetganda adminlarga ogohlantirish, kesh va vaqtinchalik fayllar avtomatik tozalanadi.
- Outbox hodisalarini yetkazish, webhook nazorati, eski yozuvlarni tozalash, davriy zaxira nusxa.
- Har vazifa Redis lock bilan himoyalangan, xato bersa boshqalarga ta'sir qilmaydi.

## 💻 Lokal ishga tushirish

```bash
cp .env.example .env        # BOT_TOKEN ni to'ldiring
docker compose up --build   # Postgres + Redis + api + bot (polling) + worker
# yoki Docker'siz:
make install && make migrate
make run-api                # alohida terminallarda: make run-bot, make run-worker
```

## 🔐 Xavfsizlik

- Token va parollar faqat environment'da, repo'da emas.
- Telegram `initData` tekshiruvi, webhook maxfiy tokeni, imzolangan muddatli stream havolalari.
- Rollar: foydalanuvchi, VIP, support, moderator, kontent menejer, admin, bosh admin; xavfli amallar audit jurnaliga yoziladi.

Batafsil: `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, `docs/RUNBOOK.md`.
