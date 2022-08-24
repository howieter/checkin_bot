from telebot import types


def markup_1():
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton(text='Москва', callback_data='msk'))
    markup1.add(types.InlineKeyboardButton(text='Казань', callback_data='kzn'))
    markup1.add(types.InlineKeyboardButton(text='Новосибирск', callback_data='nsk'))
    return markup1


def markup_2():
    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton(text='qr', callback_data='1'))
    markup2.add(types.InlineKeyboardButton(text='промокод', callback_data='2'))
    markup2.add(types.InlineKeyboardButton(text='геолокация', callback_data='3'))
    markup2.add(types.InlineKeyboardButton(text='квиз', callback_data='4'))
    return markup2
