import openai
import telegram

# Set up the OpenAI API client
openai.api_key = "<your OpenAI API key>"

# Set up the Telegram bot
bot = telegram.Bot(token="<your bot token>")

# Set a flag to indicate whether the bot is running
is_running = False

# Listen for incoming messages
for update in bot.get_updates():
    # Get the message text
    message = update.message.text

    # Check if the message is a command to start or stop the bot
    if message == "/start":
        is_running = True
        bot.send_message(chat_id=update.message.chat_id, text="Bot started")
    elif message == "/stop":
        is_running = False
        bot.send_message(chat_id=update.message.chat_id, text="Bot stopped")

    # If the bot is running, use the OpenAI API to generate a response
    if is_running:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            max_tokens=1024,
            temperature=0.5
        )

        # Send the response to the user
        bot.send_message(chat_id=update.message.chat_id, text=response["choices"][0]["text"])