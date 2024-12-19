import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from message_router import MessageRouter

load_dotenv()

class Bot:
    def __init__(self):
        self.router = MessageRouter()
        
    async def start_command(self, update, context):
        await update.message.reply_text("Привет! Вы спрашиваете - я отвечаю?")
    
    async def handle_message(self, update, context):
        text = update.message.text
        print(f'User ({update.message.chat.id}) says: {text}')
        
        response = await self.router.get_llm_response(text)
        await update.message.reply_text(response)
        
    async def error(self, update, context):
        print(f'Update {update} caused error {context.error}')
        
    def run(self):
        print('Starting bot...')
        app = Application.builder().token(os.getenv('TOKEN')).build()
        
        # Commands
        app.add_handler(CommandHandler('start', self.start_command))
        
        # Messages
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        
        # Error handler
        app.add_error_handler(self.error)
        
        # Start polling
        print('Polling...')
        app.run_polling(poll_interval=1)

if __name__ == '__main__':
    bot = Bot()
    bot.run()