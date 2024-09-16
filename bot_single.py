import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler
from openai import OpenAI
import base64

#OPENAI API
client = OpenAI(api_key = '')

# TELEGRAM TOKENS/IDs
GROUP_CHAT_ID = "-4509216306"
BOT_API_TOKEN = ''
BOT_NAME = 'Johnny'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def log_text_to_file(text, file_path="assets/log_file.txt"):
    # Open the file in append mode and write the new text
    with open(file_path, "a") as file:
        file.write(text + "\n")
    print(f"Logged: {text}")

def read_log_text(file_path="assets/log_file.txt"):
    with open(file_path, "r") as file:
        log_content = file.read()
    return log_content

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.type)
    print(update.effective_chat.id)
    print(update.effective_user.full_name)
    print(update.effective_chat.title)
    user_full_name = update.effective_user.full_name
    received_message = update.message.text
    # log_text_to_file('User ' + user_full_name + ' ' + 'just said:' + '"' + received_message + '"')
    # read_log_text()
    # log_text = read_log_text()
    if update.message.photo:  # Check if the photo list is not empty
        print('You are sending a photo')
        # If there's a photo, process it
        file_id = update.message.photo[-1].file_id  # Get the highest resolution photo
        file = await context.bot.get_file(file_id)
        image_bytearray = await file.download_as_bytearray() # Download the photo (or process it)
        print('Image byte:')
        print(image_bytearray)
        base64_encoded = base64.b64encode(image_bytearray)
        image_from_message = base64_encoded.decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Your name is "+ BOT_NAME + ", you speak conyo tagalog. Keep your answer brief and concise."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "React to the image in conyo tagalog. Example, the image is from a movie poster: wow, pinapanood ko din yan pare, it's very good! "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_from_message}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        bot_reply = response.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)
    elif update.message.text:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                # {"role": "system", "content":
                #     "here are the recent messages from other people, please refer to this when needed:" + log_text},
                {"role": "system", "content":
                    "Your name is "+ BOT_NAME + ", you speak conyo tagalog. Keep your answer brief and concise. Under 100 characters if possible.'"},
                {"role": "user", "content": "You're talking to:" + user_full_name + ", here's their message:" + received_message}
            ]
        )
        bot_reply = completion.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)

if __name__ == '__main__':
    bot = ApplicationBuilder().token(BOT_API_TOKEN).build()

    #here is our echo handler for conversation
    echo_handler_1 = MessageHandler((filters.TEXT | filters.PHOTO), conversation)
    bot.add_handler(echo_handler_1)

    bot.run_polling()