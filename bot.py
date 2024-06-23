import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram import Update

from variables import TOKEN
from database import Database
from mail import Mail


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

NAME, EMAIL, SUBJECT, BODY = range(4)

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
                SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_subject)],
                BODY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_body)],
            },
            fallbacks=[]
        )
        sent_handler = CommandHandler('send', self.send)

        self.application.add_handler(start_handler)
        self.application.add_handler(add_email_handler)
        self.application.add_handler(sent_handler)
    
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
        context.user_data['email'] = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter Email's Subject: ")
        return SUBJECT

    async def get_subject(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['subject'] = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter Email's Body: ")
        return BODY

    async def get_body(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        name = context.user_data['name']
        email = context.user_data['email']
        subject = context.user_data['subject']
        body = update.message.text

        database = Database()
        database.save_new_email(
            id=user_id,
            name=name,
            email=email,
            subject=subject,
            body=body,
        )

        await context.bot.send_message(chat_id=user_id, text="Data has been saved!")
        return ConversationHandler.END
    
    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_chat.id
        mail = Mail(sender='yugrana854@gmail.com')
        mail.send_email_from(user_id=user_id)
        await context.bot.send_message(chat_id=user_id, text="All the mails has been sent!✉️")

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    bot.run()