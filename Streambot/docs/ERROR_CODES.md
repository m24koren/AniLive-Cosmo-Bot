# Xato kodlari

Format: `E` + 4 xonali raqam. Birinchi raqam toifani bildiradi.

| Toifa | Oraliq |
|---|---|
| Autentifikatsiya | E1xxx |
| Ruxsat va rollar | E2xxx |
| Tekshiruv (validatsiya) | E3xxx |
| Topilmadi / holat | E4xxx |
| Limit va cheklov | E5xxx |
| Saqlash va media | E6xxx |
| Baza, kesh | E7xxx |
| Tashqi servislar | E8xxx |
| Tizim va modullar | E9xxx |

Foydalanuvchi ko'radigan xabar tilga qarab (uz, ru, en) `shared/i18n/locales/` dan olinadi. Loglarda kod, so'rov raqami (`request_id`) va ichki tafsilot yoziladi.

## E1xxx: Autentifikatsiya

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E1001 | `initData` yo'q yoki noto'g'ri | Web App'ni Telegram ichidan oching |
| E1002 | `initData` muddati tugagan | Ilovani yopib qayta oching |
| E1003 | `initData` imzosi mos kelmadi | `BOT_TOKEN` o'zgargan bo'lishi mumkin; qayta oching |
| E1004 | Webhook maxfiy tokeni noto'g'ri | `WEBHOOK_SECRET` va `set_webhook.py` ni tekshiring |
| E1005 | Stream tokeni yaroqsiz yoki muddati tugagan | Sahifani yangilang |

## E2xxx: Ruxsat va rollar

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E2001 | Bu amal uchun ruxsat yo'q | Kerakli rol so'rang |
| E2002 | Admin huquqi kerak | Bosh admin bilan bog'laning |
| E2003 | Taklif topilmadi yoki muddati tugagan | Yangi taklif so'rang |
| E2004 | Foydalanuvchi bloklangan | Support bilan bog'laning |
| E2005 | Majburiy obuna bajarilmagan | Kanalga obuna bo'lib, qayta urining |
| E2006 | VIP obuna talab qilinadi | VIP obunani rasmiylashtiring |

## E3xxx: Tekshiruv (validatsiya)

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E3001 | Kiritilgan ma'lumot noto'g'ri formatda | Qiymatni tuzatib qayta yuboring |
| E3002 | Majburiy maydon to'ldirilmagan | Maydonni to'ldiring |
| E3003 | Qiymat juda uzun yoki juda qisqa | Uzunlikni tekshiring |
| E3004 | Fayl turi qo'llab-quvvatlanmaydi | Ruxsat etilgan formatni yuklang |
| E3005 | Fayl hajmi chegaradan oshdi | Kichikroq fayl yuklang |
| E3006 | Sahifalash parametrlari noto'g'ri | `page` va `limit` ni tekshiring |

## E4xxx: Topilmadi / holat

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E4001 | Foydalanuvchi topilmadi | `/start` yuboring |
| E4002 | Kontent topilmadi | Katalogdan qayta tanlang |
| E4003 | Qism (epizod) topilmadi | Katalogdan qayta tanlang |
| E4004 | Fayl topilmadi | Kontent menejerga xabar bering |
| E4005 | Kontent hali chiqmagan | Chiqish sanasini kuting |
| E4006 | Yozuv allaqachon mavjud | Takroran qo'shmang |

## E5xxx: Limit va cheklov

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E5001 | So'rovlar juda ko'p (rate limit) | Biroz kuting va qayta urining |
| E5002 | Bot spam himoyasi (throttle) | Tez-tez bosmang |
| E5003 | Qurilmalar limiti to'ldi | Boshqa qurilmadan chiqing |
| E5004 | Kunlik yoki oylik limit tugadi | Limit yangilanishini kuting yoki VIP oling |

## E6xxx: Saqlash va media

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E6001 | Saqlash servisi (R2/S3) ulanmadi | `STORAGE_*` sozlamalarini tekshiring |
| E6002 | Faylni yuklab bo'lmadi | Qayta urining |
| E6003 | Telegram `file_id` yaroqsiz | Faylni qayta yuklang |
| E6004 | Stream havolasini yaratib bo'lmadi | Logni tekshiring |
| E6005 | Subtitr topilmadi yoki xato | Subtitrni qayta yuklang |
| E6006 | Transcoding xatosi | `TRANSCODER` sozlamasini tekshiring |

## E7xxx: Baza, kesh

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E7001 | Bazaga ulanib bo'lmadi | `DATABASE_URL` va baza holatini tekshiring |
| E7002 | So'rov vaqti tugadi (timeout) | Qayta urining; takrorlansa logni tekshiring |
| E7003 | Migratsiya xatosi | `make migrate` va logni tekshiring |
| E7004 | Redis ulanmadi | `REDIS_URL` ni tekshiring; xotiradagi kesh ishlaydi |
| E7005 | Lock olinmadi (vazifa band) | Odatiy holat; vazifa keyinroq qayta ishlaydi |

## E8xxx: Tashqi servislar

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E8001 | Telegram API xatosi | Biroz kutib qayta urining |
| E8002 | Telegram so'rovlar chegarasi (429) | Bot o'zi kutadi; xabarlar sonini kamaytiring |
| E8003 | Foydalanuvchi botni bloklagan | Hech narsa qilmang; xabar yuborilmaydi |
| E8004 | Tashqi servis ishlamayapti (circuit breaker ochiq) | Servis tiklanishini kuting |
| E8005 | To'lov provayderi xatosi | Qayta urining yoki supportga yozing |

## E9xxx: Tizim va modullar

| Kod | Ma'nosi | Nima qilish kerak |
|---|---|---|
| E9001 | Kutilmagan ichki xato | `request_id` bilan logni toping |
| E9002 | Modul yuklanmadi | Logni tekshiring; `DISABLED_MODULES` bilan o'chirish mumkin |
| E9003 | Modul o'chirilgan | Modulni yoqish uchun `DISABLED_MODULES` dan olib tashlang |
| E9004 | Fon vazifasi xato bilan tugadi | Logni tekshiring; boshqa vazifalarga ta'sir qilmaydi |
| E9005 | Xotira yoki disk kritik chegarada | `docs/RUNBOOK.md` 3-bo'lim |
| E9006 | Sozlama yetishmayapti yoki noto'g'ri | `.env.example` bilan solishtiring |

## Yangi kod qo'shish

1. Mos toifa oralig'ida keyingi bo'sh raqamni oling.
2. `shared/errors/error_codes.py` ga qo'shing.
3. Uch tilda xabarni `shared/i18n/locales/` ga yozing.
4. Shu jadvalga qator qo'shing.
