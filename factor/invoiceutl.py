def invoicetostr(invoices, user_id):
    if invoices[user_id]["invoice"]["InvoiceType"] == 1:
        r = "\n" + "❇نوع فاکتور: خرید"
    if invoices[user_id]["invoice"]["InvoiceType"] == 0:
        r = "\n" + "❇نوع فاکتور: فروش"
    r = r + "\n" + f"طرف حساب : {invoices[user_id]['invoice']['ContactTitle']}"
    if invoices[user_id]['invoice']['Status'] == '0':
        r = r + "\n" + "وضعیت فاکتور: پیش نویس"
    if invoices[user_id]['invoice']['Status'] == '1':
        r = r + "\n" + "وضعیت فاکتور: تایید شده"
    r = r + "\n" + f"توضیحات فاکتور: {invoices[user_id]['invoice']['Note']}"
    parsed_date = datetime.datetime.strptime(invoices[user_id]['invoice']['DueDate'], '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    r = r + "\n" + "تاریخ: " + f"{jalili_date}" + "\n"
    r = r + "\n" + "◀️    اقلام کالا یا خدمات مندرج در فاکتور:" + "\n"
    ii = 1
    itn = 0
    itm = 0
    for i in invoices[user_id]['invoice']['InvoiceItems']:
        text = next((key for key, value in code_name_mappingkalakhadamatlist.items() if value == i['ItemCode']), None)
        ir = i['Quantity'] * i['UnitPrice']
        itm = itm + ir
        itn = itn + i['Quantity']
        ir = int(ir)
        ir = "{:,}".format(ir)
        iq = int(i['Quantity'])
        iq = "{:,}".format(iq)
        iu = int(i['UnitPrice'])
        iu = "{:,}".format(iu)
        r = r + "\n" + f"❇ردیف : {ii}"
        r = r + "\n" + f"نام کالا یا خدمات: {text}" + "\n" + f"تعداد: {iq}" + "\n" + f"مبلغ واحد: {iu}" + " ریال" + "\n" + f"شرح کالا یا خدمات: {i['Description']}" + "\n" + f"جمع ردیف :{ir}" + " ریال"
        ii = ii + 1
        r = r + "\n"
    itn = int(itn)
    itn = "{:,}".format(itn)
    itm = int(itm)
    itm = "{:,}".format(itm)
    r = r + "\n\n" + "تعداد کل : " + f"{itn}" + "\n" + "مبلغ کل : " + f"{itm}" + "  ریال"
    return r


def invoicetostr(invoices, user_id):
    if invoices[user_id]["invoice"]["InvoiceType"] == 1:
        r = "\n" + "❇نوع فاکتور: خرید"
    if invoices[user_id]["invoice"]["InvoiceType"] == 0:
        r = "\n" + "❇نوع فاکتور: فروش"
    r = r + "\n" + f"طرف حساب : {invoices[user_id]['invoice']['ContactTitle']}"
    if invoices[user_id]['invoice']['Status'] == '0':
        r = r + "\n" + "وضعیت فاکتور: پیش نویس"
    if invoices[user_id]['invoice']['Status'] == '1':
        r = r + "\n" + "وضعیت فاکتور: تایید شده"
    r = r + "\n" + f"توضیحات فاکتور: {invoices[user_id]['invoice']['Note']}"
    parsed_date = datetime.datetime.strptime(invoices[user_id]['invoice']['DueDate'], '%Y-%m-%dT%H:%M:%S')
    jalili_date = JalaliDate(datetime.date(parsed_date.year, parsed_date.month, parsed_date.day))
    r = r + "\n" + "تاریخ: " + f"{jalili_date}" + "\n"
    r = r + "\n" + "◀️    اقلام کالا یا خدمات مندرج در فاکتور:" + "\n"
    ii = 1
    itn = 0
    itm = 0
    for i in invoices[user_id]['invoice']['InvoiceItems']:
        text = next((key for key, value in code_name_mappingkalakhadamatlist.items() if value == i['ItemCode']), None)
        ir = i['Quantity'] * i['UnitPrice']
        itm = itm + ir
        itn = itn + i['Quantity']
        ir = int(ir)
        ir = "{:,}".format(ir)
        iq = int(i['Quantity'])
        iq = "{:,}".format(iq)
        iu = int(i['UnitPrice'])
        iu = "{:,}".format(iu)
        r = r + "\n" + f"❇ردیف : {ii}"
        r = r + "\n" + f"نام کالا یا خدمات: {text}" + "\n" + f"تعداد: {iq}" + "\n" + f"مبلغ واحد: {iu}" + " ریال" + "\n" + f"شرح کالا یا خدمات: {i['Description']}" + "\n" + f"جمع ردیف :{ir}" + " ریال"
        ii = ii + 1
        r = r + "\n"
    itn = int(itn)
    itn = "{:,}".format(itn)
    itm = int(itm)
    itm = "{:,}".format(itm)
    r = r + "\n\n" + "تعداد کل : " + f"{itn}" + "\n" + "مبلغ کل : " + f"{itm}" + "  ریال"
    return r
