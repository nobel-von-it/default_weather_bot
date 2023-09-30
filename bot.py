import asyncio

import requests
import datetime

from googletrans import Translator
from aiogram.enums import ParseMode
from geopy import Nominatim

from config import BOT_TOKEN, WEATHER_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

dp = Dispatcher()
trans = Translator()


@dp.message(CommandStart())
async def start_command(msg: types.Message):
    await msg.reply("hello! write to me the city where you want to know the weather")


@dp.message()
async def get_weather(msg: types.Message):
    geolocation = Nominatim(user_agent="weatherApp")
    city_name = trans.translate(msg.text, dest="en")
    city_loc = geolocation.geocode(city_name.text)

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={city_loc.latitude}&lon={city_loc.longitude}&appid={WEATHER_TOKEN}&units=metric"
        )
        data = r.json()
        # pprint(data)

        name = data["name"]
        current_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_description = data["weather"][0]["description"]

        weather_description_ru = trans.translate(weather_description, dest="ru")

        await msg.reply(
            f"Сегодня {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в {msg.text}:\n"
            f"Погода сейчас: {current_weather}C°,\n"
            f"Описание погоды: {weather_description_ru.text},\n"
            f"Влажность: {humidity}, Скорость ветра: {wind_speed}."
        )
    except:
        await msg.reply("check the city's name")


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('bot started')
    asyncio.run(main())
