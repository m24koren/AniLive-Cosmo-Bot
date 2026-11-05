# Streambot buyruqlari. Ishlatish:  make <buyruq>     (ro'yxat: make help)
# Eslatma: buyruq qatorlari TAB o'rniga ">" belgisi bilan boshlanadi, shuning uchun
# matnni nusxalaganda bo'shliq/tab muammosi chiqmaydi.
.RECIPEPREFIX = >
.DEFAULT_GOAL := help
.PHONY: help install run-api run-bot run-worker migrate revision lint test parity \
        seed-admin backup webhook up down

help:  ## Buyruqlar ro'yxati
> @grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-12s %s\n", $$1, $$2}'

install:  ## Kutubxonalarni o'rnatish (ishlab chiqish uchun)
> pip install -r requirements/dev.txt

run-api:  ## API + webhook + Web App (lokal, o'zgarishda qayta yuklanadi)
> uvicorn apps.api_app.main:app --host 0.0.0.0 --port $${PORT:-8000} --proxy-headers --forwarded-allow-ips="*" --reload

run-bot:  ## Botni polling rejimida ishga tushirish (BOT_MODE=polling kerak)
> python -m apps.bot_app.main

run-worker:  ## Alohida fon vazifalari jarayoni
> python -m apps.worker_app.main

migrate:  ## Baza migratsiyasini qo'llash
> alembic upgrade head

revision:  ## Yangi migratsiya yaratish: make revision m="izoh"
> alembic revision --autogenerate -m "$(m)"

lint:  ## Kod va arxitektura qoidalarini tekshirish
> ruff check . && lint-imports

test:  ## Testlarni ishga tushirish
> pytest -q

parity:  ## Bot va Web App funksiyalari tengligini tekshirish
> python scripts/check_parity.py

seed-admin:  ## Bosh adminni bazaga yozish (SUPER_ADMIN_IDS dan)
> python scripts/seed_super_admin.py

backup:  ## Bazaning zaxira nusxasini olish
> python scripts/backup_database.py

webhook:  ## Telegram webhook holatini ko'rish
> python scripts/set_webhook.py --info

up:  ## Docker bilan hammasini ishga tushirish (Postgres + Redis + api + bot + worker)
> docker compose up --build

down:  ## Docker'ni to'xtatish
> docker compose down
