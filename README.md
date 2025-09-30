# Telegram AI Bot (Deployable on Railway)

این پروژه یک ربات تلگرام ساده است که پیام‌ها را به OpenAI می‌فرستد و پاسخ را به کاربر برمی‌گرداند. با Railway یا هر سرویس میزبانی مشابه می‌توانید آن را اجرا کنید.

## فایل‌ها
- `main.py` — کد اصلی ربات (پایتون).
- `requirements.txt` — وابستگی‌ها.
- `Procfile` — دستور اجرا برای Railway.
- `README.md` — همین فایل.

## پیش‌نیازها
1. یک توکن ربات تلگرام (با BotFather) — مقدار را در متغیر محیطی `TELEGRAM_TOKEN` قرار دهید.
2. یک کلید API از OpenAI — مقدار را در متغیر محیطی `OPENAI_API_KEY` قرار دهید.
3. (اختیاری) می‌توانید مدل پیش‌فرض را با متغیر `OPENAI_MODEL` مشخص کنید (مثلاً `gpt-4` یا `gpt-3.5-turbo`). اگر مشخص نکنید، `gpt-3.5-turbo` استفاده می‌شود.

## اجرا محلی
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export TELEGRAM_TOKEN="your_telegram_token"
export OPENAI_API_KEY="your_openai_key"
python main.py
```

## استقرار در Railway
1. به https://railway.app بروید و یک پروژه جدید بسازید.
2. Repository این پروژه را آپلود یا push کنید (مثلاً با Git).
3. در تنظیمات پروژه، متغیرهای محیطی `TELEGRAM_TOKEN` و `OPENAI_API_KEY` را اضافه کنید.
4. در قسمت Deploy، Railway به طور خودکار `Procfile` را خوانده و دستور `worker: python main.py` را اجرا می‌کند.
5. پس از اجرا، ربات شروع به کار می‌کند (با polling). اگر ترجیح می‌دهید از webhook استفاده کنید، لازم است یک endpoint HTTP ایجاد و آدرس webhook را تنظیم کنید (در کد فعلی polling استفاده شده).

## نکات امنیتی
- کلیدها را هرگز در کد قرار ندهید — همیشه از متغیرهای محیطی استفاده کنید.
- برای استفاده‌ی سنگین یا کاربران زیاد، تاریخچه گفتگو را در دیتابیس ذخیره کنید نه حافظه‌ی برنامه.
- هزینه‌ی APIهای OpenAI را در نظر بگیرید.

## سفارشی‌سازی
- برای پشتیبانی از تصاویر یا فرمان‌های بیشتر، handlerهای جدید اضافه کنید.
- می‌توانید منطق cache، محدودیت نرخ یا پایگاه‌داده برای ذخیره‌ی گفتگوها اضافه کنید.

موفق باشید! اگر می‌خواهید من این پروژه را به صورت Dockerfile یا webhook-ready تغییر بدم، بگید تا همین الان اضافه‌ش کنم.
