import requests
from flask import jsonify
from flask import request
from bs4 import BeautifulSoup as bs
from app.Global import TEXT_ERR, HELP, URL, DATA, FLAGCOMMMAND, STATISTICS, command, COMMANDHELP, USD_RUB
import time
import matplotlib.pyplot as plt


def parse_response(msg):
    result = []
    regular = r'/\w+'
    for str in msg.split(' '):
        if str == '/convert':
            pass
        else:
            result.append(str)
    return result


def get_digit(text):
    new_text = ""
    for c in text:
        if c.isdigit() or c == ".":
            new_text += c
    if new_text == "":
        return -100
    return float(new_text)


def convert_currency_xe(src, dst, amount):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
    try:
        content = requests.get(url).content

        soup = bs(content, "html.parser")
        exchange_rate_html = soup.find_all("p")[2]
        return get_digit(exchange_rate_html.text)
    except:
        time.sleep(5)
        convert_currency_xe(src, dst, amount)


def return_money_convert(arr):
    try:
        source_currency = arr[0]
        destination_currency = arr[1]
        amount = float(arr[2])
        exchange_rate = convert_currency_xe(
            source_currency, destination_currency, amount)
        return exchange_rate
    except Exception as err:
        print(err)
        return -100


def send_photo(chat_id, file_opened):
    method = "sendPhoto"
    params = {'chat_id': chat_id}
    files = {'photo': file_opened}
    resp = requests.post(URL + method, params, files=files)
    return resp


def send_message(id, text='write "help"'):
    url = URL + 'sendMessage'
    answer = {'chat_id': id, 'text': text, 'id': id}
    r = requests.post(url, json=answer)
    return r.json()


def get_digits(text):
    new_text = ""
    for c in text:
        if c.isdigit() or c == ",":
            if c == ',':
                new_text += '.'
            else:
                new_text += c
    if new_text == "":
        return -100
    return float(new_text)


def historical_coin_url(data1, data2):
    url = f"https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From={data1}&UniDbQuery.To={data2}"
    content = requests.get(url)
    soup = bs(content.text, "html.parser")
    exchange_rate_html = soup.find_all("td")
    arrData = []
    arrCourse = []
    count = 0
    for i in exchange_rate_html:
        if count % 3 == 1:
            arrData.append(i.text)
            count += 1
        elif count % 3 == 2:
            count += 1
        elif count % 3 == 0:
            if(count > 0):
                arrCourse.append(get_digits(i.text))
            count += 1
            
    return arrData, arrCourse

def plotconfig(arrData, arrCourse):
    fig, ax = plt.subplots()
    ax.plot(list(reversed(arrData)), list(
        reversed(arrCourse)), color='b', linewidth=3)
    ax.tick_params(axis='both',  # Применяем параметры к обеим осям
                   which='major',  # Применяем параметры к основным делениям
                   length=2,  # Длинна делений
                   width=1,  # Ширина делений
                   color='m',  # Цвет делений
                   pad=2,  # Расстояние между черточкой и ее подписью
                   labelsize=8,  # Размер подписи
                   labelcolor='r',  # Цвет подписи
                   bottom=True,  # Рисуем метки снизу
                   top=False,
                   left=True,  # слева
                   right=False,  # и справа
                   labelbottom=True,  # Рисуем подписи снизу
                   labeltop=False,  # сверху
                   labelleft=True,  # слева
                   labelright=False,  # и справа
                   labelrotation=30)  # Поворот подписей
    plt.savefig('my_plot.png')


def graphStat(result, id):
    msg = ''
    print("res=", result)
    data1 = result[0]
    data2 = result[1]
    arrData, arrCourse = historical_coin_url(data1, data2)

    for i in range(len(arrData)):
        msg += str(arrData[i]) + ' - ' + str(arrCourse[i]) + '\n'
    send_message(id, text=msg)
    plotconfig(arrData, arrCourse)
    send_photo(id, open('my_plot.png', 'rb'))

def sendRes(result,r, id):
    global FLAGCOMMMAND, STATISTICS, command, COMMANDHELP

    if result:
        if len(result) == 3 and FLAGCOMMMAND == 0:
            result_converted = return_money_convert(result)
            command = 0
            if result_converted != -100:
                send_message(id, text=result_converted)
            else:
                send_message(id, text='Ошибка')
            return jsonify(r)
        elif STATISTICS == 2:
            send_message(id, text=DATA)
            STATISTICS = 0
            command = 0
        elif STATISTICS == 1:
            STATISTICS = 0
            graphStat(result, id)
            command = 0
        elif COMMANDHELP == 1:
            COMMANDHELP = 0
            command = 0
            send_message(id, text=HELP)
        else:
            send_message(id, text=TEXT_ERR)

def postBot():
    global FLAGCOMMMAND, STATISTICS, command, COMMANDHELP

    r = request.get_json()
    id = r['message']['chat']['id']
    message = r['message']['text']
    result = parse_response(message)
    print(message)
    if message == '/convert_usd_rub':
        result = USD_RUB
        command = 1
        FLAGCOMMMAND = 0
    elif message == '/statistics':
        STATISTICS = 2
        FLAGCOMMMAND = 1
        command = 1
    elif message == '/help':
        COMMANDHELP = 1
        FLAGCOMMMAND = 0
        command = 1
    if FLAGCOMMMAND == 1 and command == 0:
        FLAGCOMMMAND = 0
        STATISTICS = 1
    sendRes(result, r, id)
