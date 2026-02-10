#!/usr/bin/env python3
#
# Title: Telegram Bot Spelling Alphabet
#
# Desc: Telegram bot that returns the spelling alphabet to a given string
#
# Requires:
#   + token: A telegram token from the @BotFather


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Updater,
    filters,
)

from tel_tokens import token

# set conversation handler vars
GER, INTER = range(2)
LANG: dict = {}

# setting up the inline keyboards
keyboard_main = [
    [InlineKeyboardButton("German", callback_data="ger")],
    [InlineKeyboardButton("International", callback_data="int")],
]
keyboard_after = [
    [InlineKeyboardButton("Spell again", callback_data="again")],
    [InlineKeyboardButton("End", callback_data="end")],
]


def get_mapping(word: str, lang: str) -> str:
    german_spelling = {
        "A": "Anton",
        "B": "Berta",
        "C": "Cäsar",
        "D": "Dora",
        "E": "Emil",
        "F": "Friedrich",
        "G": "Gustav",
        "H": "Heinrich",
        "I": "Ida",
        "J": "Julius",
        "K": "Kaufmann",
        "L": "Ludwig",
        "M": "Martha",
        "N": "Nordpol",
        "O": "Otto",
        "P": "Paula",
        "Q": "Quelle",
        "R": "Richard",
        "S": "Samuel",
        "SCH": "Schule",
        "T": "Theodor",
        "U": "Ulrich",
        "V": "Viktor",
        "W": "Wilhelm",
        "X": "Xanthippe",
        "Y": "Ypsilon",
        "Z": "Zacharias",
        "Ä": "Ärger",
        "Ö": "Ökonom",
        "Ü": "Übermut",
        "0": "Null",
        "1": "Eins",
        "2": "Zwei",
        "3": "Drei",
        "4": "Vier",
        "5": "Fünf",
        "6": "Sechs",
        "7": "Sieben",
        "8": "Acht",
        "9": "Neun",
        " ": "Leerzeichen",
        ".": "Punkt",
        ",": "komma",
        ";": "Semikolon",
        ":": "DoppelPunkt",
        "?": "Fragezeichen",
        "!": "Ausrufezeichen",
        "@": "At-Zeichen",
        "&": "Und-Zeichen",
        '"': "Anführungszeichen",
        "'": "Apostroph",
        "-": "Bindestrich",
        "/": "Schrägstrich",
        "\\": "Umgekehrter-Schrägstrich",
        "(": "Runde-Klammer-links",
        ")": "Runde-Klammer-rechts",
        "[": "Eckige-Klammer-links",
        "]": "Eckige-Klammer-rechts",
        "{": "Geschweifte-Klammer-links",
        "}": "Geschweifte-Klammer-rechts",
        "<": "Kleiner-als-Zeichen",
        ">": "Größer-als-Zeichen",
        "|": "Senkrechter-Strich",
        "°": "Gradzeichen",
        "*": "Sternchen",
        "+": "Pluszeichen",
        "=": "Gleichheitszeichen",
        "#": "Rautenzeichen",
        "§": "Paragraphenzeichen",
        "$": "Dollarzeichen",
        "€": "Euro-Zeichen",
        "~": "Tilde",
        "_": "Unterstrich",
        "%": "Prozentzeichen",
        "^": "Zirkumflex",
    }

    inter_spelling = {
        "A": "Alfa",
        "B": "Bravo",
        "C": "Charlie",
        "D": "Delta",
        "E": "Echo",
        "F": "Foxtrot",
        "G": "Golf",
        "H": "Hotel",
        "I": "India",
        "J": "Juliett",
        "K": "Kilo",
        "L": "Lima",
        "M": "Mike",
        "N": "November",
        "O": "Oscar",
        "P": "Papa",
        "Q": "Quebec",
        "R": "Romeo",
        "S": "Sierra",
        "T": "Tango",
        "U": "Uniform",
        "V": "Victor",
        "W": "Whiskey",
        "X": "X-ray",
        "Y": "Yankee",
        "Z": "Zulu",
        "0": "Zero",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        " ": "Space",
        ".": "Dot",
        ",": "Comma",
        ";": "Semicolon",
        ":": "Colon",
        "?": "Question-Mark",
        "!": "Exclamation-Mark",
        "@": "At-Sign",
        "&": "Ampersand",
        '"': "Double-Quotation-Mark",
        "'": "Single-Quotation-Mark",
        "-": "Minus-Sign",
        "/": "Forward-Slash",
        "\\": "Backslash",
        "(": "Left-Round-Bracket",
        ")": "Right-Round-Bracket",
        "[": "Left-Square-Bracket",
        "]": "Right-Square Bracket",
        "{": "Left-Curly-Bracket",
        "}": "Right-Curly-Bracket",
        "<": "Less-Than-Sign",
        ">": "Greater-Than-Sign",
        "|": "Pipe",
        "°": "Degree-Symbol",
        "*": "Star",
        "+": "Plus-Sign",
        "=": "Equal-Sign",
        "#": "Hash",
        "§": "Section-Sign",
        "$": "Dollar-Sign",
        "€": "Euro-Sign",
        "~": "Tilde",
        "_": "Underscore",
        "%": "Percent-Sign",
        "^": "Caret",
    }
    spelling_dict = {"German": german_spelling, "Inter": inter_spelling}

    spell_words = []
    for char in word:
        spell_words.append(spelling_dict[lang].get(char.upper(), "??"))

    outstring = " ".join(spell_words)

    return outstring


# handler functions for bot
# start function called with /start
def start(update, context) -> None:
    start_message = """
Welcome to my alphabetic spelling bot!

This bot is used to transform given word(s) into the international or german \
spelling alphabet.

Try it out using /howtospell.

There are two options:
    + ICAO/ITU/NATO Spelling Alphabet (International)
    + DIN 5009 Spelling Alphabet (German)

If you have any ideas, requests or bugs, don´t hasitate to contact me!
Thx for using my bot! Hope you will enjoy it!
- @mitschix
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=start_message)


# show different menus
def spelling_start(update, context) -> None:
    reply_markup = InlineKeyboardMarkup(keyboard_main)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Which language do you prefer?",
        reply_markup=reply_markup,
    )


def handle_words(update, context) -> int:
    user = update.message.chat_id
    given_string = update.message.text
    output = get_mapping(given_string, LANG[user])
    msg = "{} would be:\n\n{}\n\n\nWhat would you like to do next?".format(
        given_string, output
    )
    context.bot.send_message(
        chat_id=user, text=msg, reply_markup=InlineKeyboardMarkup(keyboard_after)
    )
    return ConversationHandler.END


def wrong_conv(bot, update, user_data) -> None:
    bot.send_message(
        chat_id=update.message.chat_id, text="sorry.. the given value is wrong!"
    )


def buttons_control(update, context) -> int:
    global LANG
    user = update.callback_query.message.chat_id
    option = update.callback_query.data

    if option == "ger":
        LANG[user] = "German"
        msg = "German chosen"
        msg += "\nPlease enter the word you would like to spell."
        context.bot.send_message(chat_id=user, text=msg)
        return GER
    elif option == "int":
        LANG[user] = "Inter"
        msg = "International chosen"
        msg += "\nPlease enter the word you would like to spell."
        context.bot.send_message(chat_id=user, text=msg)
        return INTER
    elif option == "again":
        msg = "OK, lets try again.\n\nWhich spelling do you want to choose?"
        context.bot.send_message(
            chat_id=user, text=msg, reply_markup=InlineKeyboardMarkup(keyboard_main)
        )
        return 0
    else:
        msg = (
            "Thank you for the usage! If you need me again, just click /howtospell. (:"
        )
        context.bot.send_message(chat_id=user, text=msg)
        return ConversationHandler.END


def help_output(update, context) -> None:
    help_string = """
/start                          - Start the bot // Read intro
/howtospell                     - access the spelling context
/help                           - show this info
"""
    context.bot.send_message(chat_id=update.message.chat_id, text=help_string)


def main() -> None:
    """
    set variables and setup bot
    """

    # updater = Updater(token=tok, use_context=True)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # handler
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help_output)
    main_handler = CommandHandler("howtospell", spelling_start)
    button_handler = CallbackQueryHandler(buttons_control)

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[button_handler],
        states={
            GER: [MessageHandler(filters.text, handle_words)],
            INTER: [MessageHandler(filters.text, handle_words)],
        },
        fallbacks=[MessageHandler(filters.text, wrong_conv)],
    )

    # add handler to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(main_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(conv_handler)

    # start the bot
    print("starting all_finance_bot")
    updater.start_polling()
    # run the bot until it receives Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()
    print("User forced me to stop... i am sorrey ):")
