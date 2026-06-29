from email import message

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, \
    CallbackQueryHandler, CommandHandler, ContextTypes
from credentials import ChatGPT_TOKEN
from gpt import ChatGptService
from util import load_message, load_prompt, send_text_buttons, send_text, \
    send_image, show_main_menu, Dialog, default_callback_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'main'

    # load and display the main screen
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)

    # display the main menu
    await show_main_menu(update, context, {
        'start': 'Main menu',
        'random': 'Get a random interesting fact 🧠',
        'gpt': 'Ask ChatGPT a question 🤖',
        'talk': 'Talk to a famous personality 👤',
        'quiz': 'Take a quiz ❓'
        # You can add a new command to the menu like this:
        # 'command': 'button text'
    })

    answer = await chat_gpt.add_message(update.message.text)
    await message.edit_text(answer)

dialog = Dialog()
dialog.mode = None

chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler('start', start))


# You can register a command handler like this:
# app.add_handler(CommandHandler('command', handler_func))
async def gpt_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # notify the user that the response is being generated
    message = await send_text(update, context, 'Thinking about your question...')

    answer = await chat_gpt.add_message(user_text)
    await message.edit_text(answer)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
        :param update:
        :param context:
        :return:
    '''

    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    else:
        await start(update, context)


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt('random')

    await send_image(update, context, 'random')
    answer = await chat_gpt.send_question(prompt, '')
    await send_text_buttons(update, context, answer, {
        'random': 'I want another random fact'
    })


quiz_data = {
    'task_1': 'sport',
    'task_2': 'cinema',
    'task_3': 'science',
    'task_4': 'history'
}


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # prompt the user to choose a quiz topic
    await send_text_buttons(
        update,
        context,
        'Choose a topic to play:',
        quiz_data
    )


async def quiz_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn = update.callback_query.data
    await update.callback_query.answer()

    # prepare the prompt for ChatGPT
    to_chatgpt = quiz_data[btn]
    chat_gpt.set_prompt('Test your knowledge together with ChatGPT!')

    message = await send_text(update, context, 'Thinking about the answer...')
    answer = await chat_gpt.add_message(to_chatgpt)
    await message.edit_text(answer)


async def random_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await random(update, context)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'gpt'
    prompt = load_prompt('gpt')
    message = load_message('gpt')
    chat_gpt.set_prompt(prompt)
    await send_image(update, context, 'gpt')
    await send_text(update, context, message)
    await show_main_menu(update, context, message)
    #add answer
    answer = await chat_gpt.add_message(update.message.text)
    await message.edit_text(answer)

app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
# You can register a button handler like this:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(random_button, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(quiz_button, pattern='^quiz_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
