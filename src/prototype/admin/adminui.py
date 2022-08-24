from telebot import types


def admin_markup():
    admin_markup = types.InlineKeyboardMarkup()
    admin_markup.add(types.InlineKeyboardButton(text='Список всех мероприятий', callback_data='event_list'))
    admin_markup.add(types.InlineKeyboardButton(text='Найти мероприятие по id', callback_data='find_event_by_id'))
    admin_markup.add(types.InlineKeyboardButton(text='Создать новое мероприятие', callback_data='create_event'))
    admin_markup.add(types.InlineKeyboardButton(text='Список всех пользователей', callback_data='users_list'))
    admin_markup.add(types.InlineKeyboardButton(text='Найти пользователя по никнейму', callback_data='find_user_by_nick'))
    admin_markup.add(types.InlineKeyboardButton(text='Создать нового пользователя', callback_data='create_user'))
    return admin_markup

def event_list_markup(events):
    event_list_markup = types.InlineKeyboardMarkup()
    for event in events:
        event_list_markup.add(types.InlineKeyboardButton(text=f'{event.eventname}', callback_data=f'event_id:{event.eventid}'))
    event_list_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return event_list_markup

def event_markup(eventid):
    event_markup = types.InlineKeyboardMarkup()
    event_markup.add(types.InlineKeyboardButton(text='Редактировать', callback_data=f'redact_event:{eventid}'))
    event_markup.add(types.InlineKeyboardButton(text='Показать зачекиненных пользователей', callback_data=f'show_checkin_users:{eventid}'))
    event_markup.add(types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_event:{eventid}'))
    event_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return event_markup

def redact_event_markup(event):
    redact_event_markup = types.InlineKeyboardMarkup()
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Название: {event.eventname}', callback_data=f'redact_event_name:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Промокод: {event.promocode}', callback_data=f'redact_event_promo:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Краткое описание: {event.eventdescription}', callback_data=f'redact_event_description:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Время начала: {event.eventstart}', callback_data=f'redact_event_start:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Время конца: {event.eventend}', callback_data=f'redact_event_end:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Тип: {event.eventtype}', callback_data=f'redact_event_type:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text=f'Организатор: {event.eventmanedger}', callback_data=f'redact_event_manager:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text='Добавить зачекиневшегося пользователя', callback_data=f'add_user_to_checkin:{event.eventid}'))
    redact_event_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return redact_event_markup

def users_list_markup(users):
    users_list_markup = types.InlineKeyboardMarkup()
    for user in users:
        users_list_markup.add(types.InlineKeyboardButton(text=f'{user.usernic}', callback_data=f'user_id:{user.userid}'))
    users_list_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return users_list_markup

def user_markup(userid):
    user_markup = types.InlineKeyboardMarkup()
    user_markup.add(types.InlineKeyboardButton(text='Редактировать', callback_data=f'redact_user:{userid}'))
    user_markup.add(types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_user:{userid}'))
    user_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return user_markup

def redact_user_markup(user):
    redact_user_markup = types.InlineKeyboardMarkup()
    redact_user_markup.add(types.InlineKeyboardButton(text=f'Ник: {user.usernic}', callback_data=f'redact_user_nic:{user.userid}'))
    redact_user_markup.add(types.InlineKeyboardButton(text=f'Имя: {user.userfname}', callback_data=f'redact_user_fname:{user.userid}'))
    redact_user_markup.add(types.InlineKeyboardButton(text=f'Место: {user.userplace}', callback_data=f'redact_user_place:{user.userid}'))
    redact_user_markup.add(types.InlineKeyboardButton(text=f'Роль: {user.userrole}', callback_data=f'redact_user_role:{user.userid}'))
    redact_user_markup.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='beck_to_menu'))
    return redact_user_markup