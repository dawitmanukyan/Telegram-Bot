from aiogram import Bot, Dispatcher, executor, types
from config import host, user, password, db_name
import pymysql
import random

connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
)

bot = Bot(token='5728249497:AAGRcOYKfJPV_CzUF3morWf0DGOZv6hGmgk')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_comm(message: types.Message):
    await message.answer(
        'Բարի գալուստ EasyDramBot ☺🥰 Այս բոտի շնորհիվ դուք կարող եք աշխատել գումար դիտելով գովազդային հոլովակներ կամ կատարելով որոշակի ոչ բարդ հանձնարարություններ։ ԲՈՏՆ ՈՒՆԻ ԿԱՆՈՆՆԵՐ ՈՐՈՆՔ ԽԱԽՏԵԼՈՒ ԴԵՊՔՈՒՄ ԱԿԿԱՈՒՆՏԸ ԿՍՏԱՆԱ ԲԱՆ ԸՆԴՄԻՇՏ ❗❗❗ 1․ Չի կարելի ստեղծել fake ակկաունտներ (բոլոր ոչակտիվ ակկաունտները ջնջվելու են)։ 2․ Բոլոր վիդեոները կամ փոստերը պետք է նայել մինիմում 1 րոպե։ 3․ Չի կարելի փորձել տեղադրել գովազդ առանց ադմինիստարցիայի հետ կապ հաստատելու։ 4․ Պետք է ուշադիր լրացնել տվյալները, սխալ նշված տվյալին գումար ուղարկելու համար մենք պատասխանատվություն չենք կրում։ 5․ Չի կարելի նույն դրամապանակի տվյալները օգտագործել միքանի ակկաունտում։ Ամեն դիտված փոստից կամ վիդեո ից ստանալու եք 2 դրամ։ Գումարը փոխանցում ենք TellCell, IDram, Qiwi Wallet:')
    await message.answer('Բոլոր հրամաններին ծանոթանալու համար գրեք /commands')


@dp.message_handler(commands=['adminmagical'])
async def admin_comm(message: types.Message):
    await message.answer('Բարի գալուստ Ադմին')


@dp.message_handler(commands=['commands'])
async def commands_comm(message: types.Message):
    await message.answer('/start - easydram - ի մասին')
    await message.answer('/reg - գրանցում համակարգում')
    await message.answer('/balance - իմ հաշիվը')


@dp.message_handler(commands=['reg'])
async def reg_comm(message: types.Message):
    await message.answer('Գրանցում ենք Ձեզ համակարգում, որից հետո դուք կարող եք սկսել գումար աշխատել ☺')
    userpassword = str(random.randint(10000000, 99999999))
    userhash = abs(hash(userpassword))
    telegramid = message.from_user.id
    with connection.cursor() as cursor:
        select_query = f"SELECT * FROM `user` WHERE `telegramid`={telegramid}"
        cursor.execute(select_query)
        result = cursor.fetchone()
        print(result)
    if result == None:
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO `user` (telegramid,password,balance,hash) VALUES ({telegramid},{userpassword},0,'{userhash}')"
            cursor.execute(insert_query)
            connection.commit()
        await message.answer(
            f'Դուք հաջողությամբ գրանցվեցիք, մուտք գործեք մեր կայք "hash" դաշտում գրեք Ձեր ունիվերսալ hash - ը ({userhash}) որից հետո կստանաք Ձեր password - ը և կկարողանաք գրանցել դրամապանակները և ստանալ հավելյալ տվյալներ')
    else:
        await message.answer(f'⛔ Դուք արդեն ունեք ակկաունտ, փորձեք մուտք գործել։')


@dp.message_handler(commands=['balance'])
async def balance_comm(message: types.Message):
    await message.answer('Ստուգում ենք Ձեր հաշիվը 🧐')
    telegid = message.from_user.id
    with connection.cursor() as cursor:
        select_balance = f"SELECT * FROM `user` WHERE `telegramid`={telegid}"
        cursor.execute(select_balance)
        result = cursor.fetchone()
        userbalance = result[3]
        await message.answer(f'{userbalance} դրամ')
        connection.commit()


if __name__ == "__main__":
    executor.start_polling(dp)

connection.close()
