# نشر Duel Lords على Render

## خطوات النشر على Render.com:

### 1. إعداد المشروع
- تأكد من وجود ملف `main.py` (موجود ✓)
- تأكد من وجود `pyproject.toml` (موجود ✓)
- تم إنشاء `start.sh` للتشغيل (موجود ✓)

### 2. إنشاء خدمة على Render
1. انتقل إلى [render.com](https://render.com)
2. اضغط "New" ثم "Web Service"
3. اربط حساب GitHub الخاص بك
4. اختر مستودع المشروع

### 3. إعدادات الخدمة
- **Name**: `duel-lords-bot`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r pyproject.toml`
- **Start Command**: `bash start.sh`

### 4. متغيرات البيئة المطلوبة
أضف في Environment Variables:
```
DISCORD_TOKEN = [توكن البوت الخاص بك]
```

### 5. إعدادات إضافية
- **Auto-Deploy**: مفعل
- **Health Check Path**: `/health`

## ملاحظات مهمة:
- البوت سيعمل 24/7 على Render
- لوحة التحكم ستكون متاحة على المنفذ الذي يحدده Render
- تأكد من إضافة DISCORD_TOKEN في إعدادات Environment Variables
- Keep-alive موجود للحفاظ على عمل البوت

## الميزات المتاحة:
✓ 13 أمر Discord متزامن
✓ نظام إدارة البطولات
✓ تسجيل اللاعبين (للمشرفين فقط)
✓ جدولة المبارزات مع التذكيرات
✓ إحصائيات اللاعبين
✓ لوحة تحكم ويب
✓ دعم متعدد اللغات