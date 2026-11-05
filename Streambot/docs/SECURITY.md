# Xavfsizlik

## 1. Sirlar (token, kalitlar, parollar)

- `BOT_TOKEN`, `DATABASE_URL`, `ENCRYPTION_KEY`, `SECRET_KEY`, `WEBHOOK_SECRET` **faqat environment'da** saqlanadi (Render Dashboard -> Environment).
- Ular kodda, `README`da, `.env.example`da, chatda yoki skrinshotlarda bo'lmasligi kerak.
- `.env` fayli `.gitignore` da, GitHub'ga yuklanmaydi. Repo **private** bo'lishi tavsiya etiladi.
- `SECRET_KEY` va `WEBHOOK_SECRET` ni Render o'zi yaratadi (`generateValue`).

### Token sizib chiqsa

1. @BotFather -> `/revoke` -> yangi token oling. Eski token shu zahoti ishlamay qoladi.
2. Render'da `BOT_TOKEN` ni yangilang va qayta deploy qiling.
3. `python scripts/set_webhook.py` bilan webhook'ni qayta o'rnating.
4. Token GitHub tarixiga tushgan bo'lsa, tokenni almashtirish yetarli. Faqat faylni o'chirish kifoya emas, chunki eski commit'larda qoladi.
5. Adminlar ro'yxatini va audit jurnalini tekshiring.

Kalitlarni davriy almashtirish: `scripts/rotate_secrets.py`.

## 2. Foydalanuvchini tekshirish

- **Bot:** Telegram foydalanuvchini o'zi aniqlaydi, bot `from_user.id` ga ishonadi. Webhook'ga faqat Telegram yuborganini `X-Telegram-Bot-Api-Secret-Token` sarlavhasi (`WEBHOOK_SECRET`) tasdiqlaydi. Noto'g'ri sarlavhali so'rov rad etiladi.
- **Web App:** Mini App Telegram'dan `initData` oladi. Server uni `BOT_TOKEN` asosida HMAC bilan tekshiradi (`shared/security/init_data_validator.py`) va yaroqlilik muddatini (`INIT_DATA_TTL_SECONDS`) hisobga oladi. Tekshiruvdan o'tmagan so'rov rad etiladi. Foydalanuvchi ID'si hech qachon so'rov tanasidagi qiymatdan olinmaydi, faqat tasdiqlangan `initData` dan.

## 3. Rollar va ruxsatlar

Rollar: foydalanuvchi, VIP, support, moderator, kontent menejer, admin, bosh admin.

- Bosh adminlar `SUPER_ADMIN_IDS` orqali belgilanadi.
- Har amal uchun ruxsat tekshiruvi **serverda** bajariladi (`permission_guard`). Web App'dagi tugmani yashirish himoya hisoblanmaydi.
- Xavfli amallar (rol berish, kontent o'chirish, sozlama o'zgartirish, to'lov) `audit` jurnaliga yoziladi: kim, qachon, nima.
- Admin takliflari (`invite_service`) bir martalik va muddatli.

## 4. Media himoyasi

- Stream havolalari **imzolangan va muddatli** (`STREAM_TOKEN_TTL_SECONDS`), foydalanuvchi va kontentga bog'langan.
- Bir akkauntda bir vaqtda ishlaydigan qurilmalar soni cheklangan (`DEVICE_LIMIT_DEFAULT`).
- Katta fayllar R2/S3 da saqlanganda havola vaqtinchalik (presigned) bo'lishi mumkin.

## 5. Ma'lumotlarni himoyalash

- Maxfiy maydonlar (masalan, to'lov ma'lumotlari, tashqi servis tokenlari) `ENCRYPTION_KEY` bilan Fernet orqali shifrlanadi (`shared/security/encryption.py`).
- Parol saqlanmaydi: kirish Telegram orqali.
- Loglarda token, `initData` va maxfiy maydonlar ko'rsatilmaydi.
- Bazaga barcha so'rovlar SQLAlchemy parametrlari bilan boriladi (SQL injection himoyasi).

## 6. Tarmoq himoyasi (API)

- `rate_limiter`: bir foydalanuvchi/IP uchun daqiqada so'rov limiti (`RATE_LIMIT_PER_MINUTE`).
- `security_headers`: `X-Content-Type-Options`, `Referrer-Policy`, `Content-Security-Policy` va boshqalar.
- `cors`: faqat ruxsat etilgan manzillar (`WEBAPP_URL`).
- `request_id`: har so'rovga raqam beriladi, xatoni topish oson bo'ladi.
- `ip_guard`: kerak bo'lsa admin yo'llarini IP bo'yicha cheklash.
- `error_handler`: foydalanuvchiga ichki xato tafsilotlari ko'rsatilmaydi, faqat xato kodi chiqadi.

## 7. Botni spamdan himoyalash

- `throttle_middleware`: bir foydalanuvchining tez-tez so'rovlari cheklanadi.
- `error_isolation`: bitta foydalanuvchi sabab bo'lgan xato botni to'xtata olmaydi.
- `circuit_breaker`: tashqi servis xato bersa, tizim qotib qolmaydi.

## 8. Bog'liqliklar va deploy

- Kutubxonalar `requirements/` da; vaqti-vaqti bilan yangilab, ma'lum zaifliklarni tekshiring.
- Docker konteynerlar oddiy foydalanuvchi (`appuser`) bilan ishlaydi, root bilan emas.
- `AUTO_MIGRATE` faqat tasdiqlangan migratsiyalarni qo'llaydi.

## 9. Xavfsizlik bo'yicha tekshiruv ro'yxati (deploydan oldin)

- [ ] `BOT_TOKEN` faqat Render'da, repo'da yo'q
- [ ] Repo private
- [ ] `ENCRYPTION_KEY` o'rnatilgan va zaxira joyda saqlangan
- [ ] `SUPER_ADMIN_IDS` to'g'ri
- [ ] `APP_ENV=production`
- [ ] Webhook maxfiy tokeni yoqilgan
- [ ] `/health` ishlayapti, `/docs` (Swagger) productionda yopiq yoki himoyalangan

## 10. Zaiflik topilsa

Zaiflikni ochiq joyda (chat, issue) emas, loyiha egasiga shaxsiy xabarda yuboring. Tuzatilgandan keyin tegishli kalit/tokenlar almashtiriladi va `docs/RUNBOOK.md` dagi tartib bo'yicha tekshiriladi.
