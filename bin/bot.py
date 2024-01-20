import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer
import asyncio
import crawler_tg_bot
import parsing_tomita
import toning
import resum



BOT_TOKEN = '6405501618:AAGPfZz6q5THSrY1BPptvSoy-WfOKK91-L0'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

#async def auto_parsing():
    #while True:
        #await asyncio.sleep(60.0)
        #await crawler_tg_bot.crawler()

# Функция для получения последних 10 новостей
async def get_latest_news():
    conn = sqlite3.connect("db_news_main2.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT title, date_news, url, content
        FROM db_news_main2
        ORDER BY date_news DESC
        LIMIT 10
    ''')
    news_list = cursor.fetchall()

    conn.close()

    return news_list

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Я бот с новостями. Используйте /news, чтобы получить последние новости и /syn *слово с маленькой  буквы*, чтобы искать синонимы для слов")

@dp.message_handler(lambda message: 'syn' in message.text.lower(), content_types=['text'])
async def get_sinWord(message: types.Message):
    sinWordUser = await sinWords(message.text[5:])
    if (sinWordUser):
        text_representation = '\n'.join(sinWordUser)
        await bot.send_message(message.chat.id, str(text_representation), parse_mode=types.ParseMode.HTML)
    else:
        await bot.send_message(message.chat.id, "Синонимы не найдены.", parse_mode=types.ParseMode.HTML)


# Команда /news
@dp.message_handler(commands=['news'])
async def cmd_news(message: types.Message):
    news_list = await get_latest_news()

    for news_item in reversed(news_list):
        title, date, url, content = news_item
        vips, landmarks, tone_flag = await parsing_tomita.get_tomita(content)
        summ, rewr = await resum.get_rewr_summ(content)
        if tone_flag != 0:
            news_tone = await toning.get_tone(content)
            news_text = text(f"<b>{title}</b>\n{date}\n{url}\n\n{content}\n\nВИП-персоны: {vips}\nДостопримечательности: {landmarks}\n\nТональность: {news_tone}\n\nАннотация: {summ}\n\nПерепись: {rewr}")
        else:
            news_text = text(f"<b>{title}</b>\n{date}\n{url}\n\n{content}\n\nВИП-персоны: {vips}\nДостопримечательности: {landmarks}\n\nАннотация: {summ}\n\nПерепись: {rewr}")
        await bot.send_message(message.chat.id, news_text, parse_mode=types.ParseMode.HTML)

async def sinWords(input_word):
    # Инициализация SparkSession
    spark = SparkSession.builder.appName("Word2VecExample").getOrCreate()

    # Подключение к SQLite базе данных
    sqlite_connection = sqlite3.connect("db_news_main2.db") 
    cursor = sqlite_connection.cursor()

    # Загрузка данных из SQLite
    cursor.execute("SELECT content FROM db_news_main2") 
    data = [row[0] for row in cursor.fetchall()]

    # Создание Spark DataFrame
    df = spark.createDataFrame([(text,) for text in data], ["text"])

    # Токенизация текста
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    words_df = tokenizer.transform(df)

    # Обучение модели Word2Vec
    word2Vec = Word2Vec(vectorSize=100, minCount=5, inputCol="words", outputCol="result")
    pipeline = Pipeline(stages=[tokenizer, word2Vec])

    # Обучаем модель
    model = pipeline.fit(df)
    result = model.transform(df)

    # Находим синонимы в модели Word2Vec
    try:
        # Находим синонимы в модели Word2Vec
        synonyms = model.stages[1].findSynonyms(input_word, 5)
        # Преобразуем синонимы в список
        synonyms_list = [row['word'] for row in synonyms.collect()]
        # Выводим результат
        print(f"Синонимы для слова '{input_word}':")
        return synonyms_list
    except Exception as e:
        if "not in vocabulary" in str(e):
            return None
        else:
            raise e

if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #loop.create_task(auto_parsing())
    executor.start_polling(dp, skip_updates=True)
    

    


