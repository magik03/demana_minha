from config import *
from requests_handler import make_request
import time
import telebot 

bot = telebot.TeleBot(bot_token)

def get_preInscriptionId(demande_number,identity_card_number):
    ### Function to return preInscriptionId.
    params = {
        'wassitNumber': demande_number,
        'identityDocNumber': identity_card_number,
        }
    return make_request(endpoint="/validateCandidate/query",
                        params=params,
                        response_type="preInscriptionId")

def get_structureId(preInscriptionId)  : 
    params = {
        'Id': preInscriptionId
    }
    return make_request(endpoint="/PreInscription/GetPreInscription",
                        params=params,
                        response_type="structureId")

def get_dates(PreInscriptionId,StructureId) : 
    params = {
        'StructureId': StructureId,
        'PreInscriptionId': PreInscriptionId,
    }
    return make_request(endpoint="/RendezVous/GetAvailableDates",
                        params=params,
                        response_type="dates")

counter = 0
message = bot.send_message(chat_id=int(chat_id),
                           text=f'جاري تشغيل البوت {counter} دقيقة')
while True : 
    counter+=1
    bot.edit_message_text(text=f"جاري تشغيل البوت {counter} دقيقة",
                          chat_id=int(chat_id),
                          message_id=message.id)
    PreInscriptionId = get_preInscriptionId(demande_number,
                                            identity_card_number)
    print(PreInscriptionId)
    StructureId =  get_structureId(PreInscriptionId)
    print(StructureId)
    Dates       = get_dates(PreInscriptionId,StructureId)
    print(Dates)
    if isinstance(Dates,list) :
        if len(Dates) == 0 : 
            bot.edit_message_text(f"موعد االبطالة لولاية الاغواط مغلق حاليا.\n عدد المحاولات {counter} محاولة \n سوف يتم إعادة محاولة بعد دقيقة {str(check_frequency_minutes)} دقيقة.",
                          chat_id=int(chat_id),
                          message_id=message.id)
        else :
            dates = "\n-"+"\n-".join(Dates)
            message = f"📣📣 New Appointements Alert 📣📣 {str(dates)}"
            bot.send_message(chat_id=chat_id,
                             text=message)
            break
    time.sleep(60*check_frequency_minutes)
    