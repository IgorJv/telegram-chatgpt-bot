from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, \
    BotCommand, MenuButtonCommands, BotCommandScopeChat, MenuButtonDefault
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


# serializes a User object into a string representation
def dialog_user_info_to_str(user_data: dict) -> str:
    mapper = {
        'language_from': 'Source language',
        'language_to': 'Target language',
        'text_to_translate': 'Text to translate'
    }

    return '\n'.join(
        f"{mapper.get(key, key)}: {value}"
        for key, value in user_data.items()
    )


# sends a text message to the chat
async def send_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str
) -> Message:
    # validate markdown formatting
    if text.count('_') % 2 != 0:
        message = (
            f"The string '{text}' is not valid Markdown. "
            f"Please use send_html() instead."
        )
        print(message)
        return await update.message.reply_text(message)

    # handle surrogate pairs correctly
    text = text.encode('utf-16', errors='surrogatepass').decode('utf-16')

    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


# sends an HTML-formatted text message to the chat
async def send_html(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    text: str) -> Message:
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id,
                                          text=text, parse_mode=ParseMode.HTML)


# sends a text message to the chat and attaches buttons
async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            text: str, buttons: dict) -> Message:
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    keyboard = []
    for key, value in buttons.items():
        button = InlineKeyboardButton(str(value), callback_data=str(key))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return await context.bot.send_message(
        update.effective_message.chat_id,
        text=text, reply_markup=reply_markup,
        message_thread_id=update.effective_message.message_thread_id)


# sends a photo to the chat
async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     name: str) -> Message:
    with open(f'resources/images/{name}.jpg', 'rb') as image:
        return await context.bot.send_photo(chat_id=update.effective_chat.id,
                                            photo=image)


# displays the command list and the main menu
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         commands: dict):
    command_list = [BotCommand(key, value) for key, value in commands.items()]
    await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(
        chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(),
                                           chat_id=update.effective_chat.id)


# clears previously registered commands for the current chat
async def hide_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonDefault(),
                                           chat_id=update.effective_chat.id)


# loads a message from the /resources/messages/ directory
def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


# loads a predefined prompt from the /resources/messages/ directory
def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    await send_html(update, context, f'You have pressed button with {query} callback')


class Dialog:
    pass
