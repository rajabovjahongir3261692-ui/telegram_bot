from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

TOKEN = "8465457182:AAGdTzfUmqQCehHJK-D56Cq4Pr9p5I2Qt-I"

# Savollar ro'yxati
questions = [
    {"text": "1. Kursingiz:", "type": "choice", "options": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "🎓 Magistratura"]},
    {"text": "2. Yo‘nalishingiz:", "type": "text"},
    {"text": "3. Jinsingiz:", "type": "choice", "options": ["👨 Erkak", "👩 Ayol"]},
    {"text": "4. Ta’lim shakli:", "type": "choice", "options": ["🏫 Kunduzgi", "🌙 Sirtqi", "🌃 Kechki", "💻 Masofaviy"]},

    {"text": "5. O‘qituvchilarning mavzuni tushuntirish darajasidan qanchalik qoniqasiz?", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Past"]},
    {"text": "6. O‘qituvchilar sizning fikrlaringiz va savollaringizni tinglaydilarmi?", "type": "choice",
     "options": ["✅ Ha, doim", "⏱ Ko‘pincha", "❓ Ba’zan", "❌ Hech qachon"]},
    {"text": "7. O‘qituvchilar zamonaviy o‘qitish usullari (multimedia, interaktiv metodlar)dan foydalanadimi?", "type": "choice",
     "options": ["🎬 Juda ko‘p", "✔ Yetarli", "⚠ Juda kam", "❌ Umuman yo‘q"]},
    {"text": "8. O‘qituvchilar talabalarga hurmat bilan munosabatda bo‘lishadimi?", "type": "choice",
     "options": ["✅ Ha, doim", "⏱ Ko‘pincha", "⚠ Kamdan-kam", "❌ Yo‘q"]},
    {"text": "9. O‘qituvchilarning siz uchun eng tajribali va salohiyatlilari qaysilar:", "type": "text"},
    {"text": "10. O‘qituvchilarning siz uchun qaysilari o’z kasbiga nolayiq deb bilasiz:", "type": "text"},

    {"text": "11. Sizning yo‘nalishingiz bo‘yicha o‘quv dasturi dolzarb va zamon talablariga mosmi?", "type": "choice",
     "options": ["✅ To‘liq mos", "⚠ Qisman mos", "❌ Yetarli emas", "❌ Mos emas"]},
    {"text": "12. O‘quv dasturida nazariya va amaliyot uyg‘unligi qay darajada ta’minlangan?", "type": "choice",
     "options": ["🌟 Juda yuqori", "👍 Yaxshi", "👌 O‘rtacha", "😕 Past"]},
    {"text": "13. O‘quv rejadagi fanlar sizni kelajakdagi kasbiy faoliyatga tayyorlashda foydalimi?", "type": "choice",
     "options": ["🌟 Juda foydali", "👍 Foydali", "⚠ Qisman foydali", "❌ Foydasiz"]},
    {"text": "14. Baholash tizimi sizning bilim va ko‘nikmalaringizni adolatli baholaydimi?", "type": "choice",
     "options": ["✅ Ha, adolatli", "⚠ Qisman adolatli", "❌ Adolatsiz"]},

    {"text": "15. Auditoriyalar, laboratoriyalar va texnik vositalar bilan ta’minlanish darajasi:", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Qoniqarsiz"]},
    {"text": "16. Kutubxona, elektron bazalar va internet imkoniyatlari yetarlimi?", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Qoniqarsiz"]},
    {"text": "17. Yotoqxona va talabalar turar joyi sharoitidan qoniqasizmi?", "type": "choice",
     "options": ["🌟 Juda qoniqaman", "👍 Qoniqaman", "⚠ Qisman", "❌ Qoniqmayman"]},
    {"text": "18. Universitetdagi ovqatlanish joylari, sport inshootlari, Wi-Fi va boshqa qulayliklar yetarlimi?", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Past"]},

    {"text": "19. O‘quv amaliyotlari va ishlab chiqarish bilan hamkorlik yetarli darajada yo‘lga qo‘yilganmi?", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Qoniqarsiz"]},
    {"text": "20. Amaliyotlar sizning kasbiy ko‘nikmalaringizni rivojlantiradimi?", "type": "choice",
     "options": ["✅ Ha, to‘liq", "⚠ Qisman", "😕 Juda kam", "❌ Yo‘q"]},
    {"text": "21. Ilmiy-tadqiqot ishlari va talabalar tashabbuslarini qo‘llab-quvvatlash darajasi:", "type": "choice",
     "options": ["🌟 Juda yuqori", "👍 Yaxshi", "👌 O‘rtacha", "😕 Past"]},
    {"text": "22. Akademik mobillik imkoniyatlari haqida yetarlicha ma’lumot bormi?", "type": "choice",
     "options": ["🌟 Juda ko‘p", "👍 Yetarli", "⚠ Juda kam", "❌ Yo‘q"]},

    {"text": "23. Universitetda madaniy-ma’naviy tadbirlar muntazam o‘tkaziladimi?", "type": "choice",
     "options": ["🌟 Juda faol", "👍 Faol", "⚠ Kamdan-kam", "❌ Umuman yo‘q"]},
    {"text": "24. Talabalarning sport va sog‘lomlashtirish faoliyati yo‘lga qo‘yilganmi?", "type": "choice",
     "options": ["🌟 Juda yaxshi", "👍 Yaxshi", "👌 O‘rtacha", "😕 Past"]},
    {"text": "25. Universitet rahbariyati talabalar murojaatlariga tezkor javob beradimi?", "type": "choice",
     "options": ["✅ Ha, doim", "⏱ Ko‘pincha", "❓ Ba’zan", "❌ Hech qachon"]},
    {"text": "26. Universitet psixologik va maslahat xizmatlaridan qoniqasizmi?", "type": "choice",
     "options": ["🌟 Juda qoniqaman", "👍 Qoniqaman", "⚠ Qisman", "❌ Qoniqmayman"]},

    {"text": "27. Siz universitetingizdagi ta’lim sifatidan qanchalik qoniqasiz?", "type": "choice",
     "options": ["🌟 Juda qoniqaman", "👍 Qoniqaman", "⚠ Qisman", "❌ Qoniqmayman"]},
    {"text": "28. Universitetingizni boshqa abituriyentlarga tavsiya qilasizmi?", "type": "choice",
     "options": ["✅ Albatta", "⚠ Ehtimol", "❓ Ikkilanishim mumkin", "❌ Yo‘q"]},
    {"text": "29. Sizning fikringizcha, ta’lim sifatini oshirish uchun eng asosiy ustuvor yo‘nalishlar nimalardan iborat?", "type": "text"},
]

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "📋 *TALABALAR UCHUN SO‘ROVNOMA - Namangan davlat texnika universiteti*\n\n"
        "Hurmatli talaba! Ushbu so‘rovnomadagi savollarga samimiy va xolisona javob berishingiz "
        "Oliy ta’lim muassasasida ta’lim sifatini yanada oshirishga yordam beradi.\n\n"
        "❗So‘rovnoma anonim tarzda o‘tkaziladi va natijalar faqat ta’lim sifatini yaxshilash maqsadida foydalaniladi."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    context.user_data["q_index"] = 0
    context.user_data["answers"] = []
    await send_question(update, context)

# Savol yuborish
async def send_question(update, context):
    index = context.user_data["q_index"]
    if index >= len(questions):
        await update.message.reply_text("✅ So‘rovnoma yakunlandi. Javoblaringiz qabul qilindi. Rahmat!")
        return

    q = questions[index]
    if q["type"] == "choice":
        keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.callback_query:
            await update.callback_query.message.edit_text(q["text"], reply_markup=reply_markup)
        else:
            await update.message.reply_text(q["text"], reply_markup=reply_markup)
    else:
        if update.callback_query:
            await update.callback_query.message.reply_text(q["text"])
        else:
            await update.message.reply_text(q["text"])

# Inline tugmalar bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["answers"].append(query.data)
    context.user_data["q_index"] += 1
    await send_question(update, context)

# Matn javoblarini qabul qilish
async def text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data["q_index"]
    q = questions[index]
    if q["type"] == "text":
        context.user_data["answers"].append(update.message.text)
        context.user_data["q_index"] += 1
        await send_question(update, context)

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_answer))
    
    keep_alive()
    print("Bot ishga tushdi...")
    app.run_polling()
