services:
  - type: web
    name: shuha-bot
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wsgi:app
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: PHOTO_URL
        sync: false
      - key: MY_TELEGRAM_ID
        sync: false
