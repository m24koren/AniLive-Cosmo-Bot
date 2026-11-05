# Bot va Web App tengligi (Feature Parity)

## Qoida

Foydalanuvchi uchun har funksiya **ham botda, ham Web App'da** ishlashi kerak va ikkalasi **bir xil servisni** chaqiradi. Ikki joyda alohida mantiq yozilmaydi.

Istisno faqat texnik sababli bo'lishi mumkin va jadvalda `➖` belgisi bilan, izoh ustunida sababi yoziladi (masalan, katta video oqimlash faqat Web App'da qulay).

Yangi funksiya qo'shilganda shu jadvalga qator qo'shiladi. `make parity` jadval bilan haqiqiy kodni solishtirib, yetishmayotgan joyni ko'rsatadi.

## Jadval

| Funksiya | Modul | Bot | Web App |
|---|---|---|---|
| Ro'yxatdan o'tish va profil | users | ✅ | ✅ |
| Til tanlash (uz, ru, en) | settings | ✅ | ✅ |
| Katalogni ko'rish (anime, kino, multfilm, donghua, drama) | catalog | ✅ | ✅ |
| Janr va kategoriya bo'yicha filtr | catalog | ✅ | ✅ |
| Qidiruv | search | ✅ | ✅ |
| Kontent kartochkasi (tavsif, fasllar, qismlar) | catalog | ✅ | ✅ |
| Qism ko'rish / yuklash | player | ✅ | ✅ |
| Videoni Web App ichida oqimlash | player | ➖ | ✅ |
| Subtitr tanlash | media | ✅ | ✅ |
| Ko'rish davomi (qaysi joyda to'xtagan) | player | ✅ | ✅ |
| Sevimlilar va kutubxona | library | ✅ | ✅ |
| Majburiy obuna tekshiruvi | subscriptions | ✅ | ✅ |
| VIP obuna | vip | ✅ | ✅ |
| To'lovlar | payments | ✅ | ✅ |
| Qurilmalar limiti | player | ➖ | ✅ |
| Qo'llab-quvvatlash (murojaat yuborish) | support | ✅ | ✅ |
| Kontent yuklash (admin) | media | ✅ | ✅ |
| Ommaviy yuklash (admin) | media | ➖ | ✅ |
| Chiqish rejasi (admin) | media | ✅ | ✅ |
| Rollar va takliflar (admin) | roles | ✅ | ✅ |
| Rejim almashtirish (foydalanuvchi / admin) | roles | ✅ | ✅ |
| Audit jurnali (admin) | audit | ✅ | ✅ |

## Izohlar

- **Videoni oqimlash:** Telegram botda video fayl sifatida yuboriladi. Web App'da esa imzolangan muddatli havola orqali oqimlanadi (`STORAGE_BACKEND=r2` yoki `s3` bo'lsa eng yaxshi ishlaydi).
- **Qurilmalar limiti:** qurilma Web App sessiyalari orqali hisoblanadi, botda "qurilma" tushunchasi yo'q.
- **Ommaviy yuklash:** ko'p fayl tanlash va jarayonni ko'rsatish Web App'da qulay. Botda bitta-bitta yuklash bor.

## Tekshirish

```bash
make parity
```

Skript jadvaldagi `✅` qatorlar uchun tegishli modulda bot adapteri (`adapters/bot`) va API adapteri (`adapters/api`) borligini tekshiradi. Yetishmasa xato bilan chiqadi.
