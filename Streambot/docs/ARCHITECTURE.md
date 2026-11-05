# Streambot arxitekturasi

## Asosiy g'oya

Bot tugmalari va Web App **bir xil servislarni** chaqiradi. Shuning uchun biror amal (masalan, kinoni sevimlilarga qo'shish) ikkala joyda ham bir xil ishlaydi va qoidalar bitta joyda yoziladi.

Ikkinchi g'oya: **bitta qism buzilsa, qolganlari ishlashda davom etadi.** Har modul mustaqil "quti", har biri alohida yuklanadi.

## Qatlamlar

```
apps/      ishga tushiriladigan jarayonlar: bot_app, api_app, worker_app
modules/   funksiyalar (catalog, roles, media, player, ...)
shared/    poydevor: config, database, cache, storage, security, events, i18n, telegram, utils
```

Bog'lanish yo'nalishi faqat pastga qarab:

- `apps` -> `modules` -> `shared`
- `shared` hech qachon `modules` yoki `apps` ni import qilmaydi (kam istisnolar `.importlinter` da yozilgan).
- Modul boshqa modulning ichki fayllariga kirmaydi. Faqat uning `public.py` fayli orqali murojaat qiladi.

Bu qoidalar `lint-imports` buyrug'i bilan avtomatik tekshiriladi (`make lint`).

## Jarayonlar

| Jarayon | Vazifasi |
|---|---|
| `api_app` | FastAPI: Telegram webhook, Web App uchun API, statik fayllar. Render'dagi asosiy servis |
| `bot_app` | Polling rejimidagi bot (lokal ishlab chiqish uchun) |
| `worker_app` | Fon vazifalari: kesh tozalash, xotira va disk nazorati, outbox yetkazish, zaxira |

`WORKER_EMBEDDED=true` bo'lsa, fon vazifalari `api_app` ichida ishlaydi (bepul Render rejasi uchun qulay). `false` bo'lsa, alohida `worker_app` ishlatiladi.

## Modul tuzilmasi

Har modul ichida:

| Fayl | Vazifasi |
|---|---|
| `manifest.py` | Modul nomi, versiyasi, bog'liqliklari, ulanish nuqtalari |
| `public.py` | Boshqa modullar uchun yagona ochiq eshik |
| `service.py` | Biznes qoidalari |
| `repository.py` | Bazaga murojaat |
| `domain/` | Modellar, enumlar, istisnolar |
| `schemas.py` | API uchun kirish/chiqish shakllari |
| `permissions.py` | Modul ruxsatlari |
| `events.py` | Modul yuboradigan hodisalar |
| `tasks.py` | Modulning fon vazifalari |

`module_loader` har modulni alohida `try/except` ichida yuklaydi. Biror modul yuklanmasa, xato jurnalga yoziladi, adminlarga xabar boradi, qolgan modullar ishlayveradi. Modulni o'chirish uchun `DISABLED_MODULES=recommendations,referral` kifoya.

## So'rov yo'li

**Bot:** Telegram -> webhook (`api_app`) -> aiogram dispatcher -> middleware'lar -> modul adapteri -> `service` -> `repository` -> baza.

**Web App:** Mini App -> `api_app` -> `init_data_auth` (Telegram `initData` tekshiruvi) -> router -> `service` -> `repository` -> baza.

Ikkala yo'l ham o'rtada bir xil `service` ga tushadi.

### Bot middleware'lari (tartib bilan)

1. `error_isolation`: xatoni ushlaydi, bitta foydalanuvchi xatosi botni to'xtatmasin
2. `i18n`: foydalanuvchi tilini aniqlaydi (uz, ru, en)
3. `throttle`: spamdan himoya
4. `role`: foydalanuvchi rolini aniqlaydi
5. `subscription_gate`: majburiy obuna tekshiruvi
6. `audit`: xavfli amallarni jurnalga yozadi

### API middleware'lari

`request_id`, `security_headers`, `cors`, `rate_limiter`, `init_data_auth`, `error_handler`.

## Ma'lumotlar

- **Baza:** PostgreSQL, SQLAlchemy (async). Migratsiyalar Alembic bilan (`shared/database/migrations`). `AUTO_MIGRATE=true` bo'lsa, ishga tushganda avtomatik qo'llanadi.
- **Repository + Unit of Work:** modul bazaga faqat repository orqali murojaat qiladi; bir necha amal bitta tranzaksiyada bajariladi.
- **Kesh:** Redis. `REDIS_URL` bo'sh bo'lsa, xotiradagi vaqtinchalik kesh ishlaydi (faqat bitta nusxa uchun).
- **Lock:** fon vazifalari Redis lock bilan himoyalangan, bir vazifa ikki marta parallel ishlamaydi.

## Media saqlash

`STORAGE_BACKEND` orqali tanlanadi:

- `telegram`: Telegram `file_id` (sozlash shart emas; 20 MB dan katta videoni Web App'da oqimlash qiyin)
- `r2` yoki `s3`: katta videolar va Web App'da oqimlash uchun

Hammasi `base_storage` interfeysi orqasida, shuning uchun backend almashtirilsa, modullar o'zgarmaydi.

## Hodisalar va Outbox

Modullar bir-birini to'g'ridan-to'g'ri chaqirish o'rniga hodisa yuboradi (`event_bus`). Muhim hodisalar avval bazadagi `outbox` jadvaliga yoziladi, keyin worker ularni yetkazadi. Shunda server o'chib qolsa ham hodisa yo'qolmaydi.

## Xatolardan himoya

- `error_boundary`: har vazifa va handler alohida himoyalangan
- `circuit_breaker`: tashqi servis (Telegram, R2) ketma-ket xato bersa, vaqtincha o'chiriladi va tizim qotib qolmaydi
- `error_codes`: har xatoning o'z kodi bor (`docs/ERROR_CODES.md`)
- Xotira va disk 85% / 90% ga yetganda adminlarga ogohlantirish va avtomatik tozalash

## Xavfsizlik (qisqacha)

Token va kalitlar faqat environment'da. Telegram `initData` imzosi tekshiriladi, webhook maxfiy token bilan himoyalangan, stream havolalari imzolangan va muddatli. Batafsil: `docs/SECURITY.md`.

## Ko'p tillilik

`shared/i18n/locales/` ichida `uz.json`, `ru.json`, `en.json`. Standart til `DEFAULT_LANG`, foydalanuvchi o'zi almashtira oladi.
