import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Пробный доступ", callback_data="trial")],
        [InlineKeyboardButton(text="💳 Купить подписку", callback_data="buy")],
        [InlineKeyboardButton(text="📖 Инструкция", callback_data="help")],
    ])
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Это VPN-сервис с быстрым подключением.\n"
        f"🎁 Бесплатный тест — {config.TRIAL_DAYS} дня\n"
        f"💳 Подписка — {config.PRICE_RUB} ₽/мес\n\n"
        "Выберите действие:",
        reply_markup=kb,
    )


@dp.message(Command("trial"))
async def cmd_trial(message: Message):
    await message.answer(
        "🎁 Пробный доступ\n\n"
        "Функция активации trial будет подключена к панели Marzban на следующем шаге.\n"
        "Пока — заглушка."
    )


@dp.message(Command("buy"))
async def cmd_buy(message: Message):
    await message.answer(
        f"💳 Подписка — {config.PRICE_RUB} ₽/мес\n\n"
        "Оплата: СБП / крипта (реквизиты пришлёт поддержка).\n"
        "После оплаты доступ активируется вручную или автоматически."
    )


@dp.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer("📊 Статус: у вас пока нет активной подписки.")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 <b>Как подключиться</b>\n\n"
        "1. Получите ключ (trial или покупка)\n"
        "2. Установите приложение:\n"
        "   • iOS — Streisand / Shadowrocket\n"
        "   • Android — v2rayNG / Hiddify\n"
        "   • Windows — Hiddify / v2rayN\n"
        "3. Импортируйте ключ (QR или ссылка)\n"
        "4. Включите подключение\n\n"
        "Вопросы — /support"
    )


@dp.message(Command("support"))
async def cmd_support(message: Message):
    await message.answer("✉️ Напишите ваш вопрос — админ ответит в течение дня. Или @ваш_ник.")


# обработка кнопок
@dp.callback_query(F.data == "trial")
async def cb_trial(call: CallbackQuery):
    await call.message.answer("🎁 Trial — заглушка, подключим к Marzban.")
    await call.answer()

@dp.callback_query(F.data == "buy")
async def cb_buy(call: CallbackQuery):
    await call.message.answer(f"💳 Оплата {config.PRICE_RUB} ₽ — реквизиты у поддержки.")
    await call.answer()

@dp.callback_query(F.data == "help")
async def cb_help(call: CallbackQuery):
    await cmd_help(call.message)
    await call.answer()


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
