import json
import re
from flask import request
from flask import Flask
from flask import jsonify
from flask_sslify import SSLify
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# ~/ngrok http 5000

def convert_currency_xe(src, dst, amount):
    def get_digits(text):
        new_text = ""
        for c in text:
            if c.isdigit() or c == ".":
                new_text += c
        if new_text == "":
            return -100
        return float(new_text)
    
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
    content = requests.get(url).content
    
    soup = bs(content, "html.parser")
    exchange_rate_html = soup.find_all("p")[2]
    return get_digits(exchange_rate_html.text)

def return_money_convert(arr):
    try:
        source_currency = arr[0]
        destination_currency = arr[1]
        amount = float(arr[2])
        exchange_rate = convert_currency_xe(source_currency, destination_currency, amount)
        return exchange_rate
    except Exception as err:
        print(err)
        return -100

def historical_coin_url():
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

    url = f"https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From=23.04.2022&UniDbQuery.To=30.04.2022"
    # url = f"https://www.xe.com/currencycharts/?from={first}&to={second}&view=1D"
    # url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR"
    content = requests.get(url)
    soup = bs(content.text,"html.parser")
    exchange_rate_html = soup.find_all("td")
    arrData=[]
    arrCourse=[]
    count = 0
    for i in exchange_rate_html:
        if count % 3 == 1:
            arrData.append(i.text)
            count += 1
        elif count %  3 == 2:
            count += 1
        elif count % 3 == 0:
            if(count > 0):
                arrCourse.append(get_digits(i.text))
            count += 1
    return arrData, arrCourse
TEXT_ERR = "Неверный запрос, воспользуйся 'help'"
URL = 'https://api.telegram.org/bot5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY/'
# URL = 'https://api.telegram.org/bot5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY/setWebHook?url=https://katyaprokhorchuk.pythonanywhere.com'


app = Flask(__name__)
sslify = SSLify(app)
USD_RUB=['USD','RUB',1]


def parse_response(msg):
    result = []
    regular = r'/\w+'
    for str in msg.split(' '):
        if str == '/convert':
            pass
        else:
            result.append(str)
    print (result)    

    return result


def send_photo(chat_id, file_opened):
    method = "sendPhoto"
    params = {'chat_id': chat_id}
    files = {'photo': file_opened}
    resp = requests.post(URL + method, params, files=files)
    return resp


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        id = r['message']['chat']['id']
        message = r['message']['text']
        print (message)
        regular = r'/\w+'
        if message == '/convert_usd_rub':
            result = USD_RUB
        elif message == '/statistics':
            result = [-1]
        else:
            result = parse_response(message)
        if result:
            if len(result) == 3:
                result_converted=return_money_convert(result)
                if result_converted != -100:
                    send_message(id, text=result_converted)
                else:
                    send_message(id, text='Ошибка')
                return jsonify(r)
            elif (result[0] == -1):
                msg = ''
                arrData, arrCourse = historical_coin_url()
                for i in range(len(arrData)):
                    msg +=  str(arrData[i]) + ' - ' + str(arrCourse[i]) + '\n'
                send_message(id, text=msg)
                plt.plot(list(reversed(arrData)), list(reversed(arrCourse)))
                plt.savefig('my_plot.png')
                plt.close()
                send_photo(id, open('my_plot.png', 'rb'))
            else:
                send_message(id, text = TEXT_ERR)
    return '<h1>hello</h1>'


def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    return r.json()


def send_message(id, text='write "help"'):
    url = URL + 'sendMessage'
    answer = {'chat_id': id, 'text': text, 'id': id}
    r = requests.post(url, json=answer)
    return r.json()




# https://api.telegram.org/bot5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY/setWebhook?url=https://328d-93-175-28-9.eu.ngrok.io
if __name__ == '__main__':
    app.run()
