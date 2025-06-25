from persiantools.jdatetime import JalaliDate
import datetime
import asyncio
def hazinestr(operation, result):
    a = "🟠" + "نوع عملیات : هزینه "
    a+="\n"+f"#Revenue"+"\n\n"
    a += "🏦بانک: " + f"{code_name_mappingbanks.get(operation.bankCode)}" + "\n" + f"#BANK{operation.bankCode} " + "\n\n"
    a += "📃" + "شناسه پیگیری: " + "\n" + f"#Document{operation.peigiri}" + "\n\n"
    formatted_amount = "{:,}".format(int(operation.amount))
    a += "💰مبلغ: " + f"{formatted_amount}" + "  ریال" + "\n"
    a+="#Price"+f"{operation.amount}"+"\n\n"
    date_part, time_part = operation.dateTime.split('T')
    parsed_date = datetime.datetime.strptime(operation.dateTime, '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    jalili_date_str = str(jalili_date).replace("-", "")
    a += "📅تاریخ : " + f"{jalili_date}" + "\n"
    a+="#DATE"+f"{jalili_date_str}"+"\n\n"
    a += "🕒ساعت : " + f"{operation.saat}" + "\n" + "\n"
    a += "📝توضیحات: " + f"{operation.description}" + "\n\n"
    a += "📆تاریخ  ثبت درخواست:" + f" {operation.date}" + "\n"
    a += "⏰ساعت ثبت درخواست:" + f" {operation.time}" + "\n" + "\n"
    o = a
    if result:
        if result.get("Success"):
            o = a

            asyncio.sleep(2)
            name, balance = get_bank_info(apiKey, loginToken, code=operation.bankCode, all_info=False)
            a += "موجودی حساب ⬇️" + "\n" + f"{name}" + "\n\n" + "م:" + "✅" + f"{balance}" + "✅" + "\n" + "\n"
            a+=datetaiid()
            dichashtag["idhazine"] = dichashtag["idhazine"] + 1
            dichashtag["idkoli"] = dichashtag["idkoli"] + 1
            h = str(dichashtag["idhazine"]).zfill(6)
            operation.hashtag = dichashtag["idhazine"]
            operation.residhesabfa = result['Result']['Number']
            operation.residkoli = dichashtag["idkoli"]
            operation.banktaraz = balance
            a += f"#Acc{result['Result']['Number']}" + "\n" + f"#H{h}"
            if operation.jarimenumber:
                a += "\n" + f"#J{operation.jarimenumber}"
            save_data1(operation)
            with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                json.dump(dichashtag, json_file)
        else:
            a += "کد خطای حسابفا: " + f"{result['ErrorCode']}" + "\n\n"
            a += "پیام خطای حسابفا: " + f"{result['ErrorMessage']}" + "\n\n"
            o = a
    a = " 🔶 🔶 🔶 🔶 🔶 🔶 🔶  " + "\n\n" + "🛃اپراتور: " + f"#O{autorizedusers.get(str(operation.user_id))['code']}" + "\n\n" + a
    return a, o


def daryaftstr(operation, result):
    if operation.type == 2:
        a = "🟢" + "نوع عملیات: " + "پرداخت"
        a += "\n" + f"#Payment" + "\n\n"
    if operation.type == 1:
        a = "🟢" + "نوع عملیات: " + "دریافت"
        a += "\n" + f"#Receipt" + "\n\n"
    a += "👤طرف حساب: " + "\n" + f"#U{operation.contactCode}" + "\n" + "\n"
    a += "🏦بانک: " + f"{code_name_mappingbanks.get(operation.bankCode)}" + "\n" + f"#BANK{operation.bankCode}" + "\n" + "\n"
    if operation.type == 2:
        a += "📃" + "شناسه پیگیری: " + "\n" + f"#Document{operation.peigiri}" + "\n" + "\n"
    if operation.type == 1:
        a += "📃" + "شناسه پیگیری: " + "\n" + f"#Document{operation.peigiri}" + "\n" + "\n"
    formatted_amount = "{:,}".format(int(operation.amount))
    a += "💰مبلغ: " + f"{formatted_amount}" + "  ریال" + "\n"
    a += "#Price" + f"{operation.amount}" + "\n\n"
    date_part, time_part = operation.dateTime.split('T')
    parsed_date = datetime.datetime.strptime(operation.dateTime, '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    jalili_date_str = str(jalili_date).replace("-", "")
    a += "📅تاریخ : " + f"{jalili_date}" + "\n"
    a += "#DATE" + f"{jalili_date_str}" + "\n\n"
    a += "🕒ساعت : " + f"{operation.saat}" + "\n" + "\n"
    a += "📝توضیحات: " + f"{operation.description}" + "\n" + "\n"
    a += "📆تاریخ  ثبت درخواست:" + f" {operation.date}" + "\n"
    a += "⏰ساعت ثبت درخواست:" + f" {operation.time}" + "\n" + "\n"
    o = a
    if result:
        if result.get("Success"):
            if operation.type == 2:
                o = a
                asyncio.sleep(2)
                name, balance = get_bank_info(apiKey, loginToken, code=operation.bankCode, all_info=False)
                a += "موجودی حساب ⬇️" + "\n" + f"{name}" + "\n\n" + "م:" + "✅" + f"{balance}" + "✅" + "\n" + "\n"
                a += datetaiid()
                dichashtag["idpardakht"] = dichashtag["idpardakht"] + 1
                dichashtag["idkoli"] = dichashtag["idkoli"] + 1
                h = str(dichashtag["idpardakht"]).zfill(6)
                operation.hashtag = dichashtag["idpardakht"]
                operation.residhesabfa = result['Result']['Number']
                operation.residkoli = dichashtag["idkoli"]
                operation.banktaraz = balance
                a += f"#ACC{result['Result']['Number']}" + "\n" + f"#P{h}"
                if operation.jarimenumber:
                    a += "\n" + f"#J{operation.jarimenumber}"
                save_data1(operation)
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
            if operation.type == 1:
                o = a
                asyncio.sleep(2)
                name, balance = get_bank_info(apiKey, loginToken, code=operation.bankCode, all_info=False)
                a += "موجودی حساب ⬇️" + "\n" + f"{name}" + "\n\n" + "م:" + "✅" + f"{balance}" + "✅" + "\n" + "\n"
                a += datetaiid()
                dichashtag["iddaryaft"] = dichashtag["iddaryaft"] + 1
                dichashtag["idkoli"] = dichashtag["idkoli"] + 1
                h = str(dichashtag["iddaryaft"]).zfill(6)
                operation.hashtag = dichashtag["iddaryaft"]
                operation.residhesabfa = result['Result']['Number']
                operation.residkoli = dichashtag["idkoli"]
                operation.banktaraz = balance
                a += f"#Acc{result['Result']['Number']}" + "\n" + f"#D{h}"
                if operation.jarimenumber:
                    a += "\n" + f"#J{operation.jarimenumber}"
                save_data1(operation)
                with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                    json.dump(dichashtag, json_file)
        else:
            a += "کد خطای حسابفا: " + f"{result['ErrorCode']}" + "\n" + "\n"
            a += "پیام خطای حسابفا: " + f"{result['ErrorMessage']}" + "\n" + "\n"
            o = a
    if operation.type == 1:
        a = "🟩 🟩 🟩 🟩 🟩 🟩 🟩" + "\n\n" + "🛃اپراتور: " + f"#O{autorizedusers.get(str(operation.user_id))['code']}" + "\n\n" + a
    elif operation.type == 2:
        a = "♦️♦️♦️♦️♦️♦️♦️" + "\n\n" + "🛃اپراتور: " + f"#O{autorizedusers.get(str(operation.user_id))['code']}" + "\n" + "\n" + a
    return a, o


def enteghalstr(operation, result1, result2):
    a = "🔵" + "نوع عملیات : انتقال"
    a += "\n" + f"#Transfer" + "\n\n"
    a += "🏦 بانک مبداً: " + f"{code_name_mappingbanks.get(operation.bankCode0)}" + "\n" + f"#BANK{operation.bankCode0}" + "\n\n"
    a += "🏦 بانک مقصد: " + f"{code_name_mappingbanks.get(operation.bankCode1)}" + "\n" + f"#BANK{operation.bankCode1}" + "\n\n"
    a += "📃" + "شناسه پیگیری: " + "\n" + f"#Document{operation.peigiri}" + "\n\n"
    formatted_amount = "{:,}".format(int(operation.amount))
    a += "💰مبلغ: " + f"{formatted_amount}" + "  ریال" + "\n"
    a += "#Price" + f"{operation.amount}" + "\n\n"
    date_part, time_part = operation.dateTime.split('T')
    parsed_date = datetime.datetime.strptime(operation.dateTime, '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    jalili_date_str = str(jalili_date).replace("-", "")
    a += "📅تاریخ : " + f"{jalili_date}" + "\n"
    a += "#DATE" + f"{jalili_date_str}" + "\n\n"
    a += "🕒ساعت : " + f"{operation.saat}" + "\n" + "\n"
    a += "📝توضیحات: " + f"{operation.description}" + "\n" + "\n"
    a += "📆تاریخ  ثبت درخواست:" + f" {operation.date}" + "\n"
    a += "⏰ساعت ثبت درخواست:" + f" {operation.time}" + "\n" + "\n"
    o = a
    if result1:
        if result1.get("Success"):

            asyncio.sleep(1)
            name, balance = get_bank_info(apiKey, loginToken, code=operation.bankCode0, all_info=False)
            a += "موجودی حساب ⬇️" + "\n" + f"{name}" + "\n\n" + "م:" + "✅" + f"{balance}" + "✅" + "\n" + "\n"
            a += datetaiid()
            operation.residhesabfa1 = result1['Result']['Number']
            operation.banktaraz1 = balance

        else:
            a += "کد خطای مرحله اول حسابفا: " + f"{result1['ErrorCode']}" + "\n"
            a += "پیام خطای مرحله اول حسابفا: " + f"{result1['ErrorMessage']}" + "\n"
            o = a
    if result2:
        if result2.get("Success"):
            asyncio.sleep(1)
            name, balance = get_bank_info(apiKey, loginToken, code=operation.bankCode1, all_info=False)
            a += "موجودی حساب ⬇️" + "\n" + f"{name}" + "\n\n" + "م:" + "✅" + f"{balance}" + "✅" + "\n" + "\n"
            a += datetaiid()
            dichashtag["identeghal"] = dichashtag["identeghal"] + 1
            dichashtag["idkoli"] = dichashtag["idkoli"] + 1
            h = str(dichashtag["identeghal"]).zfill(6)
            operation.hashtag = dichashtag["identeghal"]
            operation.residhesabfa2 = result2['Result']['Number']
            operation.residkoli = dichashtag["idkoli"]
            operation.banktaraz2 = balance
            if result1['Result']['Number']:
                a += f"#ACC{result1['Result']['Number']}" + "\n"
            a += f" #ACC{result2['Result']['Number']}\n#E{h}  "
            if operation.jarimenumber:
                a += f"\n#J{operation.jarimenumber}"
            save_data1(operation)
            with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                json.dump(dichashtag, json_file)
        else:
            a += "کد خطای مرحله دوم حسابفا: " + f"{result2['ErrorCode']}" + "\n"
            a += "پیام خطای مرحله دوم حسابفا: " + f"{result2['ErrorMessage']}" + "\n"
            o = o + "کد خطای مرحله دوم حسابفا: " + f"{result2['ErrorCode']}" + "\n" + "پیام خطای مرحله دوم حسابفا: " + f"{result2['ErrorMessage']}" + "\n"
    a = "🔷️🔷️🔷️🔷️🔷️🔷️🔷️" + "\n\n" + "🛃اپراتور: " + f"#O{autorizedusers.get(str(operation.user_id))['code']}" + "\n\n" + a
    return a, o


def havalestr(operation, result1, result2):
    a = "🔵" + "نوع عملیات : حواله"
    a += "\n" + f"#Remittance" + "\n\n"
    a += "👤 شخص فرستنده:" + "\n" + f" #U{operation.contactCode0}" + "\n\n"
    a += "👤 شخص گیرنده:" + "\n" + f" #U{operation.contactCode1}" + "\n\n"
    a += "📃" + "شناسه پیگیری: " + "\n" + f"#Document{operation.peigiri}" + "\n\n"
    formatted_amount = "{:,}".format(int(operation.amount))
    a += "💰مبلغ: " + f"{formatted_amount}" + "  ریال" + "\n"
    a += "#Price" + f"{operation.amount}" + "\n\n"
    date_part, time_part = operation.dateTime.split('T')
    parsed_date = datetime.datetime.strptime(operation.dateTime, '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    jalili_date_str = str(jalili_date).replace("-", "")
    a += "📅تاریخ : " + f"{jalili_date}" + "\n"
    a += "#DATE" + f"{jalili_date_str}" + "\n\n"
    a += "🕒ساعت : " + f"{operation.saat}" + "\n" + "\n"
    a += "📝توضیحات: " + f"{operation.description}" + "\n" + "\n"
    a += "📆تاریخ  ثبت درخواست:" + f" {operation.date}" + "\n"
    a += "⏰ساعت ثبت درخواست:" + f" {operation.time}" + "\n" + "\n"
    o = a
    if result1:
        if result1.get("Success"):
            operation.residhesabfa1 = result1['Result']['Number']
        else:
            a += "کد خطای مرحله اول حسابفا: " + f"{result1['ErrorCode']}" + "\n"
            a += "پیام خطای مرحله اول حسابفا: " + f"{result1['ErrorMessage']}" + "\n"
            o = a
    if result2:
        if result2.get("Success"):
            a += datetaiid()
            dichashtag["idhavale"] = dichashtag["idhavale"] + 1
            dichashtag["idkoli"] = dichashtag["idkoli"] + 1
            h = str(dichashtag["idhavale"]).zfill(6)
            operation.hashtag = dichashtag["idhavale"]
            operation.residhesabfa2 = result2['Result']['Number']
            operation.residkoli = dichashtag["idkoli"]
            if result1['Result']['Number']:
                a += f"#Acc{result1['Result']['Number']}\n"
            a += f"#Acc{result2['Result']['Number']}\n#C{h} \n "
            if operation.jarimenumber:
                a += f"\n#J{operation.jarimenumber}"
            save_data1(operation)
            with open(os.path.join(script_path, "dichashtag.json"), "w") as json_file:
                json.dump(dichashtag, json_file)
        else:
            a += "کد خطای مرحله دوم حسابفا: " + f"{result2['ErrorCode']}" + "\n"
            a += "پیام خطای مرحله دوم حسابفا: " + f"{result2['ErrorMessage']}" + "\n"
            o = o + "کد خطای مرحله دوم حسابفا: " + f"{result2['ErrorCode']}" + "\n" + "پیام خطای مرحله دوم حسابفا: " + f"{result2['ErrorMessage']}" + "\n"
    a = "🔷️🔷️🔷️🔷️🔷️🔷️🔷️" + "\n\n" + "🛃اپراتور: " + f"#O{autorizedusers.get(str(operation.user_id))['code']}" + "\n\n" + a
    return a, o
