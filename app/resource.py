from app.Global import TEXT_ERR, HELP, DATA, FLAGCOMMMAND, STATISTICS, command, COMMANDHELP, USD_RUB
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import requests
import time
from flask import jsonify
from flask import request
import time



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
    """
    преобразовывает строку в число
    """
    new_text = ""
    for c in text:
        if c.isdigit() or c == ".":
            new_text += c
    if new_text == "":
        return -100
    return float(new_text)


def convert_currency_xe(src, dst, amount):
    """
    парсит сайт и получает конвертируемую сумму в указанной валюте
    """
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
    """
    конвертирует валюту
    """
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



def get_digits(text):
    """
    преобразовывает строку в число
    """
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


def historical_coin_url(data1, data2, bot):
    """
    парсит сайт и получает курс
    """
    url = f"https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From={data1}&UniDbQuery.To={data2}"
    try:
        content = requests.get(url)
    except requests.exceptions.Timeout as e:
        bot.send_message(chat_id = id, text='Упс... Что-то пошло не так')
        raise SystemExit(e)
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
    


def plotconfig(arrData, arrCourse,bot):
    """
    строит график изменения цены в от начальной до конечной даты
    """
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


def graphStat(result, id, bot):
    """
    получает данные по изменению курса и отправляет пользователю результат
    """
    print("res=", result)
    data1 = result[0]
    data2 = result[1]
    arrData, arrCourse = historical_coin_url(data1, data2, bot)
    if arrData!=0 and arrCourse!=0:
        plotconfig(arrData, arrCourse,bot)
        bot.send_photo(chat_id = id, photo=open('my_plot.png', 'rb'))

def sendRes(result,r, id, bot):
    """
    отправляет пользователю результат
    """
    global FLAGCOMMMAND, STATISTICS, command, COMMANDHELP
    if result:
        if len(result) == 3 and FLAGCOMMMAND == 0:
            result_converted = return_money_convert(result)
            command = 0
            if result_converted != -100:
                bot.send_message(chat_id = id, text=result_converted)
            else:
                bot.send_message(chat_id = id, text='Ошибка')
            return jsonify(r)
        elif STATISTICS == 2:
            bot.send_message(chat_id = id, text=DATA)
            STATISTICS = 0
            command = 0
        elif STATISTICS == 1:
            STATISTICS = 0
            graphStat(result, id, bot)

            command = 0
        elif COMMANDHELP == 1:
            COMMANDHELP = 0
            command = 0
            bot.send_message(chat_id = id, text=HELP)
        else:
            bot.send_message(chat_id = id, text='Упс... Что-то пошло не так')

def postBot(bot):
    """
    парсит строку на наличие команд, проверяет правильность ввода и вызывает необходимую функцию для выполнения запроса
    """
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
    sendRes(result, r, id,bot)
