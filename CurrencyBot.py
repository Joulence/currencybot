import telebot
import requests
from bs4 import BeautifulSoup

#Parser
Ruble = 'https://www.google.com/search?sxsrf=ALeKk004kXNJfsllJl0Xw2Bc3nb-WYY9ig:1596027882197&q=1+%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&spell=1&sa=X&ved=2ahUKEwj75-CXw_LqAhXBtYsKHfBAAP0QBSgAegQIDBAq&biw=1366&bih=625'
Euro = 'https://www.google.com/search?sxsrf=ALeKk02KYraELoPUIiXGNdX3dLSHcwjLOg%3A1596026954419&ei=SnAhX7-MGYn9rgTS6JngBg&q=1+%D0%95%D0%B2%D1%80%D0%BE+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&oq=1+%D0%95%D0%B2%D1%80%D0%BE+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&gs_lcp=CgZwc3ktYWIQAzIECAAQDTIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yCAgAEAgQBxAeOgcIABCwAxBDUMK8NlibyzZg78s2aAZwAHgAgAF4iAGrBJIBAzEuNJgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwi_2a3dv_LqAhWJvosKHVJ0BmwQ4dUDCAw&uact=5'
Dollar = 'https://www.google.com/search?q=1+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&oq=1+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&aqs=chrome.0.69i59j35i39j0l6.3275j0j7&sourceid=chrome&ie=UTF-8'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

USD = requests.get(Dollar, headers=headers)
EUR = requests.get(Euro, headers=headers)
RUB = requests.get(Ruble, headers=headers)

# Bot
bot = telebot.TeleBot("1083710257:AAHZeTXk1COZcFt5nCaih1aXE8WJx9mHZ7k")

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Доллар(USD)', 'Евро(EUR)', "Рубль(RUB)")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi, " + message.chat.first_name + "!")
    bot.send_message(message.chat.id, "Я - CurrencyBot, я слежу за стоимостью валют в гривнах")
    bot.send_message(message.chat.id, "Выбери одну из валют, чтобы узнать сколько стоит", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Доллар(USD)':
        soup = BeautifulSoup(USD.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        bot.send_message(message.chat.id, "1 доллар = " + convert[0].text + " гривен")

    elif message.text == 'Евро(EUR)':
        soup = BeautifulSoup(EUR.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        bot.send_message(message.chat.id, "1 евро = " + convert[0].text + " гривен")

    elif message.text == 'Рубль(RUB)':
        soup = BeautifulSoup(RUB.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        bot.send_message(message.chat.id, "1 рубль = " + convert[0].text + " гривен")

    else:
        bot.send_message(message.chat.id, "Выберите валюту!")

bot.polling()