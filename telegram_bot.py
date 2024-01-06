import random
import numpy as np
from copy import deepcopy
import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')
CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [ [FREE_SPACE for _ in range(3) ] for _ in range(3) ]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'X (your) turn! Please, put X to the free ceil', reply_markup=reply_markup)

    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    query = update.callback_query
    idx1, idx2 = int(query.data[0]), int(query.data[1])
    if not won(np.array(context.user_data['keyboard_state']).flatten()) and context.user_data['keyboard_state'][idx1][idx2] == '.':
        context.user_data['keyboard_state'][idx1][idx2] = 'X'
        await update_display(query, context, last_move='X')

        free_ceils = [idx for idx, value in enumerate(np.array(context.user_data['keyboard_state']).flatten()) if value == '.']
        if free_ceils and not won(np.array(context.user_data['keyboard_state']).flatten()):
            random_agent_move = random.choice(free_ceils)
            context.user_data['keyboard_state'][random_agent_move // 3][random_agent_move % 3] = '0'
            await update_display(query, context, last_move='0')


async def update_display(query: Update, context: ContextTypes.DEFAULT_TYPE, last_move: str):
    """Updates display on telegram bot"""
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_reply_markup(reply_markup=reply_markup)

    if won(np.array(context.user_data['keyboard_state']).flatten()):
        await query.edit_message_text(f'{"Crosses (X)" if last_move == 'X' else 'Zeros (0)'} have won the game!',
                                      reply_markup=reply_markup)


def won(fields: list[str]) -> bool:
    """Check if crosses or zeros have won the game"""

    # check horizontal
    for row in range(0, len(fields), 3):
        if all(map(lambda x: x == 'X', fields[row:row+3])) or all(map(lambda x: x == '0', fields[row:row+3])):
            return True

    # check vertical
    for col in range(3):
        if all(map(lambda x: x == 'X', [fields[i] for i in range(col, len(fields), 3)])) or\
                all(map(lambda x: x == '0', [fields[i] for i in range(col, len(fields), 3)])):
            return True

    # check positive diagonal
    if all(map(lambda x: x == 'X', [fields[i] for i in [0, 4, 8]])) or\
            all(map(lambda x: x == '0', [fields[i] for i in [0, 4, 8]])):
        return True

    # check negative diagonal
    if all(map(lambda x: x == 'X', [fields[i] for i in [2, 4, 6]])) or\
            all(map(lambda x: x == '0', [fields[i] for i in [2, 4, 6]])):
        return True

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()