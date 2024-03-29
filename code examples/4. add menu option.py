import openai
import telegram
import asyncio

# Set up the OpenAI API client
openai.api_key = "<your OpenAI API key>"

# Set up the Telegram bot
bot = telegram.Bot(token="<your bot token>")

# Set a flag to indicate whether the bot is running
is_running = False

# Set the time for the daily reminder (9pm)
reminder_time = 21  # 24-hour clock

# Create the keyboard with the menu options
menu_keyboard = [
    ["/start", "/stop"],  # First row
    ["/menu"],  # Second row
]
menu = telegram.ReplyKeyboardMarkup(menu_keyboard)

async def main():
    # Listen for incoming messages
    while True:
        updates = await bot.get_updates()

        for update in updates:
            # Get the message text
            message = update.message.text

            # Check if the message is a command
            if message == "/start":
                is_running = True
                bot.send_message(chat_id=update.message.chat_id, text="Bot started")
            elif message == "/stop":
                is_running = False
                bot.send_message(chat_id=update.message.chat_id, text="Bot stopped")
            elif message == "/menu":
                # Send the menu keyboard
                bot.send_message(chat_id=update.message.chat_id, text="Menu:", reply_markup=menu)

            # If the bot is running, use the OpenAI API to generate a response
            if is_running:
                # Check the current time
                current_time = time.localtime().tm_hour

                # If it's time for the daily reminder, send it
                if current_time == reminder_time:
                    bot.send_message(chat_id=update.message.chat_id, text="Don't forget to take your medication!")

                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=message,
                    max_tokens=1024,
                    temperature=0.5
                )

                # Send the response to the user
                bot.send_message(chat_id=update.message.chat_id, text=response["choices"][0]["text"])

        # Pause for one day before checking the time again
        await asyncio.sleep(86400)

asyncio.run(main())
