import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


BOT_TOKEN = "8445248620:AAGZ7MiEPDUmyIBvN8kz7747ZjuhmZzcp1g"


WELCOME_MESSAGE = """Добро пожаловать в детскую языковую мастерскую «БЕЗ БАРЬЕРА» — пространство, где дети учатся говорить уверенно, красиво и с удовольствием 💬✨

Мы помогаем малышам развивать речь, мышление и уверенность в себе через игру и живое общение.

Если вы хотите, чтобы ваш ребёнок говорил свободно и с радостью — <b><u>запишитесь на пробное занятие прямо сейчас</u></b>! 💛"""

# Ссылки
LINKS = {
    'zapis': 'tg://resolve?domain=bezbaryera_english',  # Deep link для открытия диалога с обычным аккаунтом
    'telegram': 'https://t.me/berbaryera_english',
    'instagram': 'https://www.instagram.com/bezbaryera_english?igsh=MWNyM2RsNTR4M3d3bQ%3D%3D&utm_source=qr'
}


sent_welcome = set()


def create_main_keyboard():
    
    keyboard = [
        [InlineKeyboardButton("📍Записаться на занятия", url=LINKS['zapis'])],
        [InlineKeyboardButton("🕊️Наш телеграм-канал", url=LINKS['telegram'])],
        [InlineKeyboardButton("💫Наш инстаграм", url=LINKS['instagram'])]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_id = update.effective_user.id
    

    if user_id not in sent_welcome:
        keyboard = create_main_keyboard()
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        sent_welcome.add(user_id)
        logger.info(f"Приветственное сообщение отправлено пользователю {user_id}")
    else:
        
        keyboard = create_main_keyboard()
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=keyboard
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    logger.error(f"Update {update} caused error {context.error}")


def main():
    
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    
    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error_handler)
    
    
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

