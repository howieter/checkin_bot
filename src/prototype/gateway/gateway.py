from src.prototype.kernel import bot as bt
from src.prototype.basicui import back as b
from src.prototype.dal import database as d
from src.prototype.dal import schooldb as s

# load_dotenv()
# bot = AsyncTeleBot(os.getenv("TOK"))
bot = bt.Bot.sBot
command = ''
user_info = []
flag = 0
Event = d.Event()
User = d.User()
Ver = d.Ver()


@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.from_user.id, "Выбери команду из меню")


@bot.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.from_user.id, "Сначала нужно зарегистрироваться, а уже потом вводить код, дуршка) ")


@bot.message_handler(commands=['login'])
async def login(message):
    global command
    command = 'login'
    log = d.get_user(message.chat.id)
    if not log:
        await bot.send_message(message.chat.id, "введи свой ник")
    else:
        command = 'done'
        await bot.send_message(message.chat.id, "Вы уже зарегистрированы")


@bot.message_handler(commands=['createevent'])
async def event(message):
    await bot.send_message(message.chat.id, "введите название мероприятия")


@bot.message_handler(commands=['putcode'])
async def read_code(message):
    global command, flag, User
    User = d.get_user(message.chat.id)
    if User is None:
        command = 'done'
        await bot.send_message(message.chat.id, "Нужно зарегистрироваться")
    else:
        command = 'putcode'
        flag = 1
        await bot.send_message(message.chat.id, "Введите код мероприятия")


@bot.callback_query_handler(func=lambda call: True)
async def query_handler(call):
    global user_info, User, command
    await bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят')
    answer = ''
    if command == 'login':
        if call.data == 'msk':
            answer = 'Москва'
        elif call.data == 'kzn':
            answer = 'Казань'
        elif call.data == 'nsk':
            answer = 'Новосибирск'
        user_info.append(answer)
        status = d.add_user(user_info)
        if status != 1:
            command = 'done'
            await bot.send_message(call.message.chat.id, "Вы зарегистрированы")
        else:
            await bot.send_message(call.message.chat.id, "Что-то пошло не так")
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
async def log_name(message):
    global user_info, command, Event, User, Ver, flag
    User = d.get_user(message.chat.id)
    if command == 'login':
        n = s.check_user(message.text.lower())
        if not n:
            user_info.append(message.chat.id)
            user_info.append(message.text.lower())
            user_info.append(message.from_user.first_name)
            role = s.get_role(message.text.lower())
            user_info.append(role)
            await bot.send_message(message.chat.id, "Из какого ты кампуса?", reply_markup=b.markup_1())
        else:
            await bot.send_message(message.chat.id, "Пользователь не найден")
    elif command == 'putcode':
        if flag:
            flag = 0
            Ver = d.get_ver(User.usernic, message.text)
            if Ver is None:
                d.add_ver(User.usernic, 0)
                Ver = d.get_ver(User.usernic, 0)
        if d.get_event(message.text) and d.get_status(User.usernic, 0) == 0:
            print(message.text)
            Event = d.get_event(message.text)
            print(Event.eventmanedger)
            if User.usernic == Event.eventmanedger:
                Ver.delete_ver()
                command = 'done'
                await bot.send_message(message.chat.id, "Вы организатор")
            else:
                Ver.eventid = Event.eventid
                Ver.verstatus = 1
                Ver.update_ver()
                await bot.send_message(message.chat.id, "Введите промокод")
        elif not d.get_event(message.text) and d.get_status(User.usernic, 0) == 0:
            await bot.send_message(message.chat.id, "Такого мероприятия нет. Повторите ввод.")
        elif Ver.eventid != 0:
            if message.text == Event.promocode and d.get_status(User.usernic, Event.eventid) == 1:
                Ver.verstatus = 2
                Ver.update_ver()
                command = 'done'
                await bot.send_message(message.chat.id, "Верификация пройдена")
            elif message.text != Event.promocode and d.get_status(User.usernic, Event.eventid) == 1:
                await bot.send_message(message.chat.id, "Верификация не пройдена")
            elif Ver.verstatus == 2:
                command = 'done'
                await bot.send_message(message.chat.id, "Участие подтверждено")
        else:
            await bot.send_message(message.chat.id, "что-то пошло не так, повторите ввод")
    elif command == 'done':
        await bot.send_message(message.chat.id, "что-то пошло не так, повторите ввод или нажмите команду help")

bt.Bot.bot_polling(bot)
# asyncio.run(bot.polling(non_stop=True))
