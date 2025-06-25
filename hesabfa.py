import httpx
import os
from telegram.ext import Updater,CallbackQueryHandler,CommandHandler, CallbackContext
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from telegram import  ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
import telegramcalendar, telegramjcalendar
import utils
import messages
from telegram import Update, InputFile
import logging
import re
import asyncio
import json
import requests
import datetime
from persiantools.jdatetime import JalaliDate
from telegram.ext import ApplicationBuilder
import json
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update\
    ,InlineQueryResultArticle, InputTextMessageContent,InputMediaPhoto
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler,
                          PicklePersistence, filters, CallbackQueryHandler, InlineQueryHandler)
import telegram.ext
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
    PicklePersistence,
)
import time
import asyncio
import pickle
import uuid
from telegram.constants import ParseMode
from calender import telegramcalendar, telegramjcalendar
from calender import utils
from calender import messages
from utilityfunctions import delete_key_safely,operationstr,operationfill\
    ,CleanedDigitsFilter,Operationhazine,Operationdaryaft,Operationenteghal\
    ,Operationhahavale,parse_status_and_note,FactorFilter,convert_to_gregorian\
    ,get_bank_info,get_kala_list,get_kalakhadamat_list,get_contacts,get_bank_list\
    ,get_api_datadp,get_api_datafactor,invoicesaristr,format_invoice,create_invoice_image\
    ,process_invoice_data,datetaiid
from PIL import Image
from io import BytesIO
script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)
log_file_path = os.path.join(script_dir, 'hesabfabot.txt')

logging.basicConfig(
    filename=log_file_path,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.WARNING  
)

logger = logging.getLogger(__name__)
chat_idreport=-123456789
chat_idmanagement=-123456789
global apiKey, application, codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist
global loginToken,hazf
global invoices,kala,khedmat,contact,linkhesab,ramz
script_path = os.path.dirname(os.path.realpath(__file__))
script_patho=os.path.join(script_path, 'o')
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
hazf={}
last_click_times = {}
invoices = {}
kala = {}
khedmat = {}
contact = {}
linkhesab = {}
autorizedusers={}
dichashtag={}
apiKey='Hh3'
loginToken='ba3ae4eba0a'

try:
    script_path = os.path.dirname(os.path.realpath(__file__))
    file_pathramz = os.path.join(script_path, 'ramz.txt')
    file_pathjson = os.path.join(os.path.dirname(os.path.realpath(__file__)), "autorizedusers.json")
    with open(file_pathramz, 'r') as file:
        ramz = file.read().strip()
    with open(file_pathjson, "r") as file:
        json_data = file.read()
        autorizedusers = json.loads(json_data)
    with open(os.path.join(script_path, "dichashtag.json"), "r") as json_file:
        dichashtag = json.load(json_file)
except FileNotFoundError:
    pass
A, AA, B, C, D, E, F, G, H, I, KA, KB, KC, KD, KHA, KHB, KHC, \
FA, FB, FC, FD, FE, FF, R, RA, RB, SHA, SHB, LHA, LHB, GOA, GOaA, \
ENA, HAZA, O, OA, OB, HAZD1, HAA, HAB, FCM, HAZF1, HAZF2, HAZF22, \
HAZF3, FSA, FSB, FSC, FSD, FSE,GOBA,GOBB,GOBC = range(
    53)


async def save_data(obj, filephoto):
    original_datetime = datetime.datetime.strptime(obj.dateTime, "%Y-%m-%dT%H:%M:%S")
    time_part = obj.time
    time_part = time_part.replace(":", "-")
    date_part = obj.date
    jalali_date = JalaliDate.to_jalali(original_datetime.year, original_datetime.month, original_datetime.day)
    operator_folder = str(obj.operator)
    operator_path = os.path.join(script_patho, operator_folder)
    if not os.path.exists(operator_path):
        os.makedirs(operator_path)
    year_folder = jalali_date.year
    month_folder = jalali_date.month
    day_folder = jalali_date.day
    year_path = os.path.join(operator_path, str(year_folder))
    if not os.path.exists(year_path):
        os.makedirs(year_path)
    month_path = os.path.join(year_path, str(month_folder))
    if not os.path.exists(month_path):
        os.makedirs(month_path)
    day_path = os.path.join(month_path, str(day_folder))
    if not os.path.exists(day_path):
        os.makedirs(day_path)
    obj_path = os.path.join(day_path, str(obj.type1))
    if not os.path.exists(obj_path):
        os.makedirs(obj_path)
    obj_id = f"{str(year_folder)}_{str(month_folder)}_{str(day_folder)}_{str(obj.type1)}_{obj.operator}_{date_part}_{time_part}"

    file_path = os.path.join(obj_path, f'{obj_id}.pkl')
    obj.path = file_path
    file_pathphoto = os.path.join(obj_path, f'{obj_id}_aks.jpg')
    obj.imagepath = file_pathphoto
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
    if filephoto:
        await filephoto.download_to_drive(file_pathphoto)
    return obj_id


def save_data1(obj):
    file_path = obj.path
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
    return None


def save_data2(obj):
    file_path = obj.path
    obj.ok = True
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
    return None


def load_data(obj_id):
    obj_parts = obj_id.split('_')
    year_folder = obj_parts[0]
    month_folder = obj_parts[1]
    day_folder = obj_parts[2]
    obj_type = obj_parts[3]
    operator = obj_parts[4]
    day_path = os.path.join(script_patho, operator, year_folder, month_folder, day_folder, obj_type)
    file_path = os.path.join(day_path, f'{obj_id}.pkl')
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def delete_data(obj_id):
    obj_parts = obj_id.split('_')
    year_folder = obj_parts[0]
    month_folder = obj_parts[1]
    day_folder = obj_parts[2]
    obj_type = obj_parts[3]
    operator = obj_parts[4]
    day_path = os.path.join(script_patho, operator, year_folder, month_folder, day_folder, obj_type)
    file_path = os.path.join(day_path, f'{obj_id}.pkl')
    os.remove(file_path)


def show(obj):
    return obj.ok



namekalalist, code_name_mappingkala = get_kala_list(apiKey, loginToken)


codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist = get_kalakhadamat_list(apiKey,
                                                                                                                 loginToken)

codescontacts, code_name_mapping = get_contacts(apiKey, loginToken)

bankcodes, code_name_mappingbanks = get_bank_list(apiKey, loginToken)








def get_user_id_by_code(code, authorized_users):
    code = int(code)
    for user_id, user_data in authorized_users.items():
        if user_data["code"] == code:
            return user_id
    return None


def convert_persian_to_english_numbers(persian_string):
    persian_to_english_digits = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }

    english_string = ''.join(persian_to_english_digits.get(char, char) for char in persian_string)
    return english_string


def is_user_active(user_id):
    user_id_str = str(user_id)
    if user_id_str in autorizedusers and autorizedusers[user_id_str]['active'] == 1:
        return True
    return False


async def handle_debtors_creditors_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(context.user_data['report'])
    if update.callback_query:

        headers = {'Content-Type': 'application/json'}
        response = requests.post("https://api.hesabfa.com/v1/report/debtorscreditors",
                                     json=context.user_data['report'], headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("Success"):
                r = result.get("Result")
                r.sort(key=lambda item: abs(item['Debit'] - item['Credit']), reverse=True)
                for rr in r:
                    
                    image = Image.new('RGB', (250, 120), color='white')
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype("FontsFree-Net-Vazir-Regular.ttf", 16)
                    code = f"کد: {rr['Code']}"
                    name = f"نام: {rr['Name']}"
                    taraz_value = abs(rr['Credit'] - rr['Debit'])
                    
                    if taraz_value == 0:
                        continue
                    taraz = f"تراز: {format(int(taraz_value), ',d')}"

                    
                    code = arabic_reshaper.reshape(code)
                    

                    name = arabic_reshaper.reshape(name)
                  

                    taraz = arabic_reshaper.reshape(taraz)
                    

                    draw.text((10, 10), code, font=font, fill='blue')
                    draw.text((10, 40), name, font=font, fill='blue')

                    
                    if rr['Credit'] > rr['Debit']:
                        draw.text((10, 70), taraz, font=font, fill='green')
                    else:
                        draw.text((10, 70), taraz, font=font, fill='red')
                    
                    buffer = BytesIO()
                    image.save(buffer, format='PNG')
                    buffer.seek(0)

                    
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer,
                                                 caption=f"#U{rr['Code']}")
                    asyncio.sleep(4)
                await update.callback_query.message.reply_text("گزارش بستانکار بدهکار با موفقیت ارسال شد.", reply_markup=markup)
            else:
                await update.callback_query.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
        else:
            text = ("Request failed with status code:", response.status_code) + (
                    "\nResponse content:", response.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)
            await update.callback_query.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
        return A

    elif update.message.text:
        headers = {'Content-Type': 'application/json'}
        response = requests.post("https://api.hesabfa.com/v1/report/debtorscreditors", json=context.user_data['report'],
                                 headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("Success"):
                r = result.get("Result")
                r.sort(key=lambda item: abs(item['Debit'] - item['Credit']), reverse=True)
                for rr in r:
                   
                    image = Image.new('RGB', (250, 120), color='white')
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype("FontsFree-Net-Vazir-Regular.ttf", 16) 

                    code = f"کد: {rr['Code']}"
                    name = f"نام: {rr['Name']}"

                    taraz_value = abs(rr['Credit'] - rr['Debit'])
                    print(taraz_value)
                    print(type(taraz_value))
                    if taraz_value == 0:
                        continue
                    taraz = f"تراز: {format(int(taraz_value), ',d')}"
                    code = arabic_reshaper.reshape(code)
                    name = arabic_reshaper.reshape(name)
                    taraz = arabic_reshaper.reshape(taraz)
                    
                    draw.text((10, 10), code, font=font, fill='blue')
                    draw.text((10, 40), name, font=font, fill='blue')

                    
                    if rr['Credit'] > rr['Debit']:
                        draw.text((10, 70), taraz, font=font, fill='green')
                    else:
                        draw.text((10, 70), taraz, font=font, fill='red')
                    
                    buffer = BytesIO()
                    image.save(buffer, format='PNG')
                    buffer.seek(0)

                    
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer,
                                                 caption=f"#U{rr['Code']}")
                    asyncio.sleep(4)
                await update.message.reply_text("گزارش بستانکار بدهکار با موفقیت ارسال شد.",
                                                               reply_markup=markup)
            else:
                await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
        else:
            text = ("Request failed with status code:", response.status_code) + (
                "\nResponse content:", response.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
        return A


reply_keyboard = [['عملیات دریافت💰', 'عملیات پرداخت💳', 'عملیات هزینه💸', 'عملیات انتقال💳'],
                  ['ثبت فاکتور🧾', 'ثبت کالا📦', 'ثبت خدمات📋', 'عملیات حواله💳'],
                  ['گزارشات📊', 'ذخیره شخص💾👤', '🗑️حذف اسناد', 'دریافت لینک کارت حساب📧'],
                  ['آپدیت خدمات،کالاها،اشخاص،بانک ها🔄', 'اپراتورها🙋‍♂️🙋‍♀️', 'عملیات رمز🔒', 'فاکتور سریع🧾']]
reply_keyboardun = [['عملیات دریافت💰', 'عملیات پرداخت💳'], ['عملیات هزینه💸', 'عملیات انتقال💳'], ['عملیات حواله💳']]
reply_keyboardsabt = [['تایید'], ['لغو']]
markupsabt = ReplyKeyboardMarkup(reply_keyboardsabt, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markupun = ReplyKeyboardMarkup(reply_keyboardun, one_time_keyboard=True)

rbargasht = [['برگشت']]
rbarghashtmarkup = ReplyKeyboardMarkup(rbargasht, one_time_keyboard=True)
###hazf
reply_keyboardhazf = [['رسید دریافت سریع', 'رسید دریافت', 'رسید پرداخت', 'رسید پرداخت سریع'],
                      ['فاکتور فروش سریع', 'فاکتور فروش', 'فاکتور خرید', 'فاکتور خرید سریع'], ['برگشت']]
markuphazf = ReplyKeyboardMarkup(reply_keyboardhazf, one_time_keyboard=True)
receipt_optionssari = ['رسید دریافت سریع', 'رسید پرداخت سریع', 'فاکتور فروش سریع', 'فاکتور خرید سریع']
receipt_options = ['رسید دریافت', 'رسید پرداخت', 'فاکتور فروش', 'فاکتور خرید']

#####regex patterns and custom filters
##

##
rresid = ['100 رسید دریافت اول', '100 رسید پرداخت اول', '100 رسید دریافت دوم', '100 رسید پرداخت دوم',
          '100 رسید دریافت سوم', '100 رسید پرداخت سوم', '100 رسید دریافت چهارم', '100 رسید پرداخت چهارم',
          '100 رسید دریافت پنجم', '100 رسید پرداخت پنجم']
regex_patternresid = f"({'|'.join(map(re.escape, rresid))})"
######linkhesab
regex_pattern5 = r'\b\d+\b'
###operator
regexpatternoperator = r'^\d+-\d+-(0|1)$'
####mablagh
regex_patternmablagh = r"\b\d+\b"
filtermablagh = CleanedDigitsFilter(regex_patternmablagh)
######
regex_patternsaatpeigiri = r"\d{4,}\d{4,}"
filtersaatpeigiri = CleanedDigitsFilter(regex_patternsaatpeigiri)
#####
filter_factor = FactorFilter('^(\d+)(\d+).*$')
###dynamic
###dastebandi kalaha
regex_patternkalalist = '|'.join(re.escape(name) for name in namekalalist)
#####kala va khadamat
regex_patternkalakhadamatlist = '|'.join(re.escape(name) for name in list(code_name_mappingkalakhadamatlist.keys()))

######banks
regex_patternbanks = '^(' + '|'.join(re.escape(code) for code in bankcodes) + ')$'
filterbank = CleanedDigitsFilter(regex_patternbanks)

############contacts
regex_patterncontacts = '^(' + '|'.join(re.escape(code) for code in codescontacts) + ')$'
filtercontacts = CleanedDigitsFilter(regex_patterncontacts)

print('okaval')
async def hazf1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    user_id = update.message.from_user.id
    if user_id == 123456 or user_id == 123456:
        if user_id not in hazf:
            hazf[user_id] = {"apiKey": apiKey, "loginToken": loginToken}
        else:
            del hazf[user_id]
            hazf[user_id] = {"apiKey": apiKey, "loginToken": loginToken}
        reply_text = "❇شما حذف رسید یا فاکتور را انتخاب کرده اید." + "نوع رسید یا فاکتور برای حذف را انتخاب کنید."
        await update.message.reply_text(reply_text, reply_markup=markuphazf)
        return HAZF1
    else:
        if is_user_active(user_id):
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
            return A
        else:
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
            return A
async def hazf2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    text = update.message.text
    user_id = update.message.from_user.id
    hazf[user_id]['op'] = text
    r = "❇" + f"شما {text}" + " انتخاب کرده اید.شماره رسید را وارد کنید."
    await update.message.reply_text(r, reply_markup=rbarghashtmarkup)
    return HAZF2
async def hazf21(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    text = update.message.text
    user_id = update.message.from_user.id
    hazf[user_id]['op'] = text
    headers = {'Content-Type': 'application/json'}
    r = "❇" + f"شما {text}" + " انتخاب کرده اید.شماره رسید را وارد کنید."
    await update.message.reply_text(r, reply_markup=rbarghashtmarkup)
    return HAZF22
async def hazf31(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    headers = {'Content-Type': 'application/json'}
    text = ''.join(filter(str.isdigit, update.message.text))
    user_id = update.message.from_user.id
    hazf[user_id]['number'] = int(text)
    if hazf[user_id]['op'] == 'رسید دریافت':
        hazf[user_id]['type'] = 1
        hazf[user_id]['des'] = get_api_datadp(apiKey, loginToken, hazf[user_id]['number'], hazf[user_id]['type'])
    elif hazf[user_id]['op'] == 'رسید پرداخت':
        hazf[user_id]['type'] = 2
        hazf[user_id]['des'] = get_api_datadp(apiKey, loginToken, hazf[user_id]['number'], hazf[user_id]['type'])
    elif hazf[user_id]['op'] == 'فاکتور خرید':
        hazf[user_id]['type'] = 1
        hazf[user_id]['des'] = get_api_datafactor(apiKey, loginToken, hazf[user_id]['number'], hazf[user_id]['type'])
    elif hazf[user_id]['op'] == 'فاکتور فروش':
        hazf[user_id]['type'] = 0
        hazf[user_id]['des'] = get_api_datafactor(apiKey, loginToken, hazf[user_id]['number'], hazf[user_id]['type'])
    reply_keyboardtaiid = [['تایید'], ['لغو'], ['برگشت']]
    markuptaiid = ReplyKeyboardMarkup(reply_keyboardtaiid, one_time_keyboard=True)
    if hazf[user_id]['des']:
        text = "❎آیا از حذف این سند اطمینان دارید؟؟" + "\n\n" + hazf[user_id]['des']
        await update.message.reply_text(text, reply_markup=markuptaiid)
        return HAZF3
    else:
        text = "سند مذکور یافت نشد.به مرحله اول هدایت می شوید."
        await update.message.reply_text(text, reply_markup=markup)
        return A
async def hazf4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    headers = {'Content-Type': 'application/json'}
    text = update.message.text
    user_id = update.message.from_user.id
    if hazf[user_id]['op'] == 'رسید دریافت':
        hazf[user_id]['type'] = 1
        response = requests.post("https://api.hesabfa.com/v1/receipt/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'رسید پرداخت':
        hazf[user_id]['type'] = 2
        response = requests.post("https://api.hesabfa.com/v1/receipt/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'فاکتور خرید':
        hazf[user_id]['type'] = 1
        response = requests.post("https://api.hesabfa.com/v1/invoice/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'فاکتور فروش':
        hazf[user_id]['type'] = 0
        response = requests.post("https://api.hesabfa.com/v1/invoice/delete", json=hazf[user_id], headers=headers)

    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            reply_text = "حذف با موفقیت انجام شد." + "\n" + "✅✅✅✅✅✅✅✅✅✅✅✅✅" + "\n\n" + "سند:" + f"\n\n{hazf[user_id]['des']}"
            await update.message.reply_text(reply_text, reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)

    return A
async def hazf3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global hazf
    text = ''.join(filter(str.isdigit, update.message.text))
    headers = {'Content-Type': 'application/json'}
    user_id = update.message.from_user.id
    hazf[user_id]['number'] = int(text)
    if hazf[user_id]['op'] == 'رسید دریافت سریع':
        hazf[user_id]['type'] = 1
        response = requests.post("https://api.hesabfa.com/v1/receipt/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'رسید پرداخت سریع':
        hazf[user_id]['type'] = 2
        response = requests.post("https://api.hesabfa.com/v1/receipt/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'فاکتور خرید سریع':
        hazf[user_id]['type'] = 1
        response = requests.post("https://api.hesabfa.com/v1/invoice/delete", json=hazf[user_id], headers=headers)
    elif hazf[user_id]['op'] == 'فاکتور فروش سریع':
        hazf[user_id]['type'] = 0
        response = requests.post("https://api.hesabfa.com/v1/invoice/delete", json=hazf[user_id], headers=headers)

    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            reply_text = "حذف با موفقیت انجام شد."
            await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=rbarghashtmarkup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=rbarghashtmarkup)

    return HAZF2
async def operation1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    delete_key_safely('operation', context.user_data)
    user_id = update.message.from_user.id
    context.user_data['operation'] = {}
    context.user_data['operation']['operationtype'] = update.message.text
    if str(user_id) not in autorizedusers:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید.", reply_markup=markupun)
        return A
    context.user_data['operation']['apiKey'] = apiKey
    context.user_data['operation']['loginToken'] = loginToken
    reply_text, context.user_data['operation'] = operationfill(state=1, operation=context.user_data['operation'])
    await update.message.reply_text(
        text=reply_text,
        reply_markup=telegramjcalendar.create_calendar())
    return B
async def op2inline_jcalendar_handler(update: Update, context: CallbackContext):
    selected, date = await telegramjcalendar.process_calendar_selection(context.bot, update)
    if selected:
        context.user_data['operation']['dateTimejalali'] = date
        reply_text, context.user_data['operation'] = operationfill(state=2, operation=context.user_data['operation'])
        reply_text += "حال مبلغ را وارد نمایید." + "\n\n"
        await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                       text=reply_text,
                                       reply_markup=rbarghashtmarkup)
        return C
async def op3mablagh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_number = ''.join(filter(str.isdigit, update.message.text))
    context.user_data['operation']['amount'] = cleaned_number
    reply_text, context.user_data['operation'] = operationfill(state=3, operation=context.user_data['operation'])
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    if context.user_data['operation']['operationtype'] == 'عملیات حواله💳':
        return HAA
    return D
async def op3mablaghinline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.inline_query.query
    if not query:  
        return
    name_code_mappingbanks = {str(value): str(key) for key, value in code_name_mappingbanks.items()}
    names = list(name_code_mappingbanks.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    filtered_results.reverse()
    results = [InlineQueryResultArticle(id=str(index),
                                        title=name,
                                        input_message_content=InputTextMessageContent(name_code_mappingbanks.get(name)),
                                        ) for index, name in enumerate(filtered_results[:50])  # Limiting to 50 results
               ]
    
    await update.inline_query.answer(results)
    return D
async def havale1inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.inline_query.query
    if not query: 
        return
    name_code_mapping = {str(value): str(key) for key, value in code_name_mapping.items()}
    names = list(name_code_mapping.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    filtered_results.reverse()
    results = [InlineQueryResultArticle(id=str(index),
                                        title=name,
                                        input_message_content=InputTextMessageContent(name_code_mapping.get(name)),
                                        ) for index, name in enumerate(filtered_results[:50])  # Limiting to 50 results
               ]
   
    await update.inline_query.answer(results)
    return HAA
async def havale1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_code = ''.join(filter(str.isdigit, update.message.text))
    name_for_code = code_name_mapping.get(cleaned_code)
    reply_text, context.user_data['operation'] = operationfill(state=4, operation=context.user_data['operation'],
                                                               first=cleaned_code, second=name_for_code)
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return HAB
async def havale2inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.inline_query.query
    if not query: 
        return
    name_code_mapping = {str(value): str(key) for key, value in code_name_mapping.items()}
    names = list(name_code_mapping.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    filtered_results.reverse()
    results = [InlineQueryResultArticle(id=str(index),
                                        title=name,
                                        input_message_content=InputTextMessageContent(name_code_mapping.get(name)),
                                        ) for index, name in enumerate(filtered_results[:50])  # Limiting to 50 results
               ]
    
    await update.inline_query.answer(results)
    return HAB
async def havale2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_code = ''.join(filter(str.isdigit, update.message.text))
    name_for_code = code_name_mapping.get(cleaned_code)
    reply_text, context.user_data['operation'] = operationfill(state=5, operation=context.user_data['operation'],
                                                               first=cleaned_code, second=name_for_code)
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return F
async def daryaftpardakht11inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.inline_query.query
    if not query:  
        return
    name_code_mapping = {str(value): str(key) for key, value in code_name_mapping.items()}
    names = list(name_code_mapping.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    filtered_results.reverse()
    results = [InlineQueryResultArticle(id=str(index),
                                        title=name,
                                        input_message_content=InputTextMessageContent(name_code_mapping.get(name)),
                                        ) for index, name in enumerate(filtered_results[:50])  # Limiting to 50 results
               ]
    
    await update.inline_query.answer(results)
    return E
async def op4bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_code = ''.join(filter(str.isdigit, update.message.text))
    name_for_code = code_name_mappingbanks.get(cleaned_code)
    reply_text, context.user_data['operation'] = operationfill(state=4, operation=context.user_data['operation'],
                                                               first=cleaned_code, second=name_for_code)
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(text=reply_text,
                                    reply_markup=rbarghashtmarkup)
    if context.user_data['operation']['operationtype'] == 'عملیات هزینه💸':
        return HAZA
    elif context.user_data['operation']['operationtype'] == 'عملیات دریافت💰':
        return E
    elif context.user_data['operation']['operationtype'] == 'عملیات پرداخت💳':
        return E
    elif context.user_data['operation']['operationtype'] == 'عملیات انتقال💳':
        return ENA
async def hazine1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['operation']['descriptionamaliat'] = text
    if text == '0':
        context.user_data['operation']['descriptionamaliat'] = '...'
    reply_text, context.user_data['operation'] = operationfill(state=5, operation=context.user_data['operation'])
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return F
async def daryaftpardakht1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_code = ''.join(filter(str.isdigit, update.message.text))
    name_for_code = code_name_mapping.get(cleaned_code)
    reply_text, context.user_data['operation'] = operationfill(state=5, operation=context.user_data['operation'],
                                                               first=cleaned_code, second=name_for_code)
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return F
async def enteghal1inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.inline_query.query
    if not query: 
        return
    name_code_mappingbanks = {str(value): str(key) for key, value in code_name_mappingbanks.items()}
    names = list(name_code_mappingbanks.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    filtered_results.reverse()
    results = [InlineQueryResultArticle(id=str(index),
                                        title=name,
                                        input_message_content=InputTextMessageContent(name_code_mappingbanks.get(name)),
                                        ) for index, name in enumerate(filtered_results[:50])  # Limiting to 50 results
               ]
   
    await update.inline_query.answer(results)
    return ENA
async def enteghal1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cleaned_code = ''.join(filter(str.isdigit, update.message.text))
    name_for_code = code_name_mappingbanks.get(cleaned_code)
    reply_text, context.user_data['operation'] = operationfill(state=5, operation=context.user_data['operation'],
                                                               first=cleaned_code, second=name_for_code)
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(text=reply_text,
                                    reply_markup=rbarghashtmarkup)
    return F
async def op5aks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif text == "عکس رسید فوق را ندارم" or text == "0000":
        file_id = '0'
    context.user_data['operation']['file_id'] = file_id
    reply_text, context.user_data['operation'] = operationfill(state=6, operation=context.user_data['operation'])
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    await update.message.reply_text(text=reply_text,
                                    reply_markup=rbarghashtmarkup)
    return G
async def op6peigiri(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    cleaned_number = ''.join(filter(str.isdigit, update.message.text))
    context.user_data['operation']['saat'] = cleaned_number[0:4]
    context.user_data['operation']['peigiri'] = cleaned_number[4:]
    if context.user_data['operation']['operationtype'] == 'عملیات هزینه💸':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"پرداخت وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" به هزینه ها بابت {context.user_data['operation']['descriptionamaliat']} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" ش: {context.user_data['operation']['peigiri']} "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات دریافت💰':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"دریافت وجه به بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" از {context.user_data['operation']['contactCode']} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات پرداخت💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"پرداخت وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" به {context.user_data['operation']['contactCode']} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" ش: {context.user_data['operation']['peigiri']} "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات انتقال💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"انتقال وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode0'])}" + f" به بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode1'])} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات حواله💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"حواله وجه از {context.user_data['operation']['contactCode0']}" + f" به  {context.user_data['operation']['contactCode1']} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])

    reply_text, context.user_data['operation'] = operationfill(state=7, operation=context.user_data['operation'])
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    if context.user_data['operation']['file_id'] == '0':
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_markup=markupsabt)
        return H
    elif context.user_data['operation']['file_id']:
        await context.bot.send_photo(update.message.chat_id, photo=context.user_data['operation']['file_id'],
                                     caption=reply_text,
                                     reply_markup=markupsabt)
        return H
async def op7tozihat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.message.from_user.id
    if context.user_data['operation']['operationtype'] == 'عملیات هزینه💸':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"پرداخت وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" به هزینه ها بابت {context.user_data['operation']['descriptionamaliat']} " + f" {text} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" ش: {context.user_data['operation']['peigiri']} "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات دریافت💰':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"دریافت وجه به بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" از {context.user_data['operation']['contactCode']} " + f" {text} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات پرداخت💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"پرداخت وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode'])}" + f" به {context.user_data['operation']['contactCode']} " + f" {text} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" ش: {context.user_data['operation']['peigiri']} "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات انتقال💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"انتقال وجه از بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode0'])}" + f" به بانک {code_name_mappingbanks.get(context.user_data['operation']['bankCode1'])} " + f" {text} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    elif context.user_data['operation']['operationtype'] == 'عملیات حواله💳':
        context.user_data['operation'][
            'description'] = "BOT" + " اپراتور" + f" ({autorizedusers.get(str(user_id))['code']}) " + f"حواله وجه از  {context.user_data['operation']['contactCode0']}" + f" به  {context.user_data['operation']['contactCode1']} " + f" {text} " + f"طی ساعت {context.user_data['operation']['saat']} " + f" (پ {context.user_data['operation']['peigiri']}) "
        context.user_data['operation']['description'] = convert_persian_to_english_numbers(
            context.user_data['operation']['description'])
        context.user_data['operation']['amount'] = convert_persian_to_english_numbers(
            context.user_data['operation']['amount'])
    reply_text, context.user_data['operation'] = operationfill(state=8, operation=context.user_data['operation'])
    reply = '\n'.join(reply_text.rsplit('\n', 2)[:-1])
    context.user_data['operation']['reply_text'] = reply
    if context.user_data['operation']['file_id'] == '0':
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_markup=markupsabt)
        return I
    elif context.user_data['operation']['file_id']:
        await context.bot.send_photo(update.message.chat_id, photo=context.user_data['operation']['file_id'],
                                     caption=reply_text,
                                     reply_markup=markupsabt)
        return I
async def op8sabt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    operator = autorizedusers.get(str(user_id))['code']
    if context.user_data['operation']['operationtype'] == 'عملیات هزینه💸':
        filtered = {key: context.user_data['operation'][key] for key in context.user_data['operation'] if
                    key != 'reply_text'}
        operation = Operationhazine(**filtered, user_id=user_id, operator=operator, chat_id=chat_id)
        if context.user_data['operation']["file_id"] == '0':
            operation_id = await save_data(operation, None)
        else:
            file = await context.bot.getFile(context.user_data['operation']["file_id"])
            operation_id = await save_data(operation, file)

        a = InlineKeyboardMarkup.from_column([
            InlineKeyboardButton('تایید', callback_data=operation_id),
            InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
            InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")
        ])

        aa, o = hazinestr(operation, None)
    elif context.user_data['operation']['operationtype'] == 'عملیات دریافت💰':
        filtered = {key: context.user_data['operation'][key] for key in context.user_data['operation'] if
                    key != 'reply_text'}
        tarafhesab = get_user_id_by_code(context.user_data['operation']['contactCode'], autorizedusers)
        operation = Operationdaryaft(**filtered, user_id=user_id, operator=operator, chat_id=chat_id, type1='d',
                                     tarafhesab=tarafhesab)
        if context.user_data['operation']["file_id"] == '0':
            operation_id = await save_data(operation, None)
        else:
            file = await context.bot.getFile(context.user_data['operation']["file_id"])
            operation_id = await save_data(operation, file)
        a = InlineKeyboardMarkup.from_column([
            InlineKeyboardButton('تایید', callback_data=operation_id),
            InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
            InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")
        ])
        aa, o = daryaftstr(operation, None)
    elif context.user_data['operation']['operationtype'] == 'عملیات پرداخت💳':
        filtered = {key: context.user_data['operation'][key] for key in context.user_data['operation'] if
                    key != 'reply_text'}
        tarafhesab = get_user_id_by_code(context.user_data['operation']['contactCode'], autorizedusers)
        operation = Operationdaryaft(**filtered, user_id=user_id, operator=operator, chat_id=chat_id, type1='p',
                                     tarafhesab=tarafhesab)

        if context.user_data['operation']["file_id"] == '0':
            operation_id = await save_data(operation, None)
        else:
            file = await context.bot.getFile(context.user_data['operation']["file_id"])
            operation_id = await save_data(operation, file)
        a = InlineKeyboardMarkup.from_column([
            InlineKeyboardButton('تایید', callback_data=operation_id),
            InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
            InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")
        ])
        aa, o = daryaftstr(operation, None)
    elif context.user_data['operation']['operationtype'] == 'عملیات انتقال💳':
        filtered = {key: context.user_data['operation'][key] for key in context.user_data['operation'] if
                    key != 'reply_text'}
        operation = Operationenteghal(**filtered, user_id=user_id, operator=operator, chat_id=chat_id)
        if context.user_data['operation']["file_id"] == '0':
            operation_id = await save_data(operation, None)
        else:
            file = await context.bot.getFile(context.user_data['operation']["file_id"])
            operation_id = await save_data(operation, file)

        a = InlineKeyboardMarkup.from_column([
            InlineKeyboardButton('تایید', callback_data=operation_id),
            InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
            InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")
        ])
        aa, o = enteghalstr(operation, None, None)
    elif context.user_data['operation']['operationtype'] == 'عملیات حواله💳':
        filtered = {key: context.user_data['operation'][key] for key in context.user_data['operation'] if
                    key != 'reply_text'}
        tarafhesab = get_user_id_by_code(context.user_data['operation']['contactCode0'], autorizedusers)
        operation = Operationhahavale(**filtered, user_id=user_id, operator=operator, chat_id=chat_id,
                                      tarafhesab=tarafhesab)
        if context.user_data['operation']["file_id"] == '0':
            operation_id = await save_data(operation, None)
        else:
            file = await context.bot.getFile(context.user_data['operation']["file_id"])
            operation_id = await save_data(operation, file)

        a = InlineKeyboardMarkup.from_column([
            InlineKeyboardButton('تایید', callback_data=operation_id),
            InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
            InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")
        ])
        aa, o = havalestr(operation, None, None)

    formatted_jalali_date = f"{operation.date.year}-{operation.date.month:02d}-{operation.date.day:02d}"
    if operation.dateTimejalali == formatted_jalali_date:
        pass
    else:
        if context.user_data['operation']['operationtype'] in ['عملیات دریافت💰', 'عملیات پرداخت💳', 'عملیات حواله💳']:
            a = InlineKeyboardMarkup.from_column([
                InlineKeyboardButton('تایید', callback_data=operation_id),
                InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
                InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}"),
                InlineKeyboardButton('اعمال جریمه🛃', callback_data=f'jarimeye{operation_id}'),
                InlineKeyboardButton('اعمال جریمه👤', callback_data=f'jarimeyeshakhs{operation_id}'),
            ])
        else:
            a = InlineKeyboardMarkup.from_column([
                InlineKeyboardButton('تایید', callback_data=operation_id),
                InlineKeyboardButton('لغو', callback_data='cancel' + f"{operation_id}"),
                InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}"),
                InlineKeyboardButton('اعمال جریمه🛃', callback_data=f'jarimeye{operation_id}'), ])

    if context.user_data['operation']['file_id'] == '0':
        photo_path = "resid.jpg"
        aa = aa + "\n\n" + "#WAITING"
        with open(photo_path, "rb") as photo_file:
            await context.bot.send_photo(chat_id=chat_idmanagement, photo=photo_file, caption=aa, reply_markup=a)
    elif context.user_data['operation']['file_id']:
        aa = aa + "\n\n" + "#WAITING"
        await context.bot.send_photo(chat_id=chat_idmanagement, photo=context.user_data['operation']['file_id'],
                                     caption=aa,
                                     reply_markup=a)
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("درخواست موفقیت آمیز بود. برای بررسی به مدیر ارجاع می شود.",
                                        reply_markup=markupun)
        delete_key_safely('operation', context.user_data)
        return A
    await update.message.reply_text("درخواست موفقیت آمیز بود. برای بررسی به مدیر ارجاع می شود.", reply_markup=markup)
    delete_key_safely('operation', context.user_data)
    return A
async def operator1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    if user_id == 1234565 or user_id == 123456:
        reply_text = "✳️ سلام.  " \
                     "\n" \
                     "برای تغییرات در اپراتورها انتخاب کنید." \
                     "\n" \
                     "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید"
        reply_keyboardr = [["ایجاد اپراتور⚡️👤"], ['مشاهده اپراتورهای فعلی👨‍👩‍👧‍👦', 'حذف اپراتور🚫👤'], ['برگشت']]
        markupr = ReplyKeyboardMarkup(reply_keyboardr, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markupr)
        return O
    else:
        if is_user_active(user_id):
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
            return A
        else:
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
            return A
async def operator2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    reply_text = "✳️برای ایجاد اپراتور طبق الگوی زیر عمل کنید." + "\n" + "دو نوع اپراتور در سیستم ربات حسابداری موجود است." + "\n"
    reply_text += "1-اپراتور فعال: این اپراتور به همه بخش ها به جز عملیات رمز و اپراتورها دسترسی دارد. برای ایجاد چنین اپراتوری طبق الگوی زیر عمل کنید." + "\n"
    reply_text += "الگو: " + "\n" + "یوزرآیدی-کدشخص-1" + "\n\n" + "2-اپراتور نیمه فعال: این اپراتور فقط به عملیات دریافت و عملیات پرداخت دسترسی دارد. برای ایجاد چنین اپراتوری طبق الگوی زیر عمل کنید. "
    reply_text += "\n" + "الگو: " + "\n" + "یوزرآیدی-کدشخص-0"
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return OA
async def operator3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global autorizedusers
    user = update.message.from_user
    user_id = update.message.from_user.id
    text = update.message.text

    pattern = re.compile(regexpatternoperator)
    match = pattern.match(text)
    if match:
        userid, code, active = match.group().split('-')
    autorizedusers[userid] = {"code": int(code), "active": int(active)}
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "autorizedusers.json")
    json_data = json.dumps(autorizedusers, indent=4)
    with open(file_path, "w") as file:
        file.write(json_data)
    if active == '1':
        a = "وضعیت دسترسی: به تمام بخش ها به جز رمز و اپراتورها"
    elif active == '0':
        a = "وضعیت دسترسی: فقط به بخش عملیات دریافت، پرداخت، انتقال و هزینه"
    reply = "شما شخص با مشخصات زیر به عنوان اپراتور وارد کردید. " + "\n" + f"یوزرآیدی: {userid}" + "\n" + "کد شخص: " + f"{code}" + "\n" + f"{a}" + "\n" + "ایجاد نموده اید."
    await update.message.reply_text(reply, reply_markup=markup)
    return A
async def operator4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global autorizedusers
    r = "افراد با مشخصات زیر دسترسی های زیر را دارند." + "\n\n"
    i = 0
    for userid, user_data in autorizedusers.items():
        i += 1
        code = user_data['code']
        active = user_data['active']
        a = "وضعیت دسترسی: به تمام بخش ها به جز رمز و اپراتورها" if active == 1 else "وضعیت دسترسی: فقط به بخش عملیات دریافت و پرداخت"
        r += "شماره " + f"({i})" + ":" + "\n" + "یوزرآیدی: " + f"{userid}" + "\n" + "کد شخص: " + f"{code}" + "\n" + f"{a}" + "\n\n"
    await update.message.reply_text(r, reply_markup=markup)
    return A
async def operator5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply = "لطفاً یوزرآیدی فردی را که قصد حذف ایشان را دارید، وارد کنید."
    await update.message.reply_text(reply, reply_markup=rbarghashtmarkup)
    return OB
async def operator6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global autorizedusers
    user = update.message.from_user
    user_id = update.message.from_user.id
    text = update.message.text
    try:
        autorizedusers.pop(text)
        reply = "اپراتور با یوزرآیدی  " + f"({text})" + " از لیست اپراتورها حذف گردید."
        await update.message.reply_text(reply, reply_markup=markup)
    except KeyError:
        reply = "اپراتور با یوزرآیدی  " + f"({text})" + " در لیست اپراتورها موجود نیست. لطفا از منو اصلی بر روی مشاهده اپراتورهای فعلی بزنید و شماره یوزر آیدی را چک کنید."
        await update.message.reply_text(reply, reply_markup=markup)
    return A
async def ramz1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    if user_id == 123 or user_id == 12345:
        reply_text = "✳️ سلام.  " \
                     "\n" \
                     "برای عوض کردن رمز ، تغییر رمز را بزنید و برای مشاهده رمز موجود رمز فعلی را بزنید" \
                     "\n" \
                     "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید"
        reply_keyboardr = [['رمز فعلی🔐', 'تغییر رمز🔒🔄'], ['برگشت']]
        markupr = ReplyKeyboardMarkup(reply_keyboardr, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markupr)
        return RA
    else:
        if is_user_active(user_id):
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
            return A
        else:
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
            return A
async def ramz2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    reply_text = "✳️ 🔐رمز فعلی:  " \
                 "\n" \
                 f"{ramz}" \
                 "\n" \
                 "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید"
    await update.message.reply_text(reply_text, reply_markup=markup)
    return A
async def ramz3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    reply_text = "✳️ 🔐رمز فعلی:  " \
                 "\n" \
                 f"{ramz}" \
                 "\n" \
                 "⬅️برای تغییر رمز، رمز را وارد نمایید در غیر این صورت برگشت را بزنید."
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return RB
async def ramz4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global ramz
    global application
    user = update.message.from_user
    user_id = update.message.from_user.id
    text = update.message.text
    reply_text = "✳️ 🔐رمز  جدید:  " \
                 "\n" \
                 f"{text}" \
                 "\n"
    script_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_path, 'ramz.txt')
    with open(file_path, 'w') as file:
        file.write(str(text))
        ramz = text
    application.handlers[0][0].states[R][0] = MessageHandler(filters.Regex(f"{ramz}"), start)
    reply_text += "رمز با موفقیت تغییر پیدا کرد. برای ورود جدید رمز جدید را وارد کنید."
    await update.message.reply_text(reply_text, reply_markup=markup)
    return A
async def startramz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    if os.path.exists(os.path.join(script_dir, "sokhan.txt")):
        with open(os.path.join(script_dir, "sokhan.txt"), "r", encoding="utf-8") as file:
            content = file.read()
    else:
        print("File 'sokhan.txt' not found.")
        content=""
    if user_id == 123456 or user_id == 1234:

        reply_text = "✳️ سلام جناب   خوش آمدید.  " \
                     "\n" \
                     "برای شروع ثبت اسناد حسابداری یکی از گزینه ها را انتخاب بفرمایید." \
                     "\n" \
                     "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید."+f"\n\n{content}"
        await update.message.reply_text(reply_text, reply_markup=markup)
        return A

    reply_text = "✳️ سلام خوش آمدید  " \
                 "\n" \
                 "برای شروع ثبت اسناد حسابداری لطفا رمز را وارد کنید. به انگلیسی اعداد رمز را وارد کنید." \
                 "\n" \
                 "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید"+f"\n\n{content}"
    await update.message.reply_text(reply_text)
    return R
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = update.message.from_user.id
    if user_id == 1234 or user_id == 124:
        reply_text = "✳️ سلام جناب   خوش آمدید.  " \
                     "\n" \
                     "برای شروع ثبت اسناد حسابداری یکی از گزینه ها را انتخاب بفرمایید." \
                     "\n" \
                     "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید."
        await update.message.reply_text(reply_text, reply_markup=markup)
        return A
    else:
        reply_text = "✳️ سلام خوش آمدید  " \
                     "\n" \
                     "برای شروع ثبت اسناد حسابداری یکی از گزینه ها را انتخاب بفرمایید." \
                     "\n" \
                     "⬅️در هر مرحله اگر برگشت را تایپ کنید به مرحله اول بازگردانده میشوید"
        if is_user_active(user_id):
            await update.message.reply_text(reply_text, reply_markup=markup)
            return A
        else:
            await update.message.reply_text(reply_text, reply_markup=markupun)
            return A
async def update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #  conversation handler>>application.handlers[0][0]
    # application.handlers[0][0].states[R][0]
    # D: [InlineQueryHandler(op3mablaghinline),MessageHandler(filterbank, op4bank),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # HAA:[InlineQueryHandler(havale1inline),MessageHandler(filtercontacts, havale1),MessageHandler(filters.Regex(("^برگشت$")), start),],
    # HAB: [InlineQueryHandler(havale2inline),MessageHandler(filtercontacts, havale2),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # E: [InlineQueryHandler(daryaftpardakht11inline),MessageHandler(filtercontacts, daryaftpardakht1),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # ENA: [InlineQueryHandler(enteghal1inline),MessageHandler(filterbank, enteghal1),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # FB: [MessageHandler(filtercontacts, sabtfactor3),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # FD: [InlineQueryHandler(sabtfactor4inline),MessageHandler(filters.Regex(regex_patternkalakhadamatlist), sabtfactor5),CallbackQueryHandler(sabtfactor5, pattern=regex_patternkalakhadamatlist),MessageHandler(filters.Regex(("^برگشت$")), start), ],
    # KB: [InlineQueryHandler(sabtkala3inline),CallbackQueryHandler(sabtkala3, pattern=regex_patternkalalist),MessageHandler(filters.Regex(regex_patternkalalist), sabtkala3),MessageHandler(filters.Regex("^برگشت$"), start), ],
    # LHA: [MessageHandler(filters.Regex(regex_patterncontacts), linkhesab2),MessageHandler(filters.Regex(("^برگشت$")), start), ],

    global application, namekalalist, code_name_mappingkala, regex_patternkalalist
    global codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist, regex_patternkalakhadamatlist
    global bankcodes, code_name_mappingbanks, regex_patternbanks, filterbank
    global codescontacts, code_name_mapping, regex_patterncontacts, filtercontacts
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
        return A
    reply = '🔄آپدیت بانک ها، اشخاص، کالاها و خدمات و دسته بندی کالاها' + "\n\n"
    ###dynamic
    ###dastebandi kalaha
    namekalalist, code_name_mappingkala = get_kala_list(apiKey, loginToken)
    regex_patternkalalist = '|'.join(re.escape(name) for name in namekalalist)
    application.handlers[0][0].states[KB] = [InlineQueryHandler(sabtkala3inline),
                                             CallbackQueryHandler(sabtkala3, pattern=regex_patternkalalist),
                                             MessageHandler(filters.Regex(regex_patternkalalist), sabtkala3),
                                             MessageHandler(filters.Regex("^برگشت$"), start), ],
    if namekalalist:
        reply += "📦دسته بندی کالاها آپدیت شد." + "\n\n"
    else:
        reply += "📦" + "❌" + "آپدیت دسته بندی کالاها به مشکل بر خورد و سرور حسابفا جواب نداد." + "\n\n"
    #####kala va khadamat
    codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist = get_kalakhadamat_list(
        apiKey,
        loginToken)
    regex_patternkalakhadamatlist = '|'.join(re.escape(name) for name in list(code_name_mappingkalakhadamatlist.keys()))
    application.handlers[0][0].states[FD] =[
                InlineQueryHandler(sabtfactor4inline),
                 MessageHandler(filters.Regex(regex_patternkalakhadamatlist)& ~filters.Regex("^برگشت$") , sabtfactor5),
                 CallbackQueryHandler(sabtfactor5, pattern=regex_patternkalakhadamatlist),
                 MessageHandler(filters.Regex(("^برگشت$")), start),
            ],
    if code_name_mappingkalakhadamatlist:
        reply += "📋لیست کالاها و خدمات آپدیت شد." + "\n\n"
    else:
        reply += "📋" + "❌" + "آپدیت لیست کالاها و خدمات به مشکل برخورد و سرور حسابفا جواب نداد." + "\n\n"
    ######banks
    bankcodes, code_name_mappingbanks = get_bank_list(apiKey, loginToken)
    regex_patternbanks = '^(' + '|'.join(re.escape(code) for code in bankcodes) + ')$'
    filterbank = CleanedDigitsFilter(regex_patternbanks)
    application.handlers[0][0].states[D] = [InlineQueryHandler(op3mablaghinline), MessageHandler(filterbank, op4bank),
                                            MessageHandler(filters.Regex(("^برگشت$")), start), ]
    application.handlers[0][0].states[ENA] = [InlineQueryHandler(enteghal1inline),
                                              MessageHandler(filterbank, enteghal1),
                                              MessageHandler(filters.Regex(("^برگشت$")), start), ]
    if bankcodes:
        reply += "🏦" + "لیست بانک ها آپدیت شد." + "\n\n"
    else:
        reply += "🏦" + "❌" + "آپدیت لیست بانک ها به مشکل برخورد و سرور حسابفا جواب نداد." + "\n\n"
    ############contacts
    codescontacts, code_name_mapping = get_contacts(apiKey, loginToken)
    regex_patterncontacts = '^(' + '|'.join(re.escape(code) for code in codescontacts) + ')$'
    filtercontacts = CleanedDigitsFilter(regex_patterncontacts)
    application.handlers[0][0].states[HAA] = [InlineQueryHandler(havale1inline),
                                              MessageHandler(filtercontacts, havale1),
                                              MessageHandler(filters.Regex(("^برگشت$")), start), ]
    application.handlers[0][0].states[HAB] = [InlineQueryHandler(havale2inline),
                                              MessageHandler(filtercontacts, havale2),
                                              MessageHandler(filters.Regex(("^برگشت$")), start), ]
    application.handlers[0][0].states[E] = [InlineQueryHandler(daryaftpardakht11inline),
                                            MessageHandler(filtercontacts, daryaftpardakht1),
                                            MessageHandler(filters.Regex(("^برگشت$")), start), ]
    application.handlers[0][0].states[FB] = [MessageHandler(filtercontacts, sabtfactor3),
                                             MessageHandler(filters.Regex(("^برگشت$")), start), ]
    application.handlers[0][0].states[LHA] = [MessageHandler(filters.Regex(regex_patterncontacts), linkhesab2),
                                              MessageHandler(filters.Regex(("^برگشت$")), start), ]
    if codescontacts:
        reply += "👤" + "لیست اشخاص آپدیت شد." + "\n\n"
    else:
        reply += "👤" + "❌" + "آپدیت لیست اشخاص به مشکل برخورد و سرور حسابفا جواب نداد." + "\n\n"

    await update.message.reply_text(reply, reply_markup=markup)
    return A


async def linkhesab1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global linkhesab
    user_id = update.message.from_user.id
    if user_id == 12345 or user_id == 12345:
        if user_id not in linkhesab:
            linkhesab[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "showAllAccounts": True}
        else:
            linkhesab[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "showAllAccounts": True}
        reply_text = "❇شما دریافت لینک کارت حساب را انتخاب کرده اید. حال کد شخص مد نظر را وارد کنید."
        await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
        return LHA
    else:
        if is_user_active(user_id):
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
            return A
        else:
            await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
            return A
async def linkhesab2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global linkhesab
    text = update.message.text
    user_id = update.message.from_user.id
    linkhesab[user_id]['code'] = text
    name_for_code = code_name_mapping.get(text)
    r = "❇" + f"شما {name_for_code}" + " را انتخاب کرده اید. حال تعداد روز اعتبار برای دریافت لینک کارت حساب را وارد کنید."
    await update.message.reply_text(r, reply_markup=rbarghashtmarkup)
    return LHB
async def linkhesab3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global linkhesab
    text = update.message.text
    user_id = update.message.from_user.id
    name_for_code = code_name_mapping.get(linkhesab[user_id]['code'])
    linkhesab[user_id]['days'] = text
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://api.hesabfa.com/v1/contact/getContactLink", json=linkhesab[user_id],
                             headers=headers)
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            link = r["Link"]
            rr = "❇" + "در زیر لینک حساب " + f"{name_for_code}" + " آورده شده است."
            rr = rr + "\n\n" + "لینک (ها): " + "\n" + f"{link}"
            await update.message.reply_text(rr, reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    del linkhesab[user_id]
    return A
async def shakhs1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global contact
    user = update.message.from_user
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
        return A
    if user_id not in contact:
        contact[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "contact": {"ContactType": 1}}
    else:
        contact[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "contact": {"ContactType": 1}}
    reply_text = "❇شما ذخیره اشخاص را انتخاب کرده اید. حال نام شخص مد نظر را وارد کنید."

    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return SHA
async def shakhs2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global contact
    text = update.message.text
    user_id = update.message.from_user.id
    reply_text = "❇" + " شخص به نام " + f"{text}" + " در سیستم در حال ثبت است. آیا میخواهید ایشان را ثبت کنید؟"
    contact[user_id]["contact"]["Name"] = text
    await update.message.reply_text(reply_text, reply_markup=markupsabt)
    return SHB
async def shakhs3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global contact, application, codescontacts, code_name_mapping
    user_id = update.message.from_user.id
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://api.hesabfa.com/v1/contact/save", json=contact[user_id], headers=headers)
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            await update.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    del contact[user_id]
    return A
async def sabtkala1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala
    user = update.message.from_user
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
        return A
    if user_id not in kala:
        kala[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "item": {}}
    else:
        kala[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "item": {}}
    reply_text = "❇" + "شما ثبت کالا را انتخاب کرده اید. حال نام کالا را وارد کنید."
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return KA
async def sabtkala2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala
    text = update.message.text
    user_id = update.message.from_user.id
    kala[user_id]["item"]["Name"] = text
    reply_text = "❇" + f"شما اسم کالا {text} را وارد کردید. حالا دسته بندی را وارد کنید توجه کنید دسته بندی از قبل باید در سایت تعریف کرده باشید "
    names = namekalalist
    chunk_size = 90
    name_chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]
    i = 0
    for chunk in name_chunks:
        keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in chunk[i:i + 3]] for i in
                    range(0, len(chunk), 3)]
        markupkalalist = InlineKeyboardMarkup(keyboard)
        if i == 0:
            await update.message.reply_text(reply_text, reply_markup=markupkalalist)
        else:
            r = "90 دسته بندی بعدی کالاها:"
            await update.message.reply_text(r, reply_markup=markupkalalist)
        i = i + 1
    return KB
async def sabtkala3inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala
    query = update.inline_query.query
    if not query:  
        return
    if namekalalist is None:
        return
    filtered_results = [name for name in namekalalist if query.upper() in name.upper()]
    results = [InlineQueryResultArticle(id=str(index),
            title=name,
            input_message_content=InputTextMessageContent(name),
        ) for index, name in enumerate(filtered_results[:50])  
    ]
    
    await update.inline_query.answer(results)
    return KB
async def sabtkala3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala
    query = update.callback_query
    if query:
        user_id = query.from_user.id
        text = query.data
        kala[user_id]["item"]["NodeFamily"] = code_name_mappingkala.get(text)
        reply_text = "❇" + f"شما دسته بندی کالا را {text} وارد کرده اید. حال کد کالا را در صورت نیاز وارد کنید در غیر این صورت صفر وارد نمایید.."
        await query.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    else:
        text = update.message.text
        user_id = update.message.from_user.id
        kala[user_id]["item"]["NodeFamily"] = code_name_mappingkala.get(text)
        reply_text = "❇" + f"شما دسته بندی کالا را {text} وارد کرده اید. حال کد کالا را در صورت نیاز وارد کنید در غیر این صورت صفر وارد نمایید.."
        await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return KC
async def sabtkala4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala
    text = update.message.text
    user_id = update.message.from_user.id
    productcode = text
    if productcode == '0':
        productcode = None
    active_status = 1
    kala[user_id]["item"]["ProductCode"] = productcode
    kala[user_id]["item"]["Active"] = active_status
    kala[user_id]["item"]["ItemType"] = 0
    kala[user_id]["item"]["Unit"] = 'عدد'
    kala[user_id]['item']['Description'] = None
    kala[user_id]['item']['SellPrice'] = None
    kala[user_id]['item']['BuyPrice'] = None
    d = (
        "❇بازبینی عملیات انجام شده :\n\n"
        f"نام کالا: {kala[user_id]['item']['Name']}\n"
        f"دسته بندی کالا: {kala[user_id]['item']['NodeFamily']}\n"
        f"توضیحات کالا: {kala[user_id]['item']['Description']}\n"
        f"قیمت فروش: {kala[user_id]['item']['SellPrice']}\n"
        f"قیمت خرید: {kala[user_id]['item']['BuyPrice']}\n"
        f"کد کالا: {kala[user_id]['item']['ProductCode']}\n"
        f"فعال بودن : فعال"
        "\n\n"
        "آیا مورد تایید است⁉️"
    )
    await update.message.reply_text(d, reply_markup=markupsabt)
    return KD
async def sabtkala5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global kala, application, codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist
    user_id = update.message.from_user.id
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://api.hesabfa.com/v1/item/save", json=kala[user_id], headers=headers)
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            await update.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    del kala[user_id]
    return A
async def sabtkhadamat1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global khedmat
    user = update.message.from_user
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .",reply_markup=markup)
        return A
    if user_id not in khedmat:
        khedmat[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "item": {}}
    else:
        khedmat[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "item": {}}
    reply_text = "شما ثبت خدمات را انتخاب کرده اید. حال نام خدمات را وارد نمایید."
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return KHA
async def sabtkhadamat2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global khedmat
    text = update.message.text
    user_id = update.message.from_user.id
    khedmat[user_id]["item"]["Name"] = text
    reply_text = f"شما اسم خدمات {text} را وارد کرده اید. " + "حال کد خدمات را در صورت نیاز وارد کنید در غیر این صورت صفر وارد نمایید."
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return KHB
async def sabtkhadamat3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global khedmat
    text = update.message.text
    user_id = update.message.from_user.id
    productcode = text
    if productcode == '0':
        productcode = None
    active_status = 1
    khedmat[user_id]["item"]["ProductCode"] = productcode
    khedmat[user_id]["item"]["Active"] = active_status
    khedmat[user_id]["item"]["ItemType"] = 1
    khedmat[user_id]["item"]["Unit"] = 'عدد'
    khedmat[user_id]['item']['Description'] = None
    khedmat[user_id]['item']['SellPrice'] = None
    khedmat[user_id]['item']['BuyPrice'] = None

    d = (
        "بازبینی عملیات انجام شده :\n\n"
        f"نام خدمات: {khedmat[user_id]['item']['Name']}\n"
        f"کد خدمات: {khedmat[user_id]['item']['ProductCode']}\n"
        f"توضیحات خدمات: {khedmat[user_id]['item']['Description']}\n"
        f"قیمت فروش: {khedmat[user_id]['item']['SellPrice']}\n"
        f"قیمت خرید: {khedmat[user_id]['item']['BuyPrice']}\n"
        f"فعال بودن : فعال"
        "\n\n"
        "آیا مورد تایید است⁉️"
    )
    await update.message.reply_text(d, reply_markup=markupsabt)
    return KHC
async def sabtkhadamat4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global khedmat, application, regex_patternkalakhadamatlist, codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist
    user_id = update.message.from_user.id
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://api.hesabfa.com/v1/item/save", json=khedmat[user_id], headers=headers)
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        await context.bot.send_message(chat_id=chat_idreport, text=result_str)
        if result.get("Success"):
            r = result.get("Result")
            await update.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    del khedmat[user_id]
    return A
async def sabtfactor1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    user = update.message.from_user
    text=update.message.text
    context.user_data.clear()
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markup)
        return A
    if user_id not in invoices:
        invoices[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "invoice": {}}
    else:
        invoices[user_id] = {"apiKey": apiKey, "loginToken": loginToken, "invoice": {}}
    if text=="فاکتور سریع🧾":
        invoices[user_id]['فاکتور سریع']=True
    else:
        invoices[user_id]['فاکتور سریع'] =False
    reply_text = "❇شما ثبت فاکتور را انتخاب کرده اید. حال نوع فاکتور را وارد کنید"
    reply_keyboardsf2 = [['فروش'], ['خرید'], ['برگشت']]
    markupsf2 = ReplyKeyboardMarkup(reply_keyboardsf2, one_time_keyboard=True)
    await update.message.reply_text(reply_text, reply_markup=markupsf2)
    return FA
async def sabtfactor2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices

    user_id = update.message.from_user.id
    text = update.message.text
    if text == "خرید":
        invoices[user_id]["invoice"]["InvoiceType"] = 1
    if text == "فروش":
        invoices[user_id]["invoice"]["InvoiceType"] = 0

    reply_text = "❇️" + f"شما فاکتور {text} را انتخاب کرده اید. حال کد شخص مدنظر را وارد کنید"
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    return FB
async def sabtfactor3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    user_id = update.message.from_user.id
    text = update.message.text
    name_for_code = code_name_mapping.get(text)
    invoices[user_id]["invoice"]["contactCode"] = text
    invoices[user_id]["invoice"]["ContactTitle"] = name_for_code
    reply_text = f"❇شما {name_for_code} را انتخاب کرده اید." + "\n\n"
    reply_text+="حال تاریخ را وارد نمایید."
    await update.message.reply_text(
        text=reply_text,
        reply_markup=telegramjcalendar.create_calendar())
    return FCM
async def sabtfactor31(update: Update, context: CallbackContext):
    global invoices
    user_id=update.callback_query.from_user.id
    selected, date = await telegramjcalendar.process_calendar_selection(context.bot, update)
    if selected:

        invoices[user_id]["invoice"]["Date"] = convert_to_gregorian( date)
        invoices[user_id]["invoice"]["DueDate"]=convert_to_gregorian( date)
        if  invoices[user_id]['فاکتور سریع']:
            context.user_data['InvoiceType']=invoices[user_id]["invoice"]["InvoiceType"]
            context.user_data['contactCode']=invoices[user_id]["invoice"]["contactCode"]
            context.user_data['ContactTitle']=invoices[user_id]["invoice"]["ContactTitle"]
            context.user_data['Date']=invoices[user_id]["invoice"]["Date"]
            context.user_data['DueDate']=invoices[user_id]["invoice"]["DueDate"]
            context.user_data['Jalali']=date
            reply_text = "تاریخ " + f"{date}" + "انتخاب شده است." + "حال کالاها را از لیست زیر انتخاب کنید."
            names = list(code_name_mappingkalakhadamatlist.keys())
            chunk_size = 30  
            page_number = context.user_data.get("page_number", 0)  

            start_index = page_number * chunk_size
            end_index = min((page_number + 1) * chunk_size, len(names))
            current_chunk = names[start_index:end_index]

            keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in current_chunk[i:i + 3]] for i in
                        range(0, len(current_chunk), 3)]

            
            pagination_buttons = []
            if page_number > 0:
                pagination_buttons.append(InlineKeyboardButton("◀️ قبلی", callback_data="previous"))
            if end_index < len(names):
                pagination_buttons.append(InlineKeyboardButton("بعدی ▶️", callback_data="next"))

            keyboard.append(pagination_buttons)

            markupkalakhadamatlist = InlineKeyboardMarkup(keyboard)

            await update.callback_query.message.reply_text('✳️ کالا و یا خدمات مورد نظر را انتخاب بفرمایید.' + ".\n.\n.\n.\n.\n",
                                            reply_markup=markupkalakhadamatlist)
            return FSA
        else:
            reply_text = "تاریخ " + f"{date}" + "انتخاب شده است." + "حال طبق الگو موارد زیر را وارد کنید. " + "\n\n" + " توضیحات فاکتور:" + "\n\n" + "وضعیت فاکتور:پیش نویس : 0  و تایید شده : 1 وارد شود" + "\n\n" + "الگو: ⬇️" + "\n\n"
            reply_text += "وضعیت-توضیحات کلی فاکتور" + "\n\n" + "اولین عدد به عنوان وضعیت و مابقی به عنوان توضیحات در نظر گرفته می شود."
            await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                           text=reply_text,
                                           reply_markup=rbarghashtmarkup)


            return FC
async def sabtfactorsari1(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    page_number = context.user_data.get("page_number", 0)
    names = list(code_name_mappingkalakhadamatlist.keys())
    chunk_size = 30  

    if query.data == "next":
        page_number += 1
    elif query.data == "previous":
        if page_number > 0:
            page_number -= 1

    start_index = page_number * chunk_size
    end_index = min((page_number + 1) * chunk_size, len(names))
    current_chunk = names[start_index:end_index]

    keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in current_chunk[i:i + 3]] for i in
                range(0, len(current_chunk), 3)]

    # Add pagination and complete buttons
    pagination_buttons = []
    if page_number > 0:
        pagination_buttons.append(InlineKeyboardButton("◀️ قبلی", callback_data="previous"))
    if end_index < len(names):
        pagination_buttons.append(InlineKeyboardButton("بعدی ▶️", callback_data="next"))
    pagination_buttons.append(InlineKeyboardButton("اتمام 🏁", callback_data="complete"))

    keyboard.append(pagination_buttons)
    markupkalakhadamatlist = InlineKeyboardMarkup(keyboard)
    context.user_data["page_number"] = page_number

    
    if query.data in ("next", "previous"):
        if context.user_data.get("selected_products"):
            a = invoicesaristr(context.user_data["selected_products"])
        else:
            a = "لطفا از لیست زیر کالاها و خدمات را انتخاب بفرمایید." + "\n.\n.\n.\n.\n.\n."
        await query.edit_message_text(text=a, reply_markup=markupkalakhadamatlist)
        await query.answer()
    elif query.data == "complete":
        
        if context.user_data.get("selected_products"):
            
            first_product = context.user_data["selected_products"][0]
            context.user_data['current_product'] = first_product  
            await query.message.reply_text("تعداد "+f" {first_product}"+"مشخص کنید.")
            return FSB  
        else:
            await query.answer("لطفا حتما یک کالا را انتخاب بفرمایید.")
    else:
        
        selected_product = query.data
        context.user_data.setdefault("selected_products", []).append(selected_product)
        a = invoicesaristr(context.user_data["selected_products"])
        await query.edit_message_text(text=a)
        asyncio.sleep(1)
        await query.edit_message_reply_markup(reply_markup=markupkalakhadamatlist)

    return FSA

async def sabtfactorsari2(update: Update, context: CallbackContext):
    message = update.message
    if not message or not message.text.isdigit():
        await message.reply_text("لطفا عدد وارد کنید.")
        return FSB

    quantity = int(message.text)
    current_product = context.user_data['current_product']
    if not context.user_data.get('quantities'):
        context.user_data['quantities'] = {}

    context.user_data['quantities'][current_product] = quantity

    
    products = context.user_data['selected_products']
    next_index = products.index(current_product) + 1
    if next_index < len(products):
        next_product = products[next_index]
        context.user_data['current_product'] = next_product
        await message.reply_text("تعداد "+f"  {next_product}"+" مشخص کنید.")
        return FSB  

    
    await message.reply_text("تعداد کالاها مشخص شد.")
    first_product = context.user_data["selected_products"][0]
    context.user_data['current_product'] = first_product 
    await message.reply_text("قیمت کالا یا خدمت "+f"  {first_product}"+" مشخص کنید.")
    return FSC  

async def sabtfactorsari3(update: Update, context: CallbackContext):
    message = update.message
    chat_id = update.message.chat_id
    if not message:
        await update.callback_query.answer("لطفا قیمت کالا را تایپ کنید.")
        return FSC
    if 'prices' not in context.user_data:
        context.user_data['prices'] = {}
    if message.text.startswith("#"):
        number = message.text[len("#"):]
        if number.isdigit():

            price = float(number)
            for product in context.user_data['selected_products']:
                context.user_data['prices'][product] = price
            text="برای همه اقلام قیمت اعمال شد."+"\n\n"
            text+="حال طبق الگو موارد زیر را وارد کنید. "  + "\n\n" + " توضیحات فاکتور:" + "\n\n" + "وضعیت فاکتور:پیش نویس : 0  و تایید شده : 1 وارد شود" + "\n\n"
            text+= "الگو: ⬇️" + "\n\n"+ "وضعیت-توضیحات کلی فاکتور" + "\n\n" + "اولین عدد به عنوان وضعیت و مابقی به عنوان توضیحات در نظر گرفته می شود."

            await message.reply_text(text)
            return FSD
        else:
            await message.reply_text("لطفا یک عدد برای قیمت وارد کنید.")
            return FSC





    
    if not message.text.replace('.', '', 1).isdigit():
        await message.reply_text("لطفا یک عدد برای قیمت وارد کنید.")
        return FSC

    price = float(message.text)
    current_product = context.user_data.get('current_product')
    print(current_product)
    if not current_product:
        
        await message.reply_text("خطا: هیچ کالایی برای قیمت مشخص نشده است.")
        return FSC

    


    
    context.user_data['prices'][current_product] = price

    
    products = context.user_data.get('selected_products', [])
    current_index = products.index(current_product)
    
    
    if current_index + 1 < len(products):
        next_product = products[current_index + 1]
        context.user_data['current_product'] = next_product
        await message.reply_text("قیمت کالا یا خدمت "+f" {next_product}"+" مشخص کنید.")
        return FSC

    text = "برای همه اقلام قیمت اعمال شد." + "\n\n"
    text += "حال طبق الگو موارد زیر را وارد کنید. " + "\n\n" + " توضیحات فاکتور:" + "\n\n" + "وضعیت فاکتور:پیش نویس : 0  و تایید شده : 1 وارد شود" + "\n\n"
    text += "الگو: ⬇️" + "\n\n" + "وضعیت-توضیحات کلی فاکتور" + "\n\n" + "اولین عدد به عنوان وضعیت و مابقی به عنوان توضیحات در نظر گرفته می شود."

    await message.reply_text(text)
    return FSD

async def sabtfactorsari4(update: Update, context: CallbackContext):
    message = update.message
    chat_id = update.message.chat_id
    context.user_data["Status"], context.user_data["Note"] = parse_status_and_note(update.message.text)
    create_invoice_image(context.user_data)
    with open('invoice.png', 'rb') as photo:
        await context.bot.send_photo(update.message.chat_id, photo=photo,
                                     caption="در صورت اطمینان تایید کنید.",
                                     reply_markup=markupsabt)


    return FSE
async def sabtfactorsari5(update: Update, context: CallbackContext):
    message = update.message
    chat_id = update.message.chat_id
    processed_products = process_invoice_data(context.user_data,code_name_mappingkalakhadamatlist)
    data={'apiKey':apiKey,'loginToken':loginToken,'invoice':{'Date':context.user_data["Date"],
                                                             'DueDate':context.user_data["Date"],
                                                             'ContactCode':context.user_data["contactCode"],
                                                             'ContactTitle':context.user_data["ContactTitle"]
                                                             ,'InvoiceType':context.user_data["InvoiceType"],'Status':context.user_data["Status"],
    'Note':context.user_data["Note"],'InvoiceItems': processed_products },}
    print(data)
    urlsavefactor = "https://api.hesabfa.com/v1/invoice/save"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(urlsavefactor, json=data, headers=headers)
    context.user_data.clear()
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        max_message_length = 4096  
        chunks = [result_str[i:i + max_message_length] for i in range(0, len(result_str), max_message_length)]
        for chunk in chunks:
            await context.bot.send_message(chat_id=chat_idreport, text=chunk)
        if result.get("Success"):
            r = result.get("Result")
            await update.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
        "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    return A
async def sabtfactor4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    user_id = update.message.from_user.id
    invoices[user_id]["invoice"]["Status"],invoices[user_id]["invoice"]["Note"]=parse_status_and_note(update.message.text)

    invoices[user_id]["invoice"]["InvoiceItems"] = []
    names = list(code_name_mappingkalakhadamatlist.keys())
    chunk_size = 90
    name_chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]
    i = 0
    for chunk in name_chunks:
        keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in chunk[i:i + 3]] for i in
                    range(0, len(chunk), 3)]
        markupkalakhadamatlist = InlineKeyboardMarkup(keyboard)
        if i == 0:
            await update.message.reply_text('✳️ کالا و یا خدمات مورد نظر را انتخاب بفرمایید.' + ".\n.\n.\n.\n.\n",
                                            reply_markup=markupkalakhadamatlist)
        else:
            r = "90  کالا و خدمات بعدی:"
            await update.message.reply_text(r, reply_markup=markupkalakhadamatlist)
        i = i + 1
    return FD
async def sabtfactor4inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    query = update.inline_query.query
    if not query:
        return
    names = list(code_name_mappingkalakhadamatlist.keys())
    if names is None:
        return
    filtered_results = [name for name in names if query.upper() in name.upper()]
    results = [InlineQueryResultArticle(id=str(index),
            title=name,
            input_message_content=InputTextMessageContent(name),
        ) for index, name in enumerate(filtered_results[:50]) 
    ]
   
    await update.inline_query.answer(results)
    return FD
async def sabtfactor5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    query = update.callback_query
    if query:
        user_id = query.from_user.id
        text = query.data
        desired_code = code_name_mappingkalakhadamatlist[text]
        element = {"Description": None, "Quantity": None, "UnitPrice": None, "Discount": None, "Tax": None,
                   "ItemCode": desired_code}
        invoices[user_id]["invoice"]["InvoiceItems"].append(element)
        r1 = f"❇شما کالا یا خدمات {text} را انتخاب کرده اید." + "\n" + "حال طبق الگوی زیر به ترتیب تعداد-قیمت واحد-توضیحات کالا یا خدمات را وارد نمایید."
        r2 = "\n" + "تعداد:" + "\n" + "مبلغ:" + "\n" + "شرح: اگر صفر وارد کنید نام کالا در قسمت شرح وارد می شود." + "\n" + "الگو: ⬇️" + "\n" + "تعداد-مبلغ-شرح"
        await query.message.reply_text(r1 + r2, reply_markup=rbarghashtmarkup)
    else:
        text = update.message.text
        user_id = update.message.from_user.id
        desired_code = code_name_mappingkalakhadamatlist[text]
        element = {"Description": None, "Quantity": None, "UnitPrice": None, "Discount": None, "Tax": None,
                   "ItemCode": desired_code}
        invoices[user_id]["invoice"]["InvoiceItems"].append(element)
        r1 = f"❇شما کالا یا خدمات {text} را انتخاب کرده اید." + "\n" + "حال طبق الگوی زیر به ترتیب تعداد-قیمت واحد-توضیحات کالا یا خدمات را وارد نمایید."
        r2 = "\n" + "تعداد:" + "\n" + "مبلغ:" + "\n" + "شرح: اگر صفر وارد کنید نام کالا در قسمت شرح وارد می شود." + "\n" + "الگو: ⬇️" + "\n" + "تعداد-مبلغ-شرح"
        await update.message.reply_text(r1 + r2, reply_markup=rbarghashtmarkup)
    return FE
async def sabtfactor6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    user_id = update.message.from_user.id
    text = update.message.text
    pattern = r'[.,\-:_]'
    parts = re.split(pattern, text)
    quantity = ''.join(filter(str.isdigit, parts[0]))
    unit_price = ''.join(filter(str.isdigit, parts[1]))
    description = parts[2]

    invoices[user_id]['invoice']['InvoiceItems'][-1]["Description"] = description
    if description == '0':
        description = next((key for key, value in code_name_mappingkalakhadamatlist.items() if
                            value == invoices[user_id]['invoice']['InvoiceItems'][-1]["ItemCode"]), None)
        invoices[user_id]['invoice']['InvoiceItems'][-1]["Description"] = description
    invoices[user_id]['invoice']['InvoiceItems'][-1]["Quantity"] = int(quantity)
    invoices[user_id]['invoice']['InvoiceItems'][-1]["UnitPrice"] = int(unit_price)
    invoices[user_id]['invoice']['InvoiceItems'][-1]["Discount"] = 0
    invoices[user_id]['invoice']['InvoiceItems'][-1]["Tax"] = 0
    r = invoicetostr(invoices, user_id)
    reply_keyboardf = [['ثبت فاکتور'], ['افزودن کالا یا خدمات'], ['برگشت']]
    markupf = ReplyKeyboardMarkup(reply_keyboardf, one_time_keyboard=True)
    r="❇" + f"اگر عملیات ثبت فاکتور به اتمام رسیده است ( ثبت فاکتور ) را انتخاب نمایید در غیر اینصورت جهت اضافه کردن کالا یا خدمات جدید ( افزودن کالا یا خدمات ) را انتخاب بفرمایید{r}"
    max_message_length = 4096  
    chunks = [r[i:i + max_message_length] for i in range(0, len(r), max_message_length)]
    for chunk in chunks:
        await update.message.reply_text(chunk,reply_markup=markupf)
    return FF
async def sabtfactor7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    names = list(code_name_mappingkalakhadamatlist.keys())
    chunk_size = 100
    name_chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]
    i = 0
    for chunk in name_chunks:
        keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in chunk[i:i + 3]] for i in
                    range(0, len(chunk), 3)]
        markupkalakhadamatlist = InlineKeyboardMarkup(keyboard)
        if i == 0:
            await update.message.reply_text('✳️ کالا و یا خدمات مورد نظر را انتخاب بفرمایید.' + ".\n.\n.\n.\n.\n",
                                            reply_markup=markupkalakhadamatlist)
        else:
            r = "100  کالا و خدمات بعدی:"
            await update.message.reply_text(r, reply_markup=markupkalakhadamatlist)
        i = i + 1
    return FD
async def sabtfactor8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global invoices
    urlsavefactor = "https://api.hesabfa.com/v1/invoice/save"
    user_id = update.message.from_user.id
    data = invoices[user_id]
    headers = {'Content-Type': 'application/json'}
    response = requests.post(urlsavefactor, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
        max_message_length = 4096  
        chunks = [result_str[i:i + max_message_length] for i in range(0, len(result_str), max_message_length)]
        for chunk in chunks:
            await context.bot.send_message(chat_id=chat_idreport, text=chunk)
        if result.get("Success"):
            r = result.get("Result")
            await update.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
        else:
            await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
        "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await update.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    del invoices[user_id]
    return A


async def gozareshat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
        return A
    reply_text = f"شما {text} را انتخاب کرده اید."
    reply_keyboardg = [['آخرین اسناد مالی', 'موجودی بانک ها','گزارش بستانکار بدهکار' ],['برگشت']]
    markupg = ReplyKeyboardMarkup(reply_keyboardg, one_time_keyboard=True)
    await update.message.reply_text(reply_text, reply_markup=markupg)
    return GOaA


async def gozareshatbank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.message.from_user.id
    sorted_banks_info = get_bank_info(apiKey, loginToken, all_info=True)

    for index, (name, balance, code) in enumerate(sorted_banks_info, start=1):
        amount = "{:,}".format(int(balance))

        print(name)

        logo_path = None
        for bank_name, logo_file in bank_logos.items():
            if bank_name in name:
                logo_path = os.path.join('bankslogo', logo_file)
                break

        if logo_path is None or not os.path.exists(logo_path):
            
            logo_path = os.path.join('bankslogo', 'default.jpg')

        dash_index = name.find('-')
        if dash_index != -1:
            name = name[dash_index + 1:].strip()

        caption = '🏦' + f" {name}" + "\n" + "💰موجودی: " + f"{amount}" + " ریال" + "\n" + f"#BANK{code}"
        website = None
        for bank_name, site in bank_websites.items():
            if bank_name in name:
                website = site
                break
        if website:
            caption += f"\n🌐{website}"
        

        with open(logo_path, "rb") as photo_file:
            await context.bot.send_document(chat_id=user_id, document=photo_file, caption=caption)

        asyncio.sleep(2)

    await update.message.reply_text("موجودی بانک ها فرستاده شد.", reply_markup=markup)
    return A
async def amaliat1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .", reply_markup=markupun)
        return A

    
    context.user_data['report'] = {
        "apiKey": apiKey,
        "loginToken": loginToken,
    }
    reply_text = "تاریخ شروع را انتخاب کنید (برای سال مالی خود حسابفا '0' را وارد کنید)." + "\n\n"
    await update.message.reply_text(text=reply_text, reply_markup=telegramjcalendar.create_calendar())
    return GOBA
async def amaliat2(update: Update, context: CallbackContext):
    if update.callback_query:
        query=update.callback_query
        selected, date = await telegramjcalendar.process_calendar_selection(context.bot, update)
        if selected:
            context.user_data['report']['startDate'] = convert_to_gregorian( date)
            reply_text = "تاریخ پایان را انتخاب کنید. (برای سال مالی خود حسابفا '0' را وارد کنید)." + "\n\n"
            await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                           text=reply_text,
                                           reply_markup=telegramjcalendar.create_calendar())
            return GOBB
    elif update.message.text == '0':  
        reply_text = "تاریخ شروع سال مالی حسابفا قرار گرفت.تاریخ پایان را انتخاب کنید (برای سال مالی خود حسابفا '0' را وارد کنید. "
        await context.bot.send_message(chat_id = update.message.from_user.id,
                                       text=reply_text,
                                       reply_markup=telegramjcalendar.create_calendar())
        return GOBB


async def amaliat3(update: Update, context: CallbackContext):
    if update.callback_query:
        selected, date = await telegramjcalendar.process_calendar_selection(context.bot, update)
        if selected:
            context.user_data['report']['endDate'] = convert_to_gregorian(date)
            await handle_debtors_creditors_report(update, context) 
            return A
    elif update.message.text == '0':
        await handle_debtors_creditors_report(update, context)  
        return A
async def resid1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.message.from_user.id
    if str(user_id) not in autorizedusers or autorizedusers[str(user_id)]['active'] != 1:
        await update.message.reply_text("شما مجاز به استفاده از این عملیات نیستید .",reply_markup=markup)
        return A
    reply_text = f"شما {text} را انتخاب کرده اید."
    await update.message.reply_text(reply_text, reply_markup=rbarghashtmarkup)
    keyboard = [[InlineKeyboardButton(name, callback_data=name) for name in rresid[i:i + 2]] for i in
                range(0, len(rresid), 2)]
    markupresid = InlineKeyboardMarkup(keyboard)
    reply_text = "گزینه مورد نظر  را از زیر انتخاب بفرمایید و گزارش در کانال آخرین اسناد مالی دریافت پرداخت فرستاده می شود. "
    await update.message.reply_text(reply_text, reply_markup=markupresid)
    return GOA
async def resid2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id  
    text = query.data
    reply_text = f"سلام شما {text} را انتخاب کرده اید."
    await query.message.reply_text(reply_text, reply_markup=markup)
    headers = {'Content-Type': 'application/json'}
    skip = 0
    type = None
    if "دریافت" in text:
        type = 1
    elif "پرداخت" in text:
        type = 2
    if "اول" in text:
        skip = 0
    elif "دوم" in text:
        skip = 100
    elif "سوم" in text:
        skip = 200
    elif "چهارم" in text:
        skip = 300
    elif "پنجم" in text:
        skip = 400
    data = {"apiKey": apiKey, "loginToken": loginToken, "type": type,
            "queryInfo": {"SortBy": 'DateTime', "SortDesc": True, "Take": 100, "Skip": skip}}
    response = requests.post('https://api.hesabfa.com/v1/receipt/getReceipts', json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("Success"):
            r = result.get("Result")
            concatenated_text = ""
            await query.message.reply_text("درخواست موفقیت آمیز بود.", reply_markup=markup)
            for index, rr in enumerate(r['List'], start=1):
                amount = int(rr['Amount'])
                formatted_amount = "{:,}".format(amount)
                parsed_date = datetime.datetime.strptime(rr['DateTime'], '%Y-%m-%dT%H:%M:%S')
                jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
                a = "🗒" + "شماره رسید : " + f"{rr['Number']}" + "\n" \
                                                                 f"تاریخ : {jalili_date}" + "\n" \
                                                                                            f"توضیحات : {rr['Description']}\n" \
                                                                                            f" مقدار تراکنش : {formatted_amount}" + " ریال" + "\n\n\n"
                concatenated_text += a
                if index % 10 == 0 or index == len(r['List']):
                    await context.bot.send_message(chat_id="@asnadmalihesabfa", text=concatenated_text)
                    concatenated_text = ""
        else:
            await query.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    else:
        text = ("Request failed with status code:", response.status_code) + (
            "\nResponse content:", response.content.decode('utf-8'))
        await context.bot.send_message(chat_id=chat_idreport, text=text)
        await query.message.reply_text("درخواست انجام نشد.", reply_markup=markup)
    return A
async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    callback_data = query.data
    user_id = query.from_user.id
    logger.warning(f'User ID: {user_id}, Callback Data: {callback_data}, Time: {datetime.datetime.now()}')
    current_time = datetime.datetime.now()
    
    
    
    if callback_data in last_click_times:
        last_click_time = last_click_times[callback_data]
        if (current_time - last_click_time).total_seconds() < 30:
            await query.answer(text='شما دوباره کمتر از 30 ثانیه روی کلید کلیک کرده اید.', show_alert=True)
            return
    
    
    last_click_times[callback_data] = current_time
    
    parts = callback_data.split('_')
    if callback_data.startswith("cancel"):
        await query.answer(text='شما لغو را انتخاب نموده اید. منتظر تغییرات باشید.', show_alert=True)
        await handle_cancel_operation(query, callback_data, context)
    elif callback_data.startswith("hazf"):
        await handle_hazf_operation(query, callback_data, context)
    elif len(parts) >= 3:  
        await query.answer(text='شما انتخاب نموده اید. منتظر تغییرات باشید.', show_alert=True)
        await handle_numeric_callback(query, callback_data, context)
    else:
        pass

async def handle_numeric_callback(query, callback_data, context):
    if callback_data.startswith("jarimeyeshakhs"):
        callback_data = query.data[len("jarimeyeshakhs"):]
        operation = load_data(callback_data)
    elif callback_data.startswith("jarimeye"):
        callback_data = query.data[len("jarimeye"):]
        operation = load_data(callback_data)
    else:
        operation = load_data(callback_data)
    if isinstance(operation, Operationenteghal):
        await handle_operationenteghal(query, operation, context)
    elif isinstance(operation, Operationhazine):
        await handle_operationhazine(query, operation, context)
    elif isinstance(operation, Operationdaryaft):
        await handle_operationdaryaft(query, operation, context)
    elif isinstance(operation,  Operationhahavale):
        await handle_operationhavale(query, operation, context)

async def handle_operationhavale(query, operation, context):
    if query.data.startswith("jarimeyeshakhs"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response = operation.jarimeshakhs(
            Note="تاریخ ثبت درخواست:" + f"{operation.date}" + "زمان ثبت درخواست :" + f"{operation.time}" + "هشتگ جریمه:" + f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup =query.message.reply_markup.inline_keyboard[0:-1]+((InlineKeyboardButton("👤جریمه شد .هشتگ جریمه :" + f"{h}", callback_data='a'),
                                    ),)
                operation.jarimenumbershakhs=h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text = '❌️سلام وقت شما بخیر ❌️' + "\n\n"
                text += 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' + "\n\n"
                text += '⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text += 'به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.' + "\n\n"
                text += 'با تشکر🙏🏻' + "\n\n"
                text += "📆تاریخ ثبت درخواست:" + f"{operation.date}" + "\n" + "⏰زمان ثبت درخواست :" + f"{operation.time}"
                try:
                    await context.bot.send_message(chat_id=operation.tarafhesab,text=text)
                except:
                    pass
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a = "پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                    (InlineKeyboardButton(f"👤{a}", callback_data='a'),),)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)

        else:
            pass


    elif query.data.startswith("jarimeye"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response = operation.jarime(
            Note="تاریخ ثبت درخواست:" + f"{operation.date}" + "زمان ثبت درخواست :" + f"{operation.time}" + "هشتگ جریمه:" + f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup = query.message.reply_markup.inline_keyboard[0:-2] + (
                (InlineKeyboardButton("🛃جریمه شد.هشتگ جریمه :" + f"{h}", callback_data='a'),),)+(query.message.reply_markup.inline_keyboard[-1],)
                operation.jarimenumber=h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text = '❌️سلام وقت شما بخیر ❌️' + "\n\n"
                text += 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' + "\n\n"
                text += '⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text += 'به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.' + "\n\n"
                text += 'با تشکر🙏🏻' + "\n\n"
                text += "📆تاریخ ثبت درخواست:" + f"{operation.date}" + "\n" + "⏰زمان ثبت درخواست :" + f"{operation.time}"
                await context.bot.send_message(chat_id=operation.chat_id,
                                               text=text)
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a = "پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-2] + (
                    (InlineKeyboardButton(f"🛃{a}", callback_data='a'),),)+(query.message.reply_markup.inline_keyboard[-1],)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)

        else:
            pass
    else:
        response1 = operation.post1()
        asyncio.sleep(2)
        response2 = operation.post2()
        aa = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}")])
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result_str1 = json.dumps(result1, separators=(',', ':'), ensure_ascii=False)
            result2 = response2.json()
            result_str2 = json.dumps(result2, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str1)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str2)

            if result1.get("Success") and result2.get("Success"):
                a, o = havalestr(operation, result1, result2)
                c = "✅✅✅✅✅✅✅" + "\n"
                markuphazf=InlineKeyboardMarkup.from_column(
                [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
                    InlineKeyboardButton('حذف رسیدها', callback_data='hazf1' + f"{query.data}")],
                )
                await query.edit_message_caption(caption=c + a, reply_markup=markuphazf)
                operation.residhesabfa1 = result1['Result']['Number']
                operation.residhesabfa2 = result2['Result']['Number']
                save_data2(operation)

                with open("residsabz.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                    photo_file.seek(0)
                    try:
                        await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                     caption=c + o)
                    except:
                        pass
            else:
                c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
                a, o = havalestr(operation, result1, result2)
                await query.edit_message_caption(caption=c + a, reply_markup=aa)
                with open("residghermez.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                    photo_file.seek(0)
                    try:
                        await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                     caption=c + o)
                    except:
                        pass
        elif response1.status_code != 200 or response2.status_code != 200:
            c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
            if response1.status_code != 200:
                c += "سرور حسابفا مرحله اول پاسخ نداد." + "\n"
                result1 = None
            else:
                result1 = response1.json()
                result_str1 = json.dumps(result1, separators=(',', ':'), ensure_ascii=False)
                await context.bot.send_message(chat_id=chat_idreport, text=result_str1)

                if result1.get("Success"):
                    r1 = result1.get("Result")
            if response2.status_code != 200:
                c += "سرور حسابفا مرحله دوم پاسخ نداد." + "\n"
                result2 = None
            else:
                result2 = response2.json()
                result_str2 = json.dumps(result2, separators=(',', ':'), ensure_ascii=False)
                await context.bot.send_message(chat_id=chat_idreport, text=result_str2)

                if result2.get("Success"):
                    r2 = result2.get("Result")
            a, o = havalestr(operation, result1, result2)
            await query.edit_message_caption(caption=c + a, reply_markup=aa)
            with open("residghermez.jpg", "rb") as photo_file:
                await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                photo_file.seek(0)
                try:
                    await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                 caption=c + o)
                except:
                    pass
            text = ("سرور پاسخ نداد.", response1.status_code) + (
                "\nResponse content:", response1.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)


async def handle_operationenteghal(query, operation, context):
    if query.data.startswith("jarimeye"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response = operation.jarime(
            Note="تاریخ ثبت درخواست:" + f"{operation.date}" + "زمان ثبت درخواست :" + f"{operation.time}" + "هشتگ جریمه:" + f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                (InlineKeyboardButton("🛃جریمه اش کردم.هشتگ جریمه :" + f"{h}", callback_data='a'),),)
                operation.jarimenumber=h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text = '❌️سلام وقت شما بخیر ❌️' + "\n\n"
                text += 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' + "\n\n"
                text += '⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text += 'به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.' + "\n\n"
                text += 'با تشکر🙏🏻' + "\n\n"
                text += "📆تاریخ ثبت درخواست:" + f"{operation.date}" + "\n" + "⏰زمان ثبت درخواست :" + f"{operation.time}"
                await context.bot.send_message(chat_id=operation.chat_id,
                                               text=text)
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a = "پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                    (InlineKeyboardButton(f"🛃{a}", callback_data='a'),),)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)

        else:
            pass

    else:
        response1 = operation.post1()
        asyncio.sleep(2)
        response2 = operation.post2()
        aa = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}")])
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result_str1 = json.dumps(result1, separators=(',', ':'), ensure_ascii=False)
            result2 = response2.json()
            result_str2 = json.dumps(result2, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str1)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str2)

            if result1.get("Success") and result2.get("Success"):
                a, o = enteghalstr(operation, result1, result2)
                c = "✅✅✅✅✅✅✅" + "\n"
                markuphazf = InlineKeyboardMarkup.from_column(
                    [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
                     InlineKeyboardButton('حذف رسیدها', callback_data='hazf1' + f"{query.data}")],
                )
                await query.edit_message_caption(caption=c + a, reply_markup=markuphazf)
                operation.residhesabfa1 = result1['Result']['Number']
                operation.residhesabfa2 = result2['Result']['Number']
                save_data2(operation)
                with open("residsabz.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
            else:
                c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
                a, o = enteghalstr(operation, result1, result2)
                await query.edit_message_caption(caption=c + a, reply_markup=aa)
                with open("residghermez.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
        elif response1.status_code != 200 or response2.status_code != 200:
            c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
            if response1.status_code != 200:
                c += "سرور حسابفا مرحله اول پاسخ نداد." + "\n"
                result1 = None
            else:
                result1 = response1.json()
                result_str1 = json.dumps(result1, separators=(',', ':'), ensure_ascii=False)
                await context.bot.send_message(chat_id=chat_idreport, text=result_str1)

                if result1.get("Success"):
                    r1 = result1.get("Result")
            if response2.status_code != 200:
                c += "سرور حسابفا مرحله دوم پاسخ نداد." + "\n"
                result2 = None
            else:
                result2 = response2.json()
                result_str2 = json.dumps(result2, separators=(',', ':'), ensure_ascii=False)
                await context.bot.send_message(chat_id=chat_idreport, text=result_str2)

                if result2.get("Success"):
                    r2 = result2.get("Result")
            a, o = enteghalstr(operation, result1, result2)
            await query.edit_message_caption(caption=c + a, reply_markup=aa)
            with open("residghermez.jpg", "rb") as photo_file:
                await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
            text = ("سرور پاسخ نداد.", response1.status_code) + (
                "\nResponse content:", response1.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)
async def handle_operationhazine(query, operation, context):
    if query.data.startswith("jarimeye"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response=operation.jarime(Note="تاریخ ثبت درخواست:" +f"{operation.date}"+"زمان ثبت درخواست :"+f"{operation.time}"+"هشتگ جریمه:"+f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1]+((InlineKeyboardButton("🛃جریمه اش کردم.هشتگ جریمه :"+f"{h}", callback_data='a'),),)
                operation.jarimenumber = h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text='❌️سلام وقت شما بخیر ❌️'+"\n\n"
                text+= 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' +"\n\n"
                text+='⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text+='به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.'+"\n\n"
                text+='با تشکر🙏🏻'+"\n\n"
                text+="📆تاریخ ثبت درخواست:" +f"{operation.date}"+"\n" +"⏰زمان ثبت درخواست :"+f"{operation.time}"
                await context.bot.send_message(chat_id=operation.chat_id,
                                         text=text)
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a="پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                (InlineKeyboardButton(f"🛃{a}", callback_data='a'),),)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)

        else:
            pass

    else:
        response = operation.post()
        aa = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}")])
        
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)

            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                a, o = hazinestr(operation, result)
                c = "✅✅✅✅✅✅✅" + "\n"
                markuphazf = InlineKeyboardMarkup.from_column(
                    [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
                     InlineKeyboardButton('حذف رسید', callback_data='hazf1' + f"{query.data}")],
                )
                await query.edit_message_caption(caption=c + a, reply_markup=markuphazf)
                operation.residhesabfa = result['Result']['Number']
                save_data2(operation)
                with open("residsabz.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)

            else:
                c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
                a, o = hazinestr(operation, result)
                await query.edit_message_caption(caption=c + a, reply_markup=aa)
                with open("residghermez.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
        else:
            c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n" + "سرور حسابفا پاسخ نداد" + "\n"
            a, o = hazinestr(operation, None)
            await query.edit_message_caption(caption=c + a, reply_markup=aa)
            with open("residghermez.jpg", "rb") as photo_file:
                await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
            text = ("سرور پاسخ نداد.", response.status_code) + (
                "\nResponse content:", response.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)
async def handle_operationdaryaft(query, operation, context):
    if query.data.startswith("jarimeyeshakhs"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response = operation.jarimeshakhs(
            Note="تاریخ ثبت درخواست:" + f"{operation.date}" + "زمان ثبت درخواست :" + f"{operation.time}" + "هشتگ جریمه:" + f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                (InlineKeyboardButton("👤جریمه شد .هشتگ جریمه :" + f"{h}", callback_data='a'),
                 ),)
                operation.jarimenumbershakhs = h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text = '❌️سلام وقت شما بخیر ❌️' + "\n\n"
                text += 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' + "\n\n"
                text += '⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text += 'به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.' + "\n\n"
                text += 'با تشکر🙏🏻' + "\n\n"
                text += "📆تاریخ ثبت درخواست:" + f"{operation.date}" + "\n" + "⏰زمان ثبت درخواست :" + f"{operation.time}"
                try:
                    await context.bot.send_message(chat_id=operation.tarafhesab, text=text)
                except:
                    pass
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a = "پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-1] + (
                    (InlineKeyboardButton(f"👤{a}", callback_data='a'),),)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)

        else:
            pass
    elif query.data.startswith("jarimeye"):
        h = str(dichashtag["idjarime"]).zfill(6)
        response = operation.jarime(
            Note="تاریخ ثبت درخواست:" + f"{operation.date}" + "زمان ثبت درخواست :" + f"{operation.time}" + "هشتگ جریمه:" + f"{h}")
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                r = result.get("Result")
                existing_markup = query.message.reply_markup.inline_keyboard[0:-2] + (
                    (InlineKeyboardButton("🛃جریمه شد.هشتگ جریمه :" + f"{h}", callback_data='a'),),) + \
                                  (query.message.reply_markup.inline_keyboard[-1],)
                operation.jarimenumber = h
                save_data1(operation)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
                text = '❌️سلام وقت شما بخیر ❌️' + "\n\n"
                text += 'اپراتور محترم با توجه به اعلام به شما در خصوص ارسال رسید واریزی در تاریخ روز جاری رسید و عمل نکردن به این مورد مهم  شما به علت بر هم زدن نظم و ایجاد خلل و مغایرت در سیستم حسابداری مبلغ ۱۰۰ هزار تومان جریمه شده اید' + "\n\n"
                text += '⏱️ از این پس با ارسال به موقع اسناد حسابداری از این رویداد جلوگیری فرمایید ، ضمنا مبلغ فوق پس از دریافت از شما به حساب موسسه خیریه محک واریز شده و می توانید درخواست دریافت رسید را بدهید تا قبض واریزی برای شما ارسال شود.'
                text += 'به زودی تمامی خدمات برای شما غیر فعال شده تا مبلغ فوق را واریز کرده و رسید آن را ارسال فرمایید.' + "\n\n"
                text += 'با تشکر🙏🏻' + "\n\n"
                text += "📆تاریخ ثبت درخواست:" + f"{operation.date}" + "\n" + "⏰زمان ثبت درخواست :" + f"{operation.time}"
                await context.bot.send_message(chat_id=operation.chat_id,
                                               text=text)
                dichashtag["idjarime"] = dichashtag["idjarime"] + 1
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            else:
                a = "پیام خطای حسابفا: " + f"{result['ErrorMessage']}"
                existing_markup = query.message.reply_markup.inline_keyboard[0:-2] + (
                    (InlineKeyboardButton(f"🛃{a}", callback_data='a'),),) + (query.message.reply_markup.inline_keyboard[-1],)
                aa = InlineKeyboardMarkup(existing_markup)
                await query.edit_message_reply_markup(reply_markup=aa)
    else:
        response = operation.post()
        aa = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}")])
        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)

            await context.bot.send_message(chat_id=chat_idreport, text=result_str)
            if result.get("Success"):
                a, o = daryaftstr(operation, result)
                c = "✅✅✅✅✅✅✅" + "\n"
                markuphazf = InlineKeyboardMarkup.from_column(
                    [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
                     InlineKeyboardButton('حذف رسید', callback_data='hazf1' + f"{query.data}")],
                )
                await query.edit_message_caption(caption=c + a, reply_markup=markuphazf)
                operation.residhesabfa = result['Result']['Number']
                save_data2(operation)

                with open("residsabz.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                    photo_file.seek(0)
                    try:
                        await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                     caption=c + o)
                    except:
                        pass
            else:
                c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n"
                a, o = daryaftstr(operation, result)
                await query.edit_message_caption(caption=c + a, reply_markup=aa)
                with open("residghermez.jpg", "rb") as photo_file:
                    await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                    photo_file.seek(0)
                    try:
                        await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                     caption=c + o)
                    except:
                        pass
        else:
            c = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n" + "سرور حسابفا پاسخ نداد" + "\n"
            a, o = daryaftstr(operation, None)
            await query.edit_message_caption(caption=c + a, reply_markup=aa)
            with open("residghermez.jpg", "rb") as photo_file:
                await context.bot.send_photo(chat_id=operation.chat_id, photo=photo_file, caption=c + o)
                photo_file.seek(0)
                try:
                    await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file,
                                                 caption=c + o)
                except:
                    pass
            text = ("سرور پاسخ نداد.", response.status_code) + (
                "\nResponse content:", response.content.decode('utf-8'))
            await context.bot.send_message(chat_id=chat_idreport, text=text)


async def handle_cancel_operation(query, callback_data, context):
    if query.data.startswith("cancel"):
        callback_data = query.data[len("cancel"):]
        operation = load_data(callback_data)
        user_id = int(operation.user_id)
        chat_id = int(operation.chat_id)
        caption = "❌❌❌❌❌❌❌❌❌❌❌❌❌"+"\n\n" +"مدیر درخواست شما را تایید نکرد." + "\n\n" + f"{query.message.caption}"
        lines = caption.split('\n')
        filtered_lines = [line for line in lines if not line.startswith("🛃")]
        captionoperator = '\n'.join(filtered_lines)
        captionoperator = captionoperator.replace("#WAITING", "")
        aa = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={user_id}")])
        with open("residghermez.jpg", "rb") as photo_file:
            await context.bot.send_photo(chat_id=chat_id, photo=photo_file, caption=captionoperator)
            photo_file.seek(0)
            try:
                await context.bot.send_photo(chat_id=operation.tarafhesab, photo=photo_file, caption=captionoperator)
            except:
                pass
        caption = "❌❌❌❌❌❌❌❌❌❌❌❌❌" + "\n\n" + f"{query.message.caption}"
        caption = caption.replace("#WAITING", "")
        await query.edit_message_caption(caption="شما درخواست را لغو کرده اید."+"\n" + caption, reply_markup=aa)
async def handle_hazf_operation(query, callback_data, context):
    if query.data.startswith("hazf1"):
        await query.answer(text='شما برای بار اول این کلید را انتخاب نموده اید. در صورت اطمینان دوباره کلیک کنید.',show_alert=True)
        callback_data = query.data[len("hazf1"):]
        print(callback_data)
        operation = load_data(callback_data)
        markuphazf = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
             InlineKeyboardButton('⚠️حذف رسید', callback_data='hazf2' + f"{callback_data}")],
        )
        await query.edit_message_reply_markup(reply_markup=markuphazf)
    elif query.data.startswith("hazf2"):
        await query.answer(text='شما بار دوم انتخاب نموده اید. رسید حذف می شود.', show_alert=True)
        callback_data = query.data[len("hazf2"):]
        operation = load_data(callback_data)
        if isinstance(operation, Operationenteghal) or isinstance(operation, Operationhahavale):
                response1 = operation.hazf1()
                if response1.status_code == 200:
                    result1 = response1.json()
                    result_str1 = json.dumps(result1, separators=(',', ':'), ensure_ascii=False)
                    await context.bot.send_message(chat_id=chat_idreport, text=result_str1)
                    if result1.get("Success"):
                        residaval = InlineKeyboardButton('❌❌❌حذف موفقیت آمیز رسید اول❌❌❌', callback_data='None')
                    else:
                        residaval = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید اول❌❌❌❌❌❌', callback_data='None')
                else:
                    residaval = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید اول❌❌❌❌❌❌', callback_data='None')
                response2 = operation.hazf2()
                if response2.status_code == 200:
                    result2 = response2.json()
                    result_str2 = json.dumps(result2, separators=(',', ':'), ensure_ascii=False)
                    await context.bot.send_message(chat_id=chat_idreport, text=result_str2)
                    if result2.get("Success"):
                        residdovom = InlineKeyboardButton('❌❌❌حذف موفقیت آمیز رسید دوم❌❌❌', callback_data='None')
                    else:
                        residdovom = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید دوم❌❌❌❌❌❌', callback_data='None')
                else:
                    residdovom = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید دوم❌❌❌❌❌❌', callback_data='None')
                aa = InlineKeyboardMarkup.from_column(
                    [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"),
                     residaval, residdovom])
        elif isinstance(operation, Operationhazine) or isinstance(operation, Operationdaryaft):
                response = operation.hazf()
                print(response)
                if response.status_code == 200:
                    result = response.json()
                    result_str = json.dumps(result, separators=(',', ':'), ensure_ascii=False)
                    await context.bot.send_message(chat_id=chat_idreport, text=result_str)
                    if result.get("Success"):
                        resid = InlineKeyboardButton('❌❌❌حذف موفقیت آمیز رسید❌❌❌', callback_data='None')
                    else:
                        resid = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید❌❌❌❌❌❌', callback_data='None')
                else:
                    resid = InlineKeyboardButton('❌❌❌❌❌❌خطای حذف رسید❌❌❌❌❌❌', callback_data='None')
                aa = InlineKeyboardMarkup.from_column(
                    [InlineKeyboardButton('ارسال پیام به اپراتور', url=f"tg://user?id={operation.user_id}"), resid])
        user_id = int(operation.user_id)
        chat_id = int(operation.chat_id)
        caption = "" + "\n\n" + f"{query.message.caption}"
        caption += "\n" + f"#DEL{str(dichashtag['iddelete']).zfill(6)}"
        await query.edit_message_caption(caption="شما درخواست حذف رسید کرده اید." + "\n" + caption, reply_markup=aa)
        dichashtag["iddelete"] = dichashtag["iddelete"] + 1
        with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
            json.dump(dichashtag, json_file)




async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    

    await update.callback_query.answer()

    await update.effective_message.edit_text(

        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."

    )

def main() -> None:
    global application


    


    application = Application.builder().token("1").read_timeout(20).get_updates_read_timeout(20).build()
    #application = telegram.ext.ApplicationBuilder().token("1").arbitrary_callback_data(True).build().proxy(
    #proxy_url).get_updates_proxy(proxy_url).persistence(persistence)


    conv_handler = ConversationHandler(

        entry_points=[CommandHandler("start", startramz)],

        states={
            R: [MessageHandler(filters.Regex(f"{ramz}"), start)],
            AA: [MessageHandler(filters.Regex("برگشت به مرحله اول"), start)],
            A: [MessageHandler(filters.Regex("دریافت لینک کارت حساب📧"), linkhesab1),
                MessageHandler(filters.Regex("ذخیره شخص💾👤"), shakhs1),
                MessageHandler(filters.Regex('گزارشات📊'), gozareshat),
                MessageHandler(filters.Regex('آپدیت خدمات،کالاها،اشخاص،بانک ها🔄'), update),
                MessageHandler(filters.Regex(("^برگشت$")), start),
                MessageHandler(filters.Regex("ثبت کالا📦"), sabtkala1),
                MessageHandler(filters.Regex("^ثبت خدمات📋$"), sabtkhadamat1),
                MessageHandler(filters.Regex("^ثبت فاکتور🧾$"), sabtfactor1),
                MessageHandler(filters.Regex("^فاکتور سریع🧾$"), sabtfactor1),
                MessageHandler(filters.Regex("^عملیات هزینه💸$"), operation1),
                MessageHandler(filters.Regex("^عملیات انتقال💳$"), operation1),
                MessageHandler(filters.Regex("^عملیات پرداخت💳$"), operation1),
                MessageHandler(filters.Regex("^عملیات دریافت💰$"), operation1),
                MessageHandler(filters.Regex("^عملیات حواله💳$"), operation1),
                MessageHandler(filters.Regex("^عملیات رمز🔒$"), ramz1),
                MessageHandler(filters.Regex("^🗑️حذف اسناد$"), hazf1),
                MessageHandler(filters.Regex("^اپراتورها🙋‍♂️🙋‍♀️$"), operator1), ],
            HAZF1: [MessageHandler(filters.Regex(("^برگشت$")), start),
                    MessageHandler(filters.Regex("^" + "|".join(receipt_optionssari) + "$"), hazf2),
                    MessageHandler(filters.Regex("^" + "|".join(receipt_options) + "$"), hazf21)],
            HAZF22: [MessageHandler(filters.Regex(("^برگشت$")), start),
                     MessageHandler(filtermablagh, hazf31)],
            HAZF3: [MessageHandler(filters.Regex(("^برگشت$")), start),
                    MessageHandler(filters.Regex(("^لغو$")), start),
                    MessageHandler(filters.Regex(("^تایید$")), hazf4), ],
            HAZF2: [MessageHandler(filters.Regex(("^برگشت$")), start),
                    MessageHandler(filtermablagh, hazf3)],
            B: [CallbackQueryHandler(op2inline_jcalendar_handler),
                MessageHandler(filters.Regex(("^برگشت$")), start), ],
            C: [MessageHandler(filtermablagh, op3mablagh),
                MessageHandler(filters.Regex(("^برگشت$")), start), ],
            D: [InlineQueryHandler(op3mablaghinline),
                MessageHandler(filterbank, op4bank),
                MessageHandler(filters.Regex(("^برگشت$")), start), ],
            HAA: [InlineQueryHandler(havale1inline),
                  MessageHandler(filtercontacts, havale1),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            HAB: [InlineQueryHandler(havale2inline),
                  MessageHandler(filtercontacts, havale2),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            HAZA: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), hazine1),
                   MessageHandler(filters.Regex("^برگشت$"), start), ],
            E: [InlineQueryHandler(daryaftpardakht11inline),
                MessageHandler(filtercontacts, daryaftpardakht1),
                MessageHandler(filters.Regex(("^برگشت$")), start), ],
            ENA: [InlineQueryHandler(enteghal1inline),
                  MessageHandler(filterbank, enteghal1),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            F: [MessageHandler(
                telegram.ext.filters.PHOTO | filters.Regex(("^0000$")) | filters.Regex(("عکس رسید فوق را ندارم")),
                op5aks), MessageHandler(filters.Regex(("^برگشت$")), start), ],
            G: [MessageHandler(filtersaatpeigiri, op6peigiri),
                MessageHandler(filters.Regex(("^برگشت$")), start), ],
            H: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$|^لغو$|^تایید$"), op7tozihat),
                MessageHandler(filters.Regex(("^تایید$")), op8sabt),
                MessageHandler(filters.Regex(("^لغو$")), start),
                MessageHandler(filters.Regex("^برگشت$"), start), ],
            I: [MessageHandler(filters.Regex(("^تایید$")), op8sabt),
                MessageHandler(filters.Regex(("^لغو$")), start),
                MessageHandler(filters.Regex("^برگشت$"), start), ],
            FA: [MessageHandler(filters.Regex(re.compile(r"^(خرید|فروش)$|^(?!برگشت$).*$")), sabtfactor2),
                 MessageHandler(filters.Regex("^برگشت$"), start), ],
            FB: [MessageHandler(filtercontacts, sabtfactor3),
                 MessageHandler(filters.Regex(("^برگشت$")), start), ],
            FCM: [CallbackQueryHandler(sabtfactor31),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            FC: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), sabtfactor4),
                 MessageHandler(filters.Regex(("^برگشت$")), start), ],
            FSA: [CallbackQueryHandler(sabtfactorsari1),
                  MessageHandler(filters.Regex(("^برگشت$")), start),

                  ],
            FSB: [CallbackQueryHandler(sabtfactorsari2),
                  MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), sabtfactorsari2),
                  MessageHandler(filters.Regex(("^برگشت$")), start),

                  ],
            FSC: [
                MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), sabtfactorsari3),
                MessageHandler(filters.Regex(("^برگشت$")), start),
            ],
            FSD: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), sabtfactorsari4),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            FSE: [MessageHandler(filters.Regex(("^تایید$")), sabtfactorsari5),
                  MessageHandler(filters.Regex(("^لغو$")), start),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            FD: [
                InlineQueryHandler(sabtfactor4inline),
                 MessageHandler(filters.Regex(regex_patternkalakhadamatlist)& ~filters.Regex("^برگشت$") , sabtfactor5),
                 CallbackQueryHandler(sabtfactor5, pattern=regex_patternkalakhadamatlist),
                 MessageHandler(filters.Regex(("^برگشت$")), start),
            ],
            FE: [MessageHandler(filter_factor, sabtfactor6),
                 MessageHandler(filters.Regex(("^برگشت$")), start), ],
            FF: [MessageHandler(filters.Regex("^افزودن کالا یا خدمات$"), sabtfactor7),
                 MessageHandler(filters.Regex(("^ثبت فاکتور$")), sabtfactor8),
                 MessageHandler(filters.Regex(("^برگشت$")), start), ],
            O: [MessageHandler(filters.Regex(("^برگشت$")), start),
                MessageHandler(filters.Regex(("^حذف اپراتور🚫👤$")), operator5),
                MessageHandler(filters.Regex(("^مشاهده اپراتورهای فعلی👨‍👩‍👧‍👦$")), operator4),
                MessageHandler(filters.Regex(("^ایجاد اپراتور⚡️👤$")), operator2),
                ],
            OA: [MessageHandler(filters.Regex(("^برگشت$")), start),
                 MessageHandler(filters.Regex(regexpatternoperator), operator3), ],
            OB: [MessageHandler(filters.Regex(("^برگشت$")), start),
                 MessageHandler(filters.TEXT, operator6), ],
            RA: [MessageHandler(filters.Regex("^رمز فعلی🔐$"), ramz2),
                 MessageHandler(filters.Regex("^تغییر رمز🔒🔄$"), ramz3),
                 MessageHandler(filters.Regex(("^برگشت$")), start), ],
            RB: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), ramz4),
                 MessageHandler(filters.Regex(("^برگشت$")), start)],

            KA: [MessageHandler(filters.Regex(re.compile("^(?!برگشت$).*$")), sabtkala2),
                 MessageHandler(filters.Regex("^برگشت$"), start), ],

            KHA: [MessageHandler(filters.Regex(re.compile("^(?!برگشت$).*$")), sabtkhadamat2),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            KB: [InlineQueryHandler(sabtkala3inline),
                 CallbackQueryHandler(sabtkala3, pattern=regex_patternkalalist),
                 MessageHandler(filters.Regex(regex_patternkalalist), sabtkala3),
                 MessageHandler(filters.Regex("^برگشت$"), start), ],
            KHB: [MessageHandler(filters.Regex(r'^\d+$'), sabtkhadamat3),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            KC: [MessageHandler(filters.Regex(r'^\d+$'), sabtkala4),
                 MessageHandler(filters.Regex("^برگشت$"), start), ],
            KHC: [MessageHandler(filters.Regex(("^تایید$")), sabtkhadamat4),
                  MessageHandler(filters.Regex(("^لغو$")), start),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            KD: [MessageHandler(filters.Regex(("^تایید$")), sabtkala5),
                 MessageHandler(filters.Regex(("^لغو$")), start),
                 MessageHandler(filters.Regex("^برگشت$"), start), ],

            SHA: [MessageHandler(filters.TEXT & ~filters.Regex("^برگشت$"), shakhs2),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            SHB: [MessageHandler(filters.Regex(("^تایید$")), shakhs3),
                  MessageHandler(filters.Regex(("^لغو$")), start),
                  MessageHandler(filters.Regex("^برگشت$"), start), ],
            LHA: [MessageHandler(filtercontacts, linkhesab2),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            LHB: [MessageHandler(filters.Regex(regex_pattern5), linkhesab3),
                  MessageHandler(filters.Regex(("^برگشت$")), start), ],
            GOA: [CallbackQueryHandler(resid2, pattern=regex_patternresid),
                  MessageHandler(filters.Regex("^برگشت$"), start)],
            GOaA: [MessageHandler(filters.Regex("^گزارش بستانکار بدهکار$"), amaliat1),
                   MessageHandler(filters.Regex("^موجودی بانک ها$"), gozareshatbank),
                   MessageHandler(filters.Regex("^آخرین اسناد مالی$"), resid1),
                   MessageHandler(filters.Regex("^برگشت$"), start), ],
            GOBA: [MessageHandler(filters.Regex(r"^0$"), amaliat2),  # Only accept '0' for cancellation
                   CallbackQueryHandler(amaliat2),
                   MessageHandler(filters.Regex("^برگشت$"), start)],

            GOBB: [MessageHandler(filters.Regex(r"^0$"), amaliat3),  # Only accept '0' for cancellation
                   CallbackQueryHandler(amaliat3),
                   MessageHandler(filters.Regex("^برگشت$"), start)],
        },

        fallbacks=[CommandHandler("exit", start)],

        name="my_conversation",
        per_chat=False,
        # persistent=True,

    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(list_button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
#