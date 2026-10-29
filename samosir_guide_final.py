# SAMOSIR GUIDE V1.2 FINAL - TELEGRAM + LOCATION + WISATA
# BigMbolon - Samosir Island
import os, math, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

WISATA_LOKASI = [
    {"nama": "Tuk-Tuk Center", "lat": 2.686, "lon": 98.857, "desc": "Pusat turis, homestay, resto", "tiket": "Gratis", "kategori": "base"},
    {"nama": "Batu Parsidangan Ambarita", "lat": 2.681, "lon": 98.850, "desc": "Kursi batu pengadilan Batak kuno", "tiket": "20k", "kategori": "sejarah"},
    {"nama": "Museum Huta Bolon Simanindo", "lat": 2.757, "lon": 98.753, "desc": "Tarian Sigale-gale + Rumah Raja", "tiket": "20k", "kategori": "sejarah"},
    {"nama": "Makam Raja Sidabutar Tomok", "lat": 2.649, "lon": 98.882, "desc": "Makam batu 450 tahun", "tiket": "Gratis", "kategori": "sejarah"},
    {"nama": "Bukit Holbung", "lat": 2.542, "lon": 98.792, "desc": "Bukit Teletubbies, view Danau Toba", "tiket": "10k", "kategori": "alam"},
    {"nama": "Air Terjun Efrata", "lat": 2.580, "lon": 98.789, "desc": "Waterfall 30m", "tiket": "10k", "kategori": "alam"},
    {"nama": "Bukit Siadtaratas Tele", "lat": 2.738, "lon": 98.589, "desc": "View tertinggi Danau Toba", "tiket": "Gratis", "kategori": "alam"},
    {"nama": "Pantai Parbaba", "lat": 2.693, "lon": 98.831, "desc": "Pasir putih", "tiket": "10k", "kategori": "alam"},
]

JADWAL_KAPAL = """🚢 *JADWAL FERRY SAMOSIR*
*Ajibata -> Tomok:* 07:30, 09:00, 10:30, 12:00, 14:00, 15:30, 17:00
*Tomok -> Ajibata:* 08:00, 09:30, 11:00, 12:30, 14:30, 16:00, 17:30
Harga: Orang 20k, Motor 30k, Mobil 150k"""

HOMESTAY_DATA = [
    {"nama": "Toba Cottages - Tuk-Tuk", "harga": "250k/malam"},
    {"nama": "Samosir Paradise", "harga": "350k/malam"},
    {"nama": "Tabo Cottages", "harga": "200k/malam"},
]

def haversine(lat1, lon1, lat2, lon2):
    R=6371
    dlat=math.radians(lat2-lat1)
    dlon=math.radians(lon2-lon1)
    a=math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R*2*math.atan2(math.sqrt(a), math.sqrt(1-a))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🚢 Jadwal Kapal", callback_data="kapal"), InlineKeyboardButton("🏠 Homestay", callback_data="homestay")],
          [InlineKeyboardButton("🗺️ Wisata", callback_data="wisata"), InlineKeyboardButton("📍 Terdekat", callback_data="terdekat")]]
    await update.message.reply_text("Horas! Selamat datang di *Samosir Guide* 🌊\n\nPerintah:\n/kapal - Jadwal Ferry\n/homestay - List penginapan\n/wisata - 10+ lokasi wisata\n/terdekat - Share loc -> wisata terdekat\n/darurat - Nomor penting\n\nChat bebas: 'itinerary 2 hari dong'", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def kapal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(JADWAL_KAPAL, parse_mode="Markdown")
async def homestay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg="🏠 *HOMESTAY SAMOSIR*\n\n" + "\n".join([f"📍 {h['nama']} - {h['harga']}" for h in HOMESTAY_DATA])
    await update.message.reply_text(msg, parse_mode="Markdown")
async def wisata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg="🗺️ *WISATA SAMOSIR*\n\n"
    for w in WISATA_LOKASI: msg+=f"📍 *{w['nama']}* ({w['kategori']})\n   {w['desc']} | 🎟️ {w['tiket']}\n\n"
    await update.message.reply_text(msg, parse_mode="Markdown")
async def terdekat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 *FITUR TERDEKAT*\n\nShare lokasi kamu! Klik 📎 > Location > Send Current Location\nNanti aku kasih 5 wisata terdekat + jarak + link rute.", parse_mode="Markdown")
async def darurat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 *DARURAT SAMOSIR*\nPolsek: 0632-xxxx\nPuskesmas: 0812-xxxx\nBasarnas: 115")
async def lokasi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc=update.message.location; ulat, ulon=loc.latitude, loc.longitude
    sorted_w=sorted(WISATA_LOKASI, key=lambda w: haversine(ulat, ulon, w['lat'], w['lon']))
    msg=f"📍 Kamu di {ulat:.4f}, {ulon:.4f}\n\n🗺️ *5 TERDEKAT:*\n\n"
    for i,w in enumerate(sorted_w[:5],1):
        d=haversine(ulat, ulon, w['lat'], w['lon'])
        msg+=f"{i}. *{w['nama']}* - {d:.1f}km\n   {w['desc']}\n   https://maps.google.com/?q={w['lat']},{w['lon']}\n\n"
    await update.message.reply_text(msg, parse_mode="Markdown")
async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt=update.message.text.lower()
    if "itinerary" in txt or "rencana" in txt: await update.message.reply_text("Itinerary 2H1M: Hari1 Tomok & Tuk-Tuk, Hari2 Holbung & Efrata. Budget 500k/hari.")
    else: await update.message.reply_text(f"Horas! Kamu bilang: {update.message.text}. Coba /wisata atau /terdekat")
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    if q.data=="kapal": await q.edit_message_text(JADWAL_KAPAL, parse_mode="Markdown")
    elif q.data=="homestay": 
        msg="🏠 *HOMESTAY*\n" + "\n".join([f"{h['nama']} - {h['harga']}" for h in HOMESTAY_DATA]); await q.edit_message_text(msg, parse_mode="Markdown")
    elif q.data=="wisata": 
        msg="🗺️ *WISATA*\n" + "\n".join([f"{w['nama']} - {w['desc']}" for w in WISATA_LOKASI]); await q.edit_message_text(msg, parse_mode="Markdown")
    elif q.data=="terdekat": await q.edit_message_text("📍 Share lokasi kamu dulu! 📎 > Location")

if __name__=="__main__":
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kapal", kapal))
    app.add_handler(CommandHandler("homestay", homestay))
    app.add_handler(CommandHandler("wisata", wisata))
    app.add_handler(CommandHandler("terdekat", terdekat_cmd))
    app.add_handler(CommandHandler("darurat", darurat))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.LOCATION, lokasi_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_ai))
    print("Samosir Guide V1.2 running...")
    app.run_polling()￼Enter
