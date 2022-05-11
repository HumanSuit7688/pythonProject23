from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import lxml

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# Make a Button
usd_currency = KeyboardButton('USD')
eur_currency = KeyboardButton('EUR')
jpy_currency = KeyboardButton('JPY')
cny_currency = KeyboardButton('CNY')
btc_currency = KeyboardButton('BTC')
# Make a Keyboard
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# Add button to the Keyboard
keyboard.add(usd_currency)
keyboard.add(eur_currency)
keyboard.add(jpy_currency)
keyboard.add(cny_currency)
keyboard.add(btc_currency)

# Address the bot via a token
bot = Bot(token='5266259969:AAHGpg4WnvGj0UGQz0wWxSfcLMS-8aG6ruU')
# Load Bot in the Task Manager
disp = Dispatcher(bot)
ua = UserAgent()
currency_url = 'https://www.cbr.ru/currency_base/daily/'
agent = {'User-agent': ua.random}

# Create a Handler for the Command /start
@disp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Send text in the Reply
    await message.reply('Hi! I am Bot '
                        'that tells you the dollar exchange rate '
                        'according to the Central Bank of Russia.', reply_markup=keyboard)

# Create a handler for the USD text, which we wrap in a button
@disp.message_handler(text=['USD'])
async def get_currency_usd(message: types.Message):
    # Create a global variable in which we place the value from the table.
    global usd_value
    # Query the page (the 'currency_url' variable stores the address of the site)
    response = requests.get(currency_url, headers=agent)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('div', class_='table-wrapper') \
        .find('div', class_='table') \
        .find('table', class_='data') \
        .find('tbody')
    all_strings = tbody.find_all('tr')  # Search all strings
    for ev_string in all_strings:
        columns = ev_string.find_all('td')
        if len(columns) != 0 and 'USD' in columns[1]:
            usd_value = columns[4]
    await message.reply(*usd_value, reply_markup=keyboard)

@disp.message_handler(text=['EUR'])
async def get_currency_eur(message: types.Message):
    global eur_value
    response = requests.get(currency_url, headers=agent)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('div', class_='table-wrapper') \
        .find('div', class_='table') \
        .find('table', class_='data') \
        .find('tbody')
    all_strings = tbody.find_all('tr')
    for ev_string in all_strings:
        columns = ev_string.find_all('td')
        if len(columns) != 0 and 'EUR' in columns[1]:
            eur_value = columns[4]
    await message.reply(*eur_value, reply_markup=keyboard)

@disp.message_handler(text=['JPY'])
async def get_currency_jpy(message: types.Message):
    global jpy_value
    response = requests.get(currency_url, headers=agent)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('div', class_='table-wrapper') \
        .find('div', class_='table') \
        .find('table', class_='data') \
        .find('tbody')
    all_strings = tbody.find_all('tr')
    for ev_string in all_strings:
        columns = ev_string.find_all('td')
        if len(columns) != 0 and 'JPY' in columns[1]:
            jpy_value = columns[4]
    await message.reply(*jpy_value, reply_markup=keyboard)

@disp.message_handler(text=['CNY'])
async def get_currency_cny(message: types.Message):
    global cny_value
    response = requests.get(currency_url, headers=agent)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('div', class_='table-wrapper') \
        .find('div', class_='table') \
        .find('table', class_='data') \
        .find('tbody')
    all_strings = tbody.find_all('tr')
    for ev_string in all_strings:
        columns = ev_string.find_all('td')
        if len(columns) != 0 and 'CNY' in columns[1]:
            cny_value = columns[4]
    await message.reply(*cny_value, reply_markup=keyboard)

@disp.message_handler(commands=['BTC_to_USD'])
async def btc_to_usd(message: types.Message):
   get_btc_to_usd = cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
   print(f'BTC to USD: {get_btc_to_usd}$')

if __name__ == '__main__':
    executor.start_polling(disp)