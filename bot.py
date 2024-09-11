import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from openai import OpenAI

#OPENAI API
client = OpenAI(api_key = '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')

# TELEGRAM TOKENS/IDs
GROUP_CHAT_ID = "-4509216306"
BOT1_API_TOKEN = '7276036723:AAHjzVq1CnD6Ra5W8bACAhSPEzfT-xFIbfo'
BOT2_API_TOKEN = '7186428106:AAEGPaGHH2uREVJqmYWffRFmSIqKEK_Wtzw'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def echo_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update.effective_chat.type)
        print(update.effective_chat.id)
        print(update.effective_user.full_name)
        print(update.effective_chat.title)
        user_full_name = update.effective_user.full_name
        received_message = update.message.text
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Your name is Johnny, you act as anyone's long time friend. Keep your answer brief and concise. Under 100 characters if possible."},
                {"role": "user", "content": "You're talking to:" + user_full_name + ", here's their message:" + received_message}
            ]
        )
        bot_reply = completion.choices[0].message.content
        print(completion.choices[0].message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    bot_1 = ApplicationBuilder().token(BOT1_API_TOKEN).build()
    bot_2 = ApplicationBuilder().token(BOT2_API_TOKEN).build()

    # start_handler = CommandHandler('start', start)
    echo_handler_1 = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_1)
    bot_1.add_handler(echo_handler_1)
    # application.add_handler(echo_handler)

    bot_1.run_polling()