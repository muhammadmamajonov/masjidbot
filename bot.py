from telegram import Update, ReplyKeyboardMarkup, Audio, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext,ConversationHandler,MessageHandler, Filters,  CallbackQueryHandler
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

# https://api.telegram.org/bot1403694100:AAGGxtJ_eL5wP4hgi4dogc0kj_kdo9gzScQ/setWebhook?url=https://masjid.algorithmgateway.uz/masjidbot/

token = '1403694100:AAGGxtJ_eL5wP4hgi4dogc0kj_kdo9gzScQ'
updater = Updater(token)
# BOT_NAME = 'masjid_namozvaqti_bot'
# certificate = "/etc/letsencrypt/live/masjid.algorithmgateway.uz/fullchain.pem"
# updater.start_webhook(listen='45.87.2.71',
#                     port=22,
#                     url_path=token,
#                     key='hsb2#x!t!6anm)&#2&wgoro$u1y_dk!0lmnk8i9*4r7t21b4s6',
#                     cert=certificate,
#                     webhook_url='https://masjid.algorithmgateway.uz/1403694100:AAGGxtJ_eL5wP4hgi4dogc0kj_kdo9gzScQ')

# updater.bot.set_webhook("https://masjid.algorithmgateway.uz/masjidbot/" + token)

# class MasjidBot(APIView):
#     def post(self, request):
#         json_string = request.body.decode('UTF-8')
#         update = Update.de_json(json_string)
#         updater.process_new_updates([update])
#         return Response({'code': 200})

url = 'https://masjid.algorithmgateway.uz/'
tanlov = ''
tugmalar = ReplyKeyboardMarkup([['Maruzalar'], ['Namoz vaqti'], ['Darslar']], resize_keyboard=True)

s = 0
t = 0
p = 1
   
def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Assalomu alaykum {update.effective_user.first_name} masjidimiz botiga xush kelibsiz', reply_markup = tugmalar)
    return 1


def Namozvaqti(update: Update, context: CallbackContext):
    bugun = datetime.today().date()
    n = requests.get('{}api/namozvaqti'.format(url))
    data = json.loads(n.text) 
    for i in data['d']:
        if i['sana'] == str(bugun):
            update.message.reply_html("<b> Bugun : {}</b> \n\n  {} | <b>Andijon vaqti</b> \n\n ⏰<b>Tong(saharlik)</b> : {}\n\n ⏰<b>Quyosh</b> :  {}\n\n ⏰<b>Peshin</b> : {} \n\n ⏰<b>Asr</b> : {} \n\n ⏰<b>Shom(iftor)</b> : {} \n\n ⏰<b>Xufton</b> : {}".format(i['sana'], i['hafta_kuni'], i['tong'], i['quyosh'], i['peshin'], i['asr'], i['shom'], i['xufton'] ), reply_markup = tugmalar)
        else:
            print('sana togri kelmadi')
    
######################### Maruzalar ####################

def Maruzalar(update: Update, context: CallbackContext):
    global tanlov
    tanlov = 'maruza'
    m = requests.get('{}api/audio-maruzalar'.format(url))
    data = json.loads(m.text)
    print(data)
    
    print(len(data['d']), "data len")
    matn = ''
    
    global s, t
    s = 0
    t = 0
    tugmalar = [
                [
                    InlineKeyboardButton('{}'.format(s = s+1), callback_data=s),
                    InlineKeyboardButton('{}'.format(s = s+1), callback_data=s),
                    InlineKeyboardButton('{}'.format(s = s+1), callback_data=s),
                    InlineKeyboardButton('{}'.format(s = s+1), callback_data=s),
                    InlineKeyboardButton('{}'.format(s = s+1), callback_data=s),  
                ],
                [
                    InlineKeyboardButton('>>', callback_data= '>>')
                ]
            ]
    for a in data['d'][:5]:
        t += 1
        matn += '<b>{}. {} \n\t\t\t\t{} \n\n</b>'.format(t, a['maruza_nomi'], a['muallif'])
        
    update.message.reply_html(matn, reply_markup=InlineKeyboardMarkup(tugmalar))
   

############################## Mavzular ##################################################
tm = 0
sm = 0
def Mavzular(update: Update, context: CallbackContext):
    m = requests.get('{}api/mavzular'.format(url))
    data = json.loads(m.text)
    global tanlov
    tanlov = 'mavzu'
    global sm, tm
    sm = 0
    tm = 0
    matn = ''
    tugma = []
    for i in range(len(data['d'][tm:tm+5])):
        tugma.append(InlineKeyboardButton('{}'.format(sm = sm+1), callback_data=sm))
        # tugmalar_soni +=1
    tugmalar = [tugma]
    if len(data['d']) > 5:
        tugmalar.append([
                InlineKeyboardButton('>>', callback_data= 'm>>'), 
            ])

    for a in data['d'][:5]:
        tm += 1
        matn += '<b>{}. {} \n\t\t\t\t \n\n</b>'.format(tm, a['mavzu'])
        
    update.message.reply_html(matn, reply_markup=InlineKeyboardMarkup(tugmalar))

############################## Inline Call_back ##################################################
tugmalar_soni=0
data = ''
tug = ''
tugma = []
def inline_callback(update, context):
    global tugmalar_soni
    
    m = requests.get('{}api/audio-maruzalar'.format(url))
    data = json.loads(m.text)
    matn = ''
    global t, p, s
    tugmalar = []
    try:
        query = update.callback_query

        if query.data == '>>':
            tugma.clear()
            if t+5 > len(data['d']):
                tugmalar_soni = 0
                for i in range(len(data['d'][t:])):
                    tugma.append(InlineKeyboardButton('{}'.format(s = s+1), callback_data=s))
                    tugmalar_soni +=1
                tugmalar = [tugma]
            
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<'), 
                        
                    ]
                )
            else:
                for i in range(len(data['d'][t:t+5])):
                    tugmalar_soni +=1
                    tugma.append(InlineKeyboardButton('{}'.format(s = s+1), callback_data=s))
                tugmalar = [tugma]
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<'),
                        InlineKeyboardButton('>>', callback_data= '>>'),  
                    ]
                )
            
            for a in data['d'][t:t+5]:
                print('forni ichida s:', s)
                print('forni ichida t:', t)
                t = t+1
                matn += '<b>{}. {} \n\t\t\t\t{} \n\n</b>'.format(t, a['maruza_nomi'], a['muallif'])
            query.edit_message_text(text = matn, reply_markup=InlineKeyboardMarkup(tugmalar), parse_mode="HTML")

        elif query.data == '<<':
            tugma.clear()
            s -= tugmalar_soni + 5
            t -= tugmalar_soni + 5
            tugmalar_soni = 0
            for i in range(len(data['d'][t:t+5])):
                tugmalar_soni += 1
                tugma.append(InlineKeyboardButton('{}'.format(s = s+1), callback_data=s))
               
            
            tugmalar = [tugma]
            if data['d'][t] == data['d'][0]:
                tugmalar.append(
                [
                    InlineKeyboardButton('>>', callback_data= '>>')
                ]
            )
            else:
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<'), 
                        InlineKeyboardButton('>>', callback_data= '>>')
                    ]
                )

            for a in data['d'][t:t+5]:
                t = t+1
                matn += '<b>{}. {} \n\t\t\t\t{} \n\n</b>'.format(t, a['maruza_nomi'], a['muallif'])
            query.edit_message_text(text = matn, reply_markup=InlineKeyboardMarkup(tugmalar), parse_mode="HTML")
##################################### Mavzu #############################################################
        elif query.data == 'm>>':
            m = requests.get('{}api/mavzular'.format(url))
            data = json.loads(m.text)
            tugma.clear()
            global sm, tm
            if tm+5 > len(data['d']):
                tugmalar_soni = 0
                for i in range(len(data['d'][tm:])):
                    tugma.append(InlineKeyboardButton('{}'.format(sm = sm+1), callback_data=sm))
                    tugmalar_soni +=1
                tugmalar = [tugma]
            
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<m'), 
                        
                    ]
                )
            else:
                for i in range(len(data['d'][tm:tm+5])):
                    tugmalar_soni +=1
                    tugma.append(InlineKeyboardButton('{}'.format(sm = sm+1), callback_data=sm))
                tugmalar = [tugma]
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<m'),
                        InlineKeyboardButton('>>', callback_data= 'm>>'),  
                    ]
                )
            
            for a in data['d'][tm:tm+5]:
                tm = tm+1
                matn += '<b>{}. {} \n\t\t\t\t \n\n</b>'.format(tm, a['mavzu'])
            query.edit_message_text(text = matn, reply_markup=InlineKeyboardMarkup(tugmalar), parse_mode="HTML")

        elif query.data == '<<m':
            m = requests.get('{}api/mavzular'.format(url))
            data = json.loads(m.text)
            tugma.clear()
            sm -= tugmalar_soni + 5
            tm -= tugmalar_soni + 5
            tugmalar_soni = 0
            for i in range(len(data['d'][tm:tm+5])):
                tugmalar_soni += 1
                tugma.append(InlineKeyboardButton('{}'.format(sm = sm+1), callback_data=sm))
               
            
            tugmalar = [tugma]
            if data['d'][tm] == data['d'][0]:
                tugmalar.append(
                [
                    InlineKeyboardButton('>>', callback_data= 'm>>')
                ]
            )
            else:
                tugmalar.append(
                    [
                        InlineKeyboardButton('<<', callback_data= '<<m'), 
                        InlineKeyboardButton('>>', callback_data= 'm>>')
                    ]
                )

            for a in data['d'][tm:tm+5]:
                tm = tm+1
                matn += '<b>{}. {} \n\t\t\t\t \n\n</b>'.format(tm, a['mavzu'])
            query.edit_message_text(text = matn, reply_markup=InlineKeyboardMarkup(tugmalar), parse_mode="HTML")
###################################################################################################################################
        else:
            print(tanlov, "<-tanlov shu")
            if tanlov == 'maruza':
                files = {'audio': open('.{}'.format(data['d'][int(query.data) - 1]['maruza_audio']), 'rb')}
                resp = requests.post('https://api.telegram.org/bot1403694100:AAGGxtJ_eL5wP4hgi4dogc0kj_kdo9gzScQ/sendAudio?chat_id={}'.format(update.effective_user.id), files=files) 
                print(resp.status_code)
            elif tanlov == 'mavzu':
                m = requests.get('{}api/mavzular'.format(url))
                d = requests.get('{}api/darslarapi'.format(url))
                data = json.loads(m.text)
                data1 = json.loads(d.text)
                m_id = data['d'][int(query.data) - 1]['id']
                i = 0
                for dars in data1['d']:
                    print(dars['qaysi_mavzu_id'])
                    if int(dars['qaysi_mavzu_id']) == m_id:
                        files = {'audio': open('.{}'.format(dars['audio']), 'rb')}
                        resp = requests.post('https://api.telegram.org/bot1403694100:AAGGxtJ_eL5wP4hgi4dogc0kj_kdo9gzScQ/sendAudio?chat_id={}'.format(update.effective_user.id), files=files) 
                        
                    i += 1
                print(resp.status_code, 'rr')


            

    except Exception as e:
        print("error ", str(e))

############################## / inline callback ######################



conv_hendler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states = {
        1:[
            MessageHandler(Filters.regex('^(Namoz vaqti)$'), Namozvaqti),
            MessageHandler(Filters.regex('^(Maruzalar)$'), Maruzalar),
            MessageHandler(Filters.regex('^(Darslar)$'), Mavzular),
        ]
    },
    fallbacks=[MessageHandler(Filters.text, start)]
)

updater.dispatcher.add_handler(conv_hendler),
updater.dispatcher.add_handler(CallbackQueryHandler(inline_callback)),


updater.start_polling()
updater.idle()