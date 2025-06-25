from persiantools.jdatetime import JalaliDate
from persiantools import jdatetime
from telegram.ext.filters import MessageFilter
import re
import requests
import datetime
import os
import pickle
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
script_path = os.path.dirname(os.path.realpath(__file__))
script_patho=os.path.join(script_path, 'o')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Operationhahavale:
    def __init__(self, operationtype, apiKey, loginToken, dateTimejalali, dateTime, amount,
                 contactCode0, contactCode1, file_id, saat, peigiri, description, user_id, operator, chat_id,tarafhesab):
        self.operationtype = operationtype
        self.apiKey = apiKey
        self.loginToken = loginToken
        self.dateTimejalali = dateTimejalali
        self.dateTime = dateTime
        self.amount = amount
        self.contactCode0=contactCode0
        self.contactCode1=contactCode1
        self.file_id = file_id
        self.saat = saat
        self.peigiri = peigiri
        self.description = description
        self.user_id = user_id
        self.operator = operator
        self.chat_id = chat_id
        self.type1 ='ha'
        self.tarafhesab = tarafhesab
        self.firsttimehazf=False
        # Additional attributes
        self.ok = False
        self.path = None
        self.imagepath = None
        self.hashtag = None
        self.residhesabfa1 = None
        self.residhesabfa2=None
        self.residkoli = None
        self.banktaraz1 = None
        self.banktaraz2 = None
        self.jarimenumber = None
        self.jarimenumbershakhs=None
        current_date_time = datetime.datetime.now()
        date = current_date_time.strftime("%Y-%m-%dT%H:%M:%S")
        date_part, time_part = date.split('T')
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
        self.date = jalili_date
        self.time = time_part
    def post1(self):
        data1= {"apiKey": self.apiKey, "loginToken": self.loginToken, "type": 1,
             "dateTime": self.dateTime,
             'contactCode': self.contactCode0,
             'amount': self.amount,
             'bankCode': '7777',
             'description': self.description}

        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data1, headers=headers)
        return response
    def post2(self):
        data2 = {"apiKey": self.apiKey, "loginToken": self.loginToken, "type": 2,
             "dateTime": self.dateTime,
             'contactCode': self.contactCode1, 'amount': self.amount,
             'bankCode': '7777',
             'description': self.description}
        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data2, headers=headers)
        return response
    def jarime(self,Note):
        c = str(self.operator).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def jarimeshakhs(self,Note):
        c = str(self.contactCode0).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def hazf1(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf1 = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":1,"number":self.residhesabfa1}
        response = requests.post(url, json=datahazf1, headers=headers)

        return response
    def hazf2(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf2 = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":2,"number":self.residhesabfa2}
        response = requests.post(url, json=datahazf2, headers=headers)
        return response
class Operationenteghal:
    def __init__(self, operationtype, apiKey, loginToken, dateTimejalali, dateTime, amount,
                 bankCode0, bankCode1, file_id, saat, peigiri, description, user_id, operator, chat_id):
        self.operationtype = operationtype
        self.apiKey = apiKey
        self.loginToken = loginToken
        self.dateTimejalali = dateTimejalali
        self.dateTime = dateTime
        self.amount = amount
        self.bankCode0=bankCode0
        self.bankCode1=bankCode1
        self.file_id = file_id
        self.saat = saat
        self.peigiri = peigiri
        self.description = description
        self.user_id = user_id
        self.operator = operator
        self.chat_id = chat_id
        self.type1 ='e'
        self.firsttimehazf = False
        # Additional attributes
        self.ok = False
        self.path = None
        self.imagepath = None
        self.hashtag = None
        self.residhesabfa1 = None
        self.residhesabfa2=None
        self.residkoli = None
        self.banktaraz1 = None
        self.banktaraz2 = None
        self.jarimenumber = None
        current_date_time = datetime.datetime.now()
        date = current_date_time.strftime("%Y-%m-%dT%H:%M:%S")
        date_part, time_part = date.split('T')
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
        self.date = jalili_date
        self.time = time_part
    def post1(self):
        data1= {"apiKey": self.apiKey, "loginToken": self.loginToken, "type": 2,
             "dateTime": self.dateTime,
             'contactCode': '008800',
             'amount': self.amount,
             'bankCode': self.bankCode0,
             'description': self.description}

        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data1, headers=headers)
        return response
    def post2(self):
        data2 = {"apiKey": self.apiKey, "loginToken": self.loginToken, "type": 1,
             "dateTime": self.dateTime,
             'contactCode': '008800', 'amount': self.amount,
             'bankCode': self.bankCode1,
             'description': self.description}
        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data2, headers=headers)
        return response
    def jarime(self,Note):
        c = str(self.operator).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def hazf1(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf1 = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":2,"number":self.residhesabfa1}
        response = requests.post(url, json=datahazf1, headers=headers)
        return response
    def hazf2(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf2 = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":1,"number":self.residhesabfa2}
        response = requests.post(url, json=datahazf2, headers=headers)
        return response

class Operationdaryaft:
    def __init__(self, operationtype, apiKey, loginToken, type,  dateTimejalali, dateTime, amount,
                 bankCode,contactCode, file_id, saat, peigiri, description, user_id, operator, chat_id,type1,tarafhesab):
        self.operationtype = operationtype
        self.apiKey = apiKey
        self.loginToken = loginToken
        self.type = type
        self.dateTimejalali = dateTimejalali
        self.dateTime = dateTime
        self.amount = amount
        self.bankCode = bankCode
        self.contactCode = contactCode
        self.file_id = file_id
        self.saat = saat
        self.peigiri = peigiri
        self.description = description
        # Additional attributes
        self.user_id = user_id
        self.operator = operator
        self.chat_id = chat_id
        self.type1 = type1
        self.tarafhesab = tarafhesab
        self.firsttimehazf = False
        ########

        self.ok = False
        self.path = None
        self.imagepath = None
        self.hashtag = None
        self.residhesabfa = None
        self.residkoli = None
        self.banktaraz = None
        self.jarimenumber = None
        self.jarimenumbershakhs = None

        current_date_time = datetime.datetime.now()
        date = current_date_time.strftime("%Y-%m-%dT%H:%M:%S")
        date_part, time_part = date.split('T')
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
        self.date = jalili_date
        self.time = time_part
    def post(self):
        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        data = {"apiKey": self.apiKey, "loginToken": self.loginToken, "type": self.type,
                "contactCode": self.contactCode,
                "dateTime": self.dateTime, "amount": self.amount, "bankCode": self.bankCode,
                "description": self.description}
        response = requests.post(url, json=data, headers=headers)
        return response
    def jarime(self,Note):
        c = str(self.operator).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def jarimeshakhs(self,Note):
        c = str(self.contactCode).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def hazf(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":self.type,"number":self.residhesabfa}
        response = requests.post(url, json=datahazf, headers=headers)
        return response
class Operationhazine:
    def __init__(self, operationtype, apiKey, loginToken, type, contactCode, dateTimejalali, dateTime, amount,
                 bankCode, descriptionamaliat, file_id, saat, peigiri, description, user_id, operator, chat_id):
        self.operationtype = operationtype
        self.apiKey = apiKey
        self.loginToken = loginToken
        self.type = type
        self.contactCode = contactCode
        self.dateTimejalali = dateTimejalali
        self.dateTime = dateTime
        self.amount = amount
        self.bankCode = bankCode
        self.descriptionamaliat = descriptionamaliat
        self.file_id = file_id
        self.saat = saat
        self.peigiri = peigiri
        self.description = description
        # Additional attributes
        self.user_id = user_id
        self.operator = operator
        self.chat_id = chat_id
        self.firsttimehazf = False


########
        self.type1='h'
        self.ok = False
        self.path=None
        self.imagepath=None
        self.hashtag=None
        self.residhesabfa=None
        self.residkoli=None
        self.banktaraz=None
        self.jarimenumber=None
        current_date_time = datetime.datetime.now()
        date = current_date_time.strftime("%Y-%m-%dT%H:%M:%S")
        date_part, time_part = date.split('T')
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
        self.date=jalili_date
        self.time=time_part
    def post(self):
        url = 'https://api.hesabfa.com/v1/receipt/save'
        headers = {'Content-Type': 'application/json'}
        data={"apiKey": self.apiKey, "loginToken": self.loginToken, "type": self.type, "contactCode": self.contactCode,
              "dateTime":self.dateTime , "amount":self.amount,"bankCode":self.bankCode,"description":self.description}
        response = requests.post(url, json=data, headers=headers)
        return response
    def jarime(self,Note):
        c = str(self.operator).zfill(6)
        url = 'https://api.hesabfa.com/v1/invoice/save'
        headers = {'Content-Type': 'application/json'}
        datainvoice = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                "invoice": {"InvoiceType": 0,"contactCode": c ,"Note": Note,
                            "Status": 1,"DueDate": self.dateTime ,"Date": self.dateTime ,
                            "InvoiceItems": [{
                                "Description": 'تاخیر در ارسال رسید', "Quantity": 1, "UnitPrice": 1000000, "Discount": 0,
                                "Tax": 0,"ItemCode": '001062'}],}}
        response = requests.post(url, json=datainvoice, headers=headers)
        return response
    def hazf(self):
        url="https://api.hesabfa.com/v1/receipt/delete"
        headers = {'Content-Type': 'application/json'}
        datahazf = {"apiKey": self.apiKey, "loginToken": self.loginToken,
                       "type":self.type,"number":self.residhesabfa}
        response = requests.post(url, json=datahazf, headers=headers)
        return response
#wa
class CleanedDigitsFilter(MessageFilter):
    def __init__(self, pattern):
        self.pattern = pattern
    def filter(self, message):
        
        if message.text:
            
            cleaned_input = ''.join(filter(str.isdigit, message.text))
            
            return bool(re.match(self.pattern, cleaned_input))
        return False


class FactorFilter(MessageFilter):
    def __init__(self, pattern):
        
        self.pattern = pattern

    def filter(self, message):
        if message.text:
            
            pattern = r'[.,\-:_]'
            parts = re.split(pattern, message.text)

            
            if len(parts) >= 2:
                
                cleaned_input1 = ''.join(filter(str.isdigit, parts[0]))
                cleaned_input2 = ''.join(filter(str.isdigit, parts[1]))
                cleaned_input3 = parts[2] if len(parts) > 2 else '' 
                cleaned_input = f"{cleaned_input1}{cleaned_input2}{cleaned_input3}"

                
                return bool(re.match(self.pattern, cleaned_input))

        return False
def datetaiid():
    current_date_time = datetime.datetime.now()
    date = current_date_time.strftime("%Y-%m-%dT%H:%M:%S")
    date_part, time_part = date.split('T')
    parsed_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    a="📅"+ "تاریخ تایید: " +f"{jalili_date}"+"\n"+"🕒"+"زمان تایید: "+f"{time_part}"+"\n\n"
    return a
def convert_to_gregorian(persian_date):
    year, month, day = map(int, persian_date.split('-'))
    jalali_date = JalaliDate(int(year), int(month), int(day))
    gregorian_date = jalali_date.to_gregorian()
    formatted_result = gregorian_date.strftime("%Y-%m-%dT%H:%M:%S")
    return formatted_result
def delete_key_safely(key, user_data):
    if key in user_data:
        del user_data[key]
    else:
        print(f"Key '{key}' does not exist in user_data.")

def operationfill(state,operation,first=None,second=None):
    if state==1:
        if operation['operationtype']=='عملیات هزینه💸':
            operation['type']=2
            operation['contactCode']= '009900'
            reply=operationstr(state,operation)
        elif operation['operationtype']=='عملیات دریافت💰':
            operation['type'] = 1
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات پرداخت💳':
            operation['type'] = 2
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = operationstr(state, operation)
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = operationstr(state, operation)
        return reply,operation
    elif state==2:
        operation['dateTime']=convert_to_gregorian(operation['dateTimejalali'])
        reply=operationstr(state,operation)
        return reply,operation
    elif state==3:
        reply=operationstr(state,operation)
        return reply,operation
    elif state==4:
        if operation['operationtype']=='عملیات هزینه💸':
            operation['bankCode']=first
            reply=operationstr(state,operation,second)
        elif operation['operationtype']=='عملیات دریافت💰':
            operation['bankCode'] = first
            reply = operationstr(state, operation,second)
        elif operation['operationtype']=='عملیات پرداخت💳':
            operation['bankCode'] = first
            reply = operationstr(state, operation,second)
        elif operation['operationtype']=='عملیات انتقال💳':
            operation['bankCode0']=first
            reply = operationstr(state, operation,second)
        elif operation['operationtype'] == 'عملیات حواله💳':
            operation['contactCode0'] = first
            reply = operationstr(state, operation, second)
        return reply,operation
    elif state==5:
        if operation['operationtype']=='عملیات هزینه💸':
            reply=operationstr(state,operation)
        elif operation['operationtype']=='عملیات دریافت💰':
            operation['contactCode']=first
            reply = operationstr(state, operation, second)
        elif operation['operationtype']=='عملیات پرداخت💳':
            operation['contactCode'] = first
            reply = operationstr(state, operation,second)
        elif operation['operationtype']=='عملیات انتقال💳':
            operation['bankCode1'] = first
            reply = operationstr(state, operation,second)
        elif operation['operationtype'] == 'عملیات حواله💳':
            operation['contactCode1'] = first
            reply = operationstr(state, operation, second)

        return reply,operation
    elif state==6:
        if operation['operationtype']=='عملیات هزینه💸':
            reply=operationstr(state,operation)
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = operationstr(state, operation)
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = operationstr(state, operation)
        return reply,operation
    elif state==7:
        if operation['operationtype']=='عملیات هزینه💸':
            reply=operationstr(state,operation)
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = operationstr(state, operation)
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = operationstr(state, operation)
        return reply,operation
    elif state==8:
        if operation['operationtype']=='عملیات هزینه💸':
            reply=operationstr(state,operation)
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = operationstr(state, operation)
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = operationstr(state, operation)
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = operationstr(state, operation)
        return reply,operation
def operationstr(state,operation,first=None):
    if state==1:
        if operation['operationtype']=='عملیات هزینه💸':
            reply="🔴"+"نوع عملیات : هزینه "+"\n\n"
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = "🟢" + "نوع عملیات : دریافت "+"\n\n"
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = "🔴" + "نوع عملیات : پرداخت "+"\n\n"
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = "🔴" + "نوع عملیات : انتقال " + "\n\n"
        elif operation['operationtype']=='عملیات حواله💳':
            reply = "🔴" + "نوع عملیات : حواله " + "\n\n"
        return reply
    elif state==2:
        if operation['operationtype']=='عملیات هزینه💸':
            reply="🔴"+"نوع عملیات : هزینه "+"\n\n"
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = "🟢" + "نوع عملیات : دریافت "+"\n\n"
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = "🔴" + "نوع عملیات : پرداخت "+"\n\n"
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = "🔴" + "نوع عملیات : انتقال " + "\n\n"
        elif operation['operationtype']=='عملیات حواله💳':
            reply = "🔴" + "نوع عملیات : حواله " + "\n\n"
        reply+="📅تاریخ :"+f"{operation['dateTimejalali']}"+"\n\n"

        return reply
    elif state==3:
        amount = int(operation['amount'])
        formatted_amount = "{:,}".format(amount)
        if operation['operationtype']=='عملیات هزینه💸':
            reply="🔴"+"نوع عملیات : هزینه "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply+="کد بانک را وارد نمایید."
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = "🟢" + "نوع عملیات : دریافت "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "کد بانک را وارد نمایید."
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = "🔴" + "نوع عملیات : پرداخت "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "کد بانک را وارد نمایید."
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = "🔴" + "نوع عملیات : انتقال " + "\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "کد بانک مبداء را وارد نمایید."
        elif operation['operationtype']=='عملیات حواله💳':
            reply = "🔴" + "نوع عملیات : حواله " + "\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "👤کد شخص فرستنده را وارد نمایید."
        return reply
    elif state==4:
        amount = int(operation['amount'])
        formatted_amount = "{:,}".format(amount)
        if operation['operationtype']=='عملیات هزینه💸':
            reply="🔴"+"نوع عملیات : هزینه "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply+="🏦بانک: "+f"{first}"+"\n\n"
            reply+="❇️نوع عملیات هزینه را وارد کنید. برای عملیات هزینه خالی صفر را وارد کنید."
        elif operation['operationtype']=='عملیات دریافت💰':
            reply = "🟢" + "نوع عملیات : دریافت "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "🏦بانک: " + f"{first}" + "\n\n"
            reply += "👤کد طرف حساب را وارد نمایید."
        elif operation['operationtype']=='عملیات پرداخت💳':
            reply = "🔴" + "نوع عملیات : پرداخت "+"\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "🏦بانک: " + f"{first}" + "\n\n"
            reply+="👤کد طرف حساب را وارد نمایید."
        elif operation['operationtype']=='عملیات انتقال💳':
            reply = "🔴" + "نوع عملیات : انتقال " + "\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "🏦بانک مبداء: " + f"{first}" + "\n\n"
            reply +='❇️کد بانک مقصد را وارد نمایید.'
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = "🔴" + "نوع عملیات : حواله " + "\n\n"
            reply += "📅تاریخ :" + f"{operation['dateTimejalali']}" + "\n\n"
            reply += "💰مبلغ : " + f"{formatted_amount}" + " ریال" + "\n\n"
            reply += "👤شخص فرستنده: " + f"{first}" + "\n\n"
            reply += "کد شخص گیرنده را وارد نمایید."

        return reply
    elif state == 5:
        if operation['operationtype'] == 'عملیات هزینه💸':
            reply=operation['reply_text']+"\n\n"
            reply += "❇️نوع عملیات هزینه:"+f"{operation['descriptionamaliat']}"+"\n\n"
            reply+="حال تصویر رسید را بفرستید و یا دقیقاً تایپ کنید (عکس رسید فوق را ندارم)."
        elif operation['operationtype'] == 'عملیات دریافت💰':
            reply = operation['reply_text']+"\n\n"
            reply +="👤نام طرف حساب: "+f"{first}"+"\n\n"
            reply += "حال تصویر رسید را بفرستید و یا دقیقاً تایپ کنید (عکس رسید فوق را ندارم)."
        elif operation['operationtype'] == 'عملیات پرداخت💳':
            reply = operation['reply_text']+"\n\n"
            reply += "👤نام طرف حساب: " + f"{first}" + "\n\n"
            reply += "حال تصویر رسید را بفرستید و یا دقیقاً تایپ کنید (عکس رسید فوق را ندارم)."
        elif operation['operationtype'] == 'عملیات انتقال💳':
            reply = operation['reply_text'] + "\n\n"
            reply+="🏦بانک مقصد: "+f"{first}"+"\n\n"
            reply += "حال تصویر رسید را بفرستید و یا دقیقاً تایپ کنید (عکس رسید فوق را ندارم)."
        elif operation['operationtype'] == 'عملیات حواله💳':
            reply = operation['reply_text'] + "\n\n"
            reply += "👤 شخص گیرنده: " + f"{first}" + "\n\n"
            reply += "حال تصویر رسید را بفرستید و یا دقیقاً تایپ کنید (عکس رسید فوق را ندارم)."
        return reply
    elif state == 6:
        if operation['file_id'] == '0':
            reply=operation['reply_text']+"\n\n"
            reply+="📷عکس : ندارد"+"\n\n"
            reply+="حال لطفا ساعت و شماره پیگیری را وارد کنید. دقت فرمایید ساعت و شماره پیگیری کاراکتر عددی است و حداقل باید شامل 4 کاراکتر عددی باشد.ساعت-شماره پیگیری"
        else:
            reply = operation['reply_text'] + "\n\n"
            reply += "📷عکس : دارد" + "\n\n"
            reply += "حال لطفا ساعت و شماره پیگیری را وارد کنید. دقت فرمایید ساعت و شماره پیگیری کاراکتر عددی است و حداقل باید شامل 4 کاراکتر عددی باشد.ساعت-شماره پیگیری"

        return reply
    elif state == 7:
            reply=operation['reply_text']+"\n\n"
            reply+="🕒ساعت : "+f"{operation['saat']}"+"\n\n"
            reply+="📃" + "شناسه پیگیری: " +f"{operation['peigiri']}"+"\n\n"
            reply+="📝"+"توضیحات ثبت: "+f"{operation['description']}"+"\n\n"
            reply+="❇️سند فوق به شکل بالا در حال ثبت می باشد." + "در صورت نیاز به توضیحات ، توضیحات مدنظر را تایپ کنید. در غیر اینصورت تایید یا لغو را بزنید." +""
            return reply
    elif state == 8:
            reply=operation['reply_text']+"\n\n"
            reply+="📝"+"توضیحات ثبت جدید: "+f"{operation['description']}"+"\n\n"
            reply+="❇️سند فوق به شکل بالا در حال ثبت می باشد." + "در صورت نیاز به توضیحات ، توضیحات مدنظر را تایپ کنید. در غیر اینصورت تایید یا لغو را بزنید." +""
            return reply


def parse_status_and_note(input_string):
    
    for index, char in enumerate(input_string):
        if char.isdigit():
            
            status = int(char)
            
            note = input_string[index + 1:]
            return status, note

    
    return None, "No digit found in the input string"

def get_bank_info(apiKey, loginToken, code=None, all_info=False):
    url = 'https://api.hesabfa.com/v1/report/trialbalanceitems'
    data = {
        "apiKey": apiKey,
        "loginToken": loginToken,
        "accountPath": "دارایی ها : دارایی های جاری : موجودی نقد و بانک : بانک"}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if result.get("Success"):
            banks = result.get("Result")
            if code:
                for bank in banks:
                    if bank['Code'] == code:
                        if bank['BalanceType'] == 0:
                            amount = "{:,}".format(int(bank['Balance']))
                            return bank['Name'], str(amount)
                        elif bank['BalanceType'] == 1:
                            amount = "{:,}".format(int(bank['Balance']))
                            return bank['Name'], 'منفی'+" " + str(amount) +'-'
            elif all_info:
                bank_info = []
                for bank in banks:
                    if bank['Balance'] > 0 and bank['BalanceType'] == 0:
                        bank_info.append((bank['Name'], bank['Balance'], bank['Code']))
                bank_info.sort(key=lambda x: x[1], reverse=True)
                return bank_info
            else:
                return "Please provide a bank code or set all_info to True."
        else:
            return "Request failed. Success is not true."
    else:
        return f"Request failed with status code: {response.status_code}, Response content: {response.content.decode('utf-8')}"
def get_kala_list(apiKey, loginToken):
    urlkalalist = 'https://api.hesabfa.com/v1/setting/GetProductCategories'
    headers = {'Content-Type': 'application/json'}
    datakalalist = {"apiKey": apiKey, "loginToken": loginToken}
    print('get_kala_list0')
    response = requests.post(urlkalalist, json=datakalalist, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print('get_kala_list1')
        if result.get("Success"):
            r = result.get("Result")
            namekalalist = [item['Name'] for item in r['Root']['Children']]
            code_name_mappingkala = {item['Name']: item['FullPath'] for item in r['Root']['Children']}
            return namekalalist, code_name_mappingkala
        else:
            print("Request failed. Success is not true.")
            return None, None
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))
        return None, None
def get_kalakhadamat_list(apiKey, loginToken):
    urlkalakhadamatlist = 'https://api.hesabfa.com/v1/item/getitems'
    data = {
        "apiKey": apiKey,
        "loginToken": loginToken,
        "queryInfo": {
            "SortBy": 'NodeId',
            "SortDesc": True,
            "Take": 1000,
            "Skip": 0,
            "Filters": [{
                "Property": 'Active',
                "Operator": '=',
                "Value": 'True'
            }]
        }
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(urlkalakhadamatlist, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()

        if result.get("Success"):
            r = result.get("Result")
            codeskalakhadamatlist = [item['Code'] for item in r['List']]
            code_name_mappingkalakhadamatlist = {item['Name']: item['Code'] for item in r['List']}
            names = list(code_name_mappingkalakhadamatlist.keys())
            reply_keyboardkalakhadamatlist = [names[i:i + 4] for i in range(0, len(names), 4)]

            return codeskalakhadamatlist, code_name_mappingkalakhadamatlist, reply_keyboardkalakhadamatlist
        else:
            print("Request failed. Success is not true.")
            return None, None, None
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))
        return None, None, None
def get_contacts(apiKey, loginToken):
    urlcontacts = 'https://api.hesabfa.com/v1/contact/getcontacts'
    headers = {'Content-Type': 'application/json'}
    datacontacts = {
        "apiKey": apiKey,
        "loginToken": loginToken,
        "queryInfo": {
            "SortBy": 'Code',
            "SortDesc": True,
            "Take": 2000,
            "Skip": 0,
        }
    }

    response = requests.post(urlcontacts, json=datacontacts, headers=headers)

    if response.status_code == 200:
        result = response.json()

        if result.get("Success"):
            r = result.get("Result")
            codescontacts = [item['Code'] for item in r['List']]
            code_name_mapping = {item['Code']: item['Name'] for item in r['List']}
            return codescontacts, code_name_mapping
        else:
            print("Request failed. Success is not true.")
            return None, None
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))
        return None, None
def get_bank_list(apiKey, loginToken):
    urlbanks = "https://api.hesabfa.com/v1/setting/GetBanks"
    headers = {'Content-Type': 'application/json'}
    databanks = {
        "apiKey": apiKey,
        "loginToken": loginToken,
        "queryInfo": {
            "SortBy": 'Code',
            "SortDesc": True,
            "Take": 1000,
            "Skip": 0,
        }
    }

    response = requests.post(urlbanks, json=databanks, headers=headers)

    if response.status_code == 200:
        result = response.json()

        if result.get("Success"):
            r = result.get("Result")
            bankcodes = [item['Code'] for item in r]
            code_name_mappingbanks = {item['Code']: item['Name'] for item in r}
            return bankcodes, code_name_mappingbanks
        else:
            print("Request failed. Success is not true.")
            return None, None
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))
        return None, None
def convert_to_persian_calendarasnad(gregorian_datetime):
    
    jalali_datetime = JalaliDateTime.strptime(gregorian_datetime, "%Y-%m-%dT%H:%M:%S")
    parsed_date = datetime.datetime.strptime(gregorian_datetime, "%Y-%m-%dT%H:%M:%S")
    persian_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    persian_time = jalali_datetime.strftime("%H:%M:%S")

    return persian_date, persian_time
def get_api_datadp(apiKey,loginToken,number,type):
    data = {"apiKey": apiKey, "loginToken": loginToken, "type": int(type),"number":int(number)
            }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.hesabfa.com/v1/receipt/get', json=data, headers=headers)
    if response.status_code == 200:

        result = response.json()

        if result.get("Success"):
            result=result.get("Result")
            if type==1:
                persian_date, persian_time = convert_to_persian_calendarasnad(result['DateTime'])
                formatted_amount = "{:,}".format(int(result['Amount']))
                text = "🗒" + "شماره رسید دریافت: " + f" {result['Number']}" + "\n\n"
                text += "📅" + "تاریخ رسید دریافت: " + f" {persian_date}" + "\n\n"
                text += "💰" + "مبلغ رسید: " + f"{formatted_amount}" + " ریال" + "\n\n"
                if result['Items'][0]['Contact']['Code']:
                    text +="👤"+"کد طرف حساب: "+f"{result['Items'][0]['Contact']['Code']}"+"\n"
                    text +="👤"+"نام طرف حساب: "+f"{result['Items'][0]['Contact']['Name']}"+"\n\n"
                if result['Transactions'][0]['Bank']['Code']:
                    text+="🏦"+"کد بانک: "+f"{result['Transactions'][0]['Bank']['Code']}"+"\n"
                    text += "🏦" + "نام بانک: " + f"{result['Transactions'][0]['Bank']['Name']}" + "\n\n"
                text += "📝" + "توضیحات رسید: " + f"{result['Description']}" + "\n\n"
                return text
            if type==2:
                persian_date, persian_time = convert_to_persian_calendarasnad(result['DateTime'])
                formatted_amount = "{:,}".format(int(result['Amount']))
                text = "🗒" + "شماره رسید پرداخت: " + f" {result['Number']}" + "\n\n"
                text += "📅" + "تاریخ رسید پرداخت: " + f" {persian_date}" + "\n\n"
                text += "💰" + "مبلغ رسید: " + f"{formatted_amount}" + " ریال" + "\n\n"
                if result['Items'][0]['Contact']['Code']:
                    text += "👤" + "کد طرف حساب: " + f"{result['Items'][0]['Contact']['Code']}" + "\n"
                    text += "👤" + "نام طرف حساب: " + f"{result['Items'][0]['Contact']['Name']}" + "\n\n"
                if result['Transactions'][0]['Bank']['Code']:
                    text += "🏦" + "کد بانک: " + f"{result['Transactions'][0]['Bank']['Code']}" + "\n"
                    text += "🏦" + "نام بانک: " + f"{result['Transactions'][0]['Bank']['Name']}" + "\n\n"
                text += "📝" + "توضیحات رسید: " + f"{result['Description']}" + "\n\n"
                return text
        else:
            pass
    else:
        pass
    return None

def get_api_datafactor(apiKey,loginToken,number,type):
    data = {"apiKey": apiKey, "loginToken": loginToken, "type": int(type),"number":int(number)
            }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.hesabfa.com/v1/invoice/get', json=data, headers=headers)
    if response.status_code == 200:

        result = response.json()

        if result.get("Success"):
            result=result.get("Result")
            if type==0:
                persian_date, persian_time = convert_to_persian_calendarasnad(result['Date'])
                formatted_amount = "{:,}".format(int(result['Sum']))
                text = "🗒" + "شماره فاکتور فروش: " + f" {result['Number']}" + "\n\n"
                text += "📅" + "تاریخ فاکتور فروش: " + f" {persian_date}" + "\n\n"
                text += "👤" + "کد شخص : " + f"{result['ContactCode']}" + "\n\n"
                text+="🔽🔽🔽🔽"+"اقلام فاکتور:"+"\n\n"
                for item in result['InvoiceItems']:
                    text+="🔢"+"ردیف: "+f"{item['RowNumber']}"+"--"+"تعداد:"+f"{item['Quantity']}"+"\n"
                    text+= "🏷️"+"نام کالا: "+f"{item['Description']}"+"\n"
                    text+="💲"+"قیمت واحد: "+f"{item['UnitPrice']:,}"+"ریال"+"\n"
                    text+="📊"+"جمع ردیف: "+f"{item['Sum']}"+"\n\n"

                text +="\n"+ "🔢➕💵" + "جمع مبلغ اقلام : " + f"{formatted_amount}" + " ریال" + "\n\n"

                return text
            if type==1:
                persian_date, persian_time = convert_to_persian_calendarasnad(result['Date'])
                formatted_amount = "{:,}".format(int(result['Sum']))
                text = "🗒" + "شماره فاکتور خرید: " + f" {result['Number']}" + "\n\n"
                text += "📅" + "تاریخ فاکتور خرید: " + f" {persian_date}" + "\n\n"
                text += "👤" + "کد شخص : " + f"{result['ContactCode']}" + "\n\n"
                text += "🔽🔽🔽🔽" + "اقلام فاکتور:" + "\n\n"
                for item in result['InvoiceItems']:
                    text += "🔢" + "ردیف: " + f"{item['RowNumber']}" + "--" + "تعداد:" + f"{item['Quantity']}" + "\n"
                    text += "🏷️" + "نام کالا: " + f"{item['Description']}" + "\n"
                    text += "💲" + "قیمت واحد: " + f"{item['UnitPrice']:,}" + "ریال" + "\n"
                    text += "📊" + "جمع ردیف: " + f"{item['Sum']}" + "\n\n"

                text += "\n" + "🔢➕💵" + "جمع مبلغ اقلام : " + f"{formatted_amount}" + " ریال" + "\n\n"

                return text
        else:
            pass
    else:
        pass
    return None

def invoicesaristr(products,quantity=None):
    reply=""
    i=1
    if products:
        for product in products:
            reply+="کالا ردیف "+f"{i}:" +f"{product}"+"\n"
            i+=1
    if quantity:
        reply=""

    return reply
def format_invoice(invoice):
    products = invoice['selected_products']
    quantities = invoice['quantities']
    prices = invoice['prices']

    
    header = f"{'محصول':<15} | {'تعداد':<10} | {'قیمت واحد':<12} | {'قیمت کل':<12}"
    separator = '-' * len(header)

   
    rows = [header, separator]
    for product in products:
        quantity = quantities.get(product, 0)
        price = prices.get(product, 0.0)
        total = quantity * price
        
        rows.append(f"{product:<15} | {quantity:<10} | {price:<12.2f} | {total:<12.2f}")

    
    return "```\n" + "\n".join(rows) + "\n```"


def create_invoice_image(invoice):
    try:
        
        font = ImageFont.truetype("FontsFree-Net-Vazir-Regular.ttf", 20)
    except IOError:
        
        font = ImageFont.load_default()

    
    num_items = len(invoice['selected_products'])
    additional_info_lines = 3  
    img_height = 50 + num_items * 30 + additional_info_lines * 50

    img = Image.new('RGB', (800, img_height), 'white')
    d = ImageDraw.Draw(img)

    y = 10


    details_text = [
        f"کد شخص: {invoice.get('contactCode', '')}",
        f"عنوان شخص: {invoice.get('ContactTitle', '')}",
        f"تاریخ : {invoice.get('Jalali', '')}"
    ]
    for detail in details_text:
        reshaped_text = arabic_reshaper.reshape(detail)
        bidi_text = get_display(reshaped_text)  
        d.text((10, y), reshaped_text , fill="black", font=font)
        y += 30


    headers = ['محصول', 'تعداد', 'قیمت واحد', 'قیمت کل']
    x_positions = [10, 250, 400, 600] 
    
    y += 20  
    for idx, header in enumerate(headers):
        reshaped_text = arabic_reshaper.reshape(header) 
        bidi_text = get_display(reshaped_text)
        d.text((x_positions[idx], y), reshaped_text, fill="black", font=font)
    y += 30

    
    for product in invoice['selected_products']:
        quantity = invoice['quantities'][product]
        price = invoice['prices'][product]
        total = quantity * price
        details = [product, str(quantity), f"{(int(price)):,}", f"{(int(total)):,}"]

        for idx, detail in enumerate(details):
            reshaped_text = arabic_reshaper.reshape(detail)  
            bidi_text = get_display(reshaped_text)
            d.text((x_positions[idx], y), reshaped_text, fill="black", font=font)
        y += 30

   
    img.save('invoice.png')
def process_invoice_data(invoice,code_name_mappingkalakhadamatlist):
    
    products = invoice['selected_products']
    quantities = invoice['quantities']
    prices = invoice['prices']

    
    processed_products = []

    
    for product in products:
        
        quantity = quantities.get(product, 0)  
        price = prices.get(product, 0.0)  

        
        total_price = quantity * price
        desired_code = code_name_mappingkalakhadamatlist[product]
        
        processed_products.append({
            'Description': product,
            'Quantity': quantity,
            'UnitPrice': price,
            'Tax':0,
            'Discount':0,
            'ItemCode':desired_code,
        })

    return processed_products
