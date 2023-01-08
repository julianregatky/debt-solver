import logging
import os
import re
from typing import Dict, List

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from debt_solver import DebtSolver

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def parse_list(lst: List[str]) -> Dict[str, int]:
    """
    Parse list of strings in the format '[name] [amount]' into a dictionary.
    
    Parameters:
        lst (List[str]): List of strings to parse
    
    Returns:
        dictionary (Dict[str, int]): Dictionary with keys as names and values as amounts
    """
    pattern = r"(.+)\s(\d+)"
    dictionary = {}
    for item in lst:
        match = re.match(pattern, item)
        if match:
            name = match.group(1)
            number = int(match.group(2))
            dictionary[name] = number
    return dictionary

def start(update, context):
    """
    Sends a message to the user explaining how to use the bot.
    
    Args:
        update (obj): The update object, which contains information about the
            user's message.
        context (obj): The context object, which contains information about the
            current state of the bot.
    """
    # Send a message to the user
    update.message.reply_text('Send me a single message with each member on a new line, following the format \[name]\[space]\[amount]. Those who did not pay, add them with 0 in amount.')

def message(update, context):
    """
    Parses the user's message and sends a message with the results of the
    debt calculation.
    
    Args:
        update (obj): The update object, which contains information about the
            user's message.
        context (obj): The context object, which contains information about the
            current state of the bot.
    """
    # Parse the expenses from the message
    expenses = parse_list(update.message.text.split('\n'))
    
    # Check if the expenses could be parsed
    if len(expenses) > 0:
        # Solve the debts
        result = DebtSolver(expenses).solve()
        
        # Send the result to the user
        update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
    else:
        # Inform the user if the expenses couldn't be parsed
        update.message.reply_text("Couldn't parse the expenses provided.")

def main():
    """Starts the bot and sets up handlers for commands and messages."""

    # Updater with bot's token
    updater = Updater(os.environ.get("BOT_TOKEN"), use_context=True)

    # Dispatcher to register handlers
    dp = updater.dispatcher

    # On commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    
    # On noncommand i.e message - process message
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start Polling
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()