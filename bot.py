import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram import Update

from variables import TOKEN
from database import Database


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

NAME, EMAIL = range(2)

class Bot:
    def __init__(self, token):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start)
        add_email_handler = ConversationHandler(
            entry_points=[CommandHandler('add', self.add_email)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_name)],
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_email)],
            },
            fallbacks=[]
        )
        self.application.add_handler(start_handler)
        self.application.add_handler(add_email_handler)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome! {update.effective_chat.id}")

    async def add_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Enter your friend Name: ")
        return NAME

    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['name'] = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Enter your friend Email: ")
        return EMAIL

    async def get_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        friend_name = context.user_data['name']
        friend_email = update.message.text
        database = Database()
        database.save_new_email(
            id=user_id,
            name=friend_name,
            email=friend_email,
            template='This is template'
        )
        await context.bot.send_message(chat_id=user_id, text=f"Your data is saved!")
        return ConversationHandler.END

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    bot.run()