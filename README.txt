ИНСТРУКЦИЯ ПО ЗАПУСКУ БОТА ДЛЯ DIKIDI НА RENDER
==================================================

В этой папке находятся 3 файла, необходимые для работы вашего автоматического помощника.

1. requirements.txt — список библиотек для сервера.
2. wsgi.py — файл для правильного запуска веб-сервера.
3. app.py — основной код логики.

ЧТО ДЕЛАТЬ ДАЛЬШЕ:
-----------------
1. Создайте приватный (Private) репозиторий на GitHub.
2. Загрузите туда файлы: app.py, wsgi.py, requirements.txt.
3. Зарегистрируйтесь на Render.com через ваш GitHub-аккаунт.
4. Нажмите New + -> Web Service и выберите этот репозиторий.
5. Настройки на Render:
   - Language: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn wsgi:app
   - Тариф: Free (Бесплатный)
6. В разделе 'Environment Variables' (Переменные окружения) на Render обязательно добавьте:
   - BOT_TOKEN : токен вашего бота из @BotFather
   - PHOTO_URL : прямая ссылка на фото вашей двери (image.png)
   - MY_TELEGRAM_ID : ваш личный ID в Telegram (чтобы бот присылал вам уведомления о записях)

7. Полученную ссылку от Render (например, https://my-bot.onrender.com/dikidi-webhook) 
   вставьте в настройки Вебхуков в DIKIDI Business.
