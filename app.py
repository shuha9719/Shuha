import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Берем токены из настроек безопасности Render (Environment Variables)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Прямая ссылка на фото image.png, загруженное на фотохостинг (например, imgbb)
PHOTO_URL = os.environ.get("PHOTO_URL") 
# Ваш личный Telegram ID, чтобы бот дублировал вам информацию о новых записях
MY_TELEGRAM_ID = os.environ.get("MY_TELEGRAM_ID")

@app.route('/dikidi-webhook', methods=['POST'])
def dikidi_webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
        
    # Вытаскиваем данные о клиенте и записи из DIKIDI
    # (Структура полей может слегка отличаться в зависимости от версии API DIKIDI, 
    # этот вариант адаптирован под стандартный webhook передачи данных клиента)
    client_name = data.get('client', {}).get('name', 'Гость')
    client_phone = data.get('client', {}).get('phone', '')
    
    # Извлекаем дату и время визита
    session_date = data.get('date', 'ближайшее время')
    session_time = data.get('time', '')
    
    # Текст сообщения для клиента
    text_message = (
        f"Привет, {client_name}! Ваша запись в студию S&h подтверждена. 🎉\n\n"
        f"📅 Дата: {session_date} в {session_time}\n\n"
        "Если вы у нас впервые, держите мини-инструкцию:\n"
        "📍 Вход в студию находится со двора.\n"
        "🚪 На двери нажимайте **9 на домофоне**.\n"
        "Фото входа прикрепил ниже 👇"
    )

    # Ищем Telegram ID клиента. Чтобы это работало идеально, 
    # клиент должен запустить бота, а его ID должен передаваться из DIKIDI 
    # или сопоставляться по номеру телефона в вашей мини-базе.
    client_tg_id = data.get('client', {}).get('telegram_id') 

    # Если Telegram ID клиента успешно передан из CRM
    if client_tg_id:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": client_tg_id,
            "photo": PHOTO_URL,
            "caption": text_message,
            "parse_mode": "Markdown"
        }
        requests.post(telegram_url, json=payload)
    
    # Оповещение мастера (вас) в Telegram о том, что вебхук сработал
    if MY_TELEGRAM_ID:
        notify_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        master_text = (
            f"🔔 Новая запись в DIKIDI!\n"
            f"👤 Клиент: {client_name} ({client_phone})\n"
            f"⏰ Время: {session_date} в {session_time}\n\n"
            f"ℹ️ Попытка отправить инструкцию: "
            f"{'Успешно (TG ID найден)' if client_tg_id else 'TG ID клиента не передан. Отправьте вручную.'}"
        )
        requests.post(notify_url, json={
            "chat_id": MY_TELEGRAM_ID,
            "text": master_text
        })

    return jsonify({"status": "success"}), 200
