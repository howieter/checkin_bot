from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os
import asyncio
from src.prototype.admin import adminui
from src.prototype.dal import database as d
load_dotenv()
bot = AsyncTeleBot(os.getenv("ADMTOK"))


class States:
    state = 0
    S_NORMAL = 0
    S_REDACT_EVENT_NAME = 1
    S_REDACT_EVENT_DESCRIPTION = 2
    S_REDACT_EVENT_TIME_START = 3
    S_REDACT_EVENT_TIME_END = 4
    S_REDACT_EVENT_TYPE = 5
    S_REDACT_EVENT_MANAGER = 6
    S_FIND_EVENT_BY_ID = 7
    S_CREATE_EVENT = 8
    S_REDACT_USER_NICK = 9
    S_REDACT_USER_FNAME = 10
    S_REDACT_USER_PLACE = 11
    S_REDACT_USER_ROLE = 12
    S_FIND_USER_BY_NICK = 13
    S_CREATE_USER = 14
    S_ADD_USER_TO_CHECKIN = 15
    S_REDACT_EVENT_PROMO = 16


class DBObject:
    event = d.Event()
    user = d.User()


@bot.message_handler(commands=['admin'])
async def admin(message):
    await bot.send_message(message.chat.id, 'Чего изволите?', reply_markup=adminui.admin_markup())


@bot.callback_query_handler(func=lambda call: True)
async def query_handler(call):
    # await bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят')
    # Event handler
    if call.data.split(':')[0] == 'redact_event':
        event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(event))
    elif call.data.split(':')[0] == 'redact_event_name':
        States.state = States.S_REDACT_EVENT_NAME
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новое название мероприятия')
    elif call.data.split(':')[0] == 'redact_event_promo':
        States.state = States.S_REDACT_EVENT_PROMO
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новый промокод')
    elif call.data.split(':')[0] == 'redact_event_description':
        States.state = States.S_REDACT_EVENT_DESCRIPTION
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новое краткое описание')
    elif call.data.split(':')[0] == 'redact_event_start':
        States.state = States.S_REDACT_EVENT_TIME_START
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новое время начала мероприятия')
    elif call.data.split(':')[0] == 'redact_event_end':
        States.state = States.S_REDACT_EVENT_TIME_END
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новое время конца мероприятия')
    elif call.data.split(':')[0] == 'redact_event_type':
        States.state = States.S_REDACT_EVENT_TYPE
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новый тип мероприятия')
    elif call.data.split(':')[0] == 'redact_event_manager':
        States.state = States.S_REDACT_EVENT_MANAGER
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите никнейм нового менеджера мероприятия')
    elif call.data == 'event_list':
        events = d.get_events()
        await bot.send_message(call.message.chat.id, 'Список всех мероприятий', reply_markup=adminui.event_list_markup(events))
    elif call.data.split(':')[0] == 'delete_event':
        event = d.get_event_by_id(call.data.split(':')[1])
        event.delete_event()
        await bot.send_message(call.message.chat.id, 'Мероприятие успешно удалено')
        await bot.send_message(call.message.chat.id, 'Чего изволите?', reply_markup=adminui.admin_markup())
    elif call.data == 'find_event_by_id':
        States.state = States.S_FIND_EVENT_BY_ID
        await bot.send_message(call.message.chat.id, 'Введите id мероприятия')
    elif call.data == 'create_event':
        States.state = States.S_CREATE_EVENT
        await bot.send_message(call.message.chat.id,
                               'Пример ввода мероприятия: Тип мероприятия/Название/Краткое описание/Время начала/Время конца/Организатор')
    elif call.data.split(':')[0] == 'event_id':
        event = d.get_event_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, f'Название: {event.eventname}\nКраткое описание: {event.eventdescription}\nПромокод: {event.promocode}',
                               reply_markup=adminui.event_markup(event.eventid))
    elif call.data.split(':')[0] == 'add_user_to_checkin':
        States.state = States.S_ADD_USER_TO_CHECKIN
        DBObject.event = d.get_event_by_id(call.data.split(':')[1])

        await bot.send_message(call.message.chat.id, 'Введите никнейм пользователя')

    # User handler
    elif call.data == 'users_list':
        users = d.get_users()
        await bot.send_message(call.message.chat.id, 'Список всех пользователей', reply_markup=adminui.users_list_markup(users))
    elif call.data.split(':')[0] == 'user_id':
        user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, f'Ник: {user.usernic}\nГород: {user.userplace}',
                               reply_markup=adminui.user_markup(user.userid))
    elif call.data == 'find_user_by_nick':
        States.state = States.S_FIND_USER_BY_NICK
        await bot.send_message(call.message.chat.id, 'Введите никнейм пользователя')
    elif call.data.split(':')[0] == 'redact_user':
        user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(user))
    elif call.data.split(':')[0] == 'redact_user_nic':
        States.state = States.S_REDACT_USER_NICK
        DBObject.user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новый никнейм пользователя')
    elif call.data.split(':')[0] == 'redact_user_fname':
        States.state = States.S_REDACT_USER_FNAME
        DBObject.user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новое имя пользователя')
    elif call.data.split(':')[0] == 'redact_user_role':
        States.state = States.S_REDACT_USER_ROLE
        DBObject.user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новую роль пользователя')
    elif call.data.split(':')[0] == 'redact_user_place':
        States.state = States.S_REDACT_USER_PLACE
        DBObject.user = d.get_user_by_id(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Напишите новый город пользователя')
    elif call.data == 'create_user':
        States.state = States.S_CREATE_USER
        await bot.send_message(call.message.chat.id, 'Пример ввода нового пользователя: Никнейм/Имя/Роль/Город')
    elif call.data.split(':')[0] == 'delete_user':
        event = d.get_user_by_id(call.data.split(':')[1])
        event.delete_user()
        await bot.send_message(call.message.chat.id, 'Пользователь успешно удален')
        await bot.send_message(call.message.chat.id, 'Чего изволите?', reply_markup=adminui.admin_markup())
    elif call.data.split(':')[0] == 'show_checkin_users':
        checkin_users = d.get_checkin_users(call.data.split(':')[1])
        await bot.send_message(call.message.chat.id, 'Список зачекиненных пользователей',
                               reply_markup=adminui.users_list_markup(checkin_users))


    elif call.data == 'beck_to_menu':
        await bot.send_message(call.message.chat.id, 'Чего изволите?', reply_markup=adminui.admin_markup())


@bot.message_handler(content_types=['text'])
async def text_handler(message):
    # Event handler
    if States.state == States.S_REDACT_EVENT_NAME:
        States.state = States.S_NORMAL
        DBObject.event.eventname = message.text
        DBObject.event.update_event()
        # DBObject.event.set_event_name(message.text)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_PROMO:
        States.state = States.S_NORMAL
        DBObject.event.promocode = message.text
        DBObject.event.update_event()
        # DBObject.event.set_event_name(message.text)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_DESCRIPTION:
        States.state = States.S_NORMAL
        DBObject.event.eventdescription = message.text
        DBObject.event.update_event()
        # DBObject.event.set_event_description(message.text)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_TIME_START:
        States.state = States.S_NORMAL
        start_time = message.text
        DBObject.event.eventstart = start_time
        DBObject.event.update_event()
        # DBObject.event.set_event_start(start_time)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_TIME_END:
        States.state = States.S_NORMAL
        end_time = message.text
        DBObject.event.eventend = end_time
        DBObject.event.update_event()
        # DBObject.event.set_event_end(end_time)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_TYPE:
        States.state = States.S_NORMAL
        DBObject.event.eventtype = message.text
        DBObject.event.update_event()
        # DBObject.event.set_event_type(message.text)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_REDACT_EVENT_MANAGER:
        States.state = States.S_NORMAL
        DBObject.event.eventmanedger = message.text
        DBObject.event.update_event()
        # DBObject.event.set_event_manager(message.text)
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(DBObject.event))
    elif States.state == States.S_FIND_EVENT_BY_ID:
        States.state = States.S_NORMAL
        event = d.get_event_by_id(message.text)
        await bot.send_message(message.chat.id, f'Название: {event.eventname}\nКраткое описание: {event.eventdescription}\nПромокод: {event.promocode}',
                               reply_markup=adminui.event_markup(message.text))
    elif States.state == States.S_CREATE_EVENT:
        States.state = States.S_NORMAL
        fields_list = message.text.split('/')
        event = d.Event(eventtype=fields_list[0], eventname=fields_list[1], eventdescription=fields_list[2],
                        eventstart=fields_list[3], eventend=fields_list[4], eventmanedger=fields_list[5])
        event.update_event()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_event_markup(event))

    # User handler
    elif States.state == States.S_REDACT_USER_NICK:
        States.state = States.S_NORMAL
        DBObject.user.usernic = message.text
        DBObject.user.update_user()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(DBObject.user))
    elif States.state == States.S_REDACT_USER_FNAME:
        States.state = States.S_NORMAL
        DBObject.user.userfname = message.text
        DBObject.user.update_user()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(DBObject.user))
    elif States.state == States.S_REDACT_USER_ROLE:
        States.state = States.S_NORMAL
        DBObject.user.userrole = message.text
        DBObject.user.update_user()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(DBObject.user))
    elif States.state == States.S_REDACT_USER_PLACE:
        States.state = States.S_NORMAL
        DBObject.user.userplace = message.text
        DBObject.user.update_user()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(DBObject.user))

    elif States.state == States.S_FIND_USER_BY_NICK:
        States.state = States.S_NORMAL
        user = d.get_user_by_nick(message.text)
        await bot.send_message(message.chat.id, f'Ник: {user.usernic}\nГород: {user.userplace}',
                               reply_markup=adminui.user_markup(user.userid))
    elif States.state == States.S_CREATE_USER:
        States.state = States.S_NORMAL
        fields_list = message.text.split('/')
        user = d.User(usernic=fields_list[0], userfname=fields_list[1],
                      userrole=fields_list[2], userplace=fields_list[3])
        user.update_user()
        await bot.send_message(message.chat.id, 'Редактирование', reply_markup=adminui.redact_user_markup(user))

    elif States.state == States.S_ADD_USER_TO_CHECKIN:
        States.state = States.S_NORMAL
        user = d.get_user_by_nick(message.text)
        ver = d.Ver()
        ver.userid = user.userid
        ver.eventid = DBObject.event.eventid
        ver.verstatus = 2
        ver.update_ver()
        # events_users = DBObject.event.users
        checkin_users = d.get_checkin_users(DBObject.event.eventid)
        # print(dir(checkin_users))
        # print(user1.usernic)
        await bot.send_message(message.chat.id, f'Список зачекиненных пользователей',
                                reply_markup=adminui.users_list_markup(checkin_users))

asyncio.run(bot.polling(non_stop=True))
