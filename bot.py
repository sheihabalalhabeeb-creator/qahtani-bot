import os
import telebot
import yt_dlp

TOKEN = "8606202559:AAGvQU7m57Z-RqVQ73FggJO0T6M1bFA7YWE"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت القحطاني تحميل العلوي الشادوي الحسيني 📥\nأرسل لي أي رابط فيديو أو ريلز من انستغرام أو تيك توك وسأقوم بتحميله وإرساله إليك فوراً.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    msg = bot.reply_to(message, "جاري معالجة الطلب والتحميل، يرجى الانتظار قليلاً... ⏳")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open('downloaded_video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوت القحطاني ✅")

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"عذراً، حدث خطأ أثناء التحميل أو أن الرابط غير مدعوم.", message.chat.id, msg.message_id)

    finally:
        if os.path.exists('downloaded_video.mp4'):
            os.remove('downloaded_video.mp4')

print("Bot is running...")
bot.infinity_polling()
