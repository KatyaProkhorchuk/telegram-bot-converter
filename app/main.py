import json
from flask import request
from flask import Flask
from flask import jsonify
from flask_sslify import SSLify
import requests
from bs4 import BeautifulSoup as bs

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
    
    source_currency = arr[0]
    destination_currency = arr[1]
    amount = float(arr[2])
    exchange_rate = convert_currency_xe(source_currency, destination_currency, amount)
    return exchange_rate

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
        else:
            result = parse_response(message)
        
        if len(result) == 3:
            result_converted=return_money_convert(result)
            if result_converted != -100:
                send_message(id, text=result_converted)
            else:
                send_message(id, text='Ошибка')
            return jsonify(r)
        else:
            send_message(id, text = TEXT_ERR)
    return '<h1>hello</h1>'


# def write_json(data, filename='answer.json'):
#     with open(filename, 'w') as file:
#         json.dump(data, file, indent=2, ensure_ascii=False)


def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    return r.json()
    # write_json(r.json())


def send_message(id, text='write "help"'):
    url = URL + 'sendMessage'
    answer = {'chat_id': id, 'text': text, 'id': id}
    r = requests.post(url, json=answer)
    return r.json()




# https://api.telegram.org/bot5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY/setWebhook?url=https://328d-93-175-28-9.eu.ngrok.io
if __name__ == '__main__':
    app.run()
