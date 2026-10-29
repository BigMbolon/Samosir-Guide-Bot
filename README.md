# Samosir Guide 🌊 — AI Guide for Lake Toba

> Horas! Your 24/7 bilingual (ID/EN) guide for Samosir Island.

One brain, two platforms: **Telegram + WhatsApp**. Built for tourists, owned by locals.

Live Bot: [@SamosirGuideBot on Telegram](https://t.me/SamosirGuideBot) | WA: soon

### ✨ Features V1
- 🚢 `/kapal` - Ferry schedule Ajibata ↔ Tomok (real-time ready)
- 🏠 `/homestay` - Curated homestays in Tuk-Tuk (200k-350k)
- 🗺️ AI Itinerary - "2D1N family trip" auto-generated
- 🍜 Kuliner Batak - Naniura, Saksang, Mie Gomak
- ⛅ `/cuaca` - Lake Toba weather (BMKG integration V2)
- 🆘 `/darurat` - Emergency contacts
- Bilingual ID/EN auto-detect

### 🛠️ Tech Stack
- Python + python-telegram-bot
- Flask (for WhatsApp webhook)
- Meta WhatsApp Business API
- Google Sheets as CMS (no-code edit for homestay owners)

### 🚀 Quick Start
```bash
git clone https://github.com/kamu/samosir-guide-bot
pip install -r requirements.txt
export BOT_TOKEN="your_token_from_BotFather"
python samosir_guide_v1.py
