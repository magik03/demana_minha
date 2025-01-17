import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# رابط الصفحة التي ستستقبل البيانات
url = "https://wassitonline.anem.dz/postulation/prolongationDemande"

# إعداد تليغرام بوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'مرحبًا! من فضلك، أرسل أولاً رقم التسجيل في الوكالة الوطنية للتشغيل (Numéro d’inscription ANEM).'
    )

# دالة لجمع رقم التسجيل ANEM ثم طلب NIN
def handle_anem(update: Update, context: CallbackContext) -> None:
    # تخزين رقم التسجيل ANEM
    context.user_data['anem_number'] = update.message.text.strip()
    update.message.reply_text('الآن، من فضلك، أرسل رقم التعريف الوطني (Numéro d\'identification nationale - NIN).')

# دالة لإرسال البيانات إلى الموقع
def handle_nin(update: Update, context: CallbackContext) -> None:
    # الحصول على رقم NIN
    nin = update.message.text.strip()
    
    # الحصول على رقم التسجيل ANEM من البيانات المخزنة
    anem_number = context.user_data.get('anem_number')
    
    # إذا لم يتم إدخال رقم التسجيل ANEM
    if not anem_number:
        update.message.reply_text("يرجى أولاً إرسال رقم التسجيل في الوكالة الوطنية للتشغيل (ANEM).")
        return
    
    # البيانات التي سيتم إرسالها للموقع
    data = {
        "num_inscription_anem": anem_number,  # رقم التسجيل في الوكالة الوطنية للتشغيل
        "num_identification_nationale": nin,  # رقم التعريف الوطني (NIN)
    }

    # إرسال الطلب إلى الموقع
    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            update.message.reply_text("تم تقديم طلبك بنجاح! سنقوم بمعالجته في أقرب وقت.")
        else:
            update.message.reply_text(f"فشل تقديم الطلب. رمز الخطأ: {response.status_code}")
    except Exception as e:
        update.message.reply_text(f"حدث خطأ أثناء إرسال الطلب: {e}")

# إعداد البوت وتشغيله
def main():
    # استبدل هذا بالتوكن الخاص بك
    TOKEN = "7814578110:AAEow4VR3yfYreNYzNsxhs48Jzy_uusJyU4"
    updater = Updater(TOKEN)

    # إضافة المعالجين (Handlers)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_anem))  # التعامل مع رقم التسجيل
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_nin))  # التعامل مع رقم NIN

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
