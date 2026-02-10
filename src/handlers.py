# handler.py

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards import keyboard_after, keyboard_main
from spelling import spell_word

GER, INTER = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
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
   """)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot // Read intro\n"
        "/howtospell - access the spelling context\n"
        "/help - show this info"
    )


async def spelling_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Which language do you prefer?", reply_markup=keyboard_main
    )


async def buttons_control(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_choice = query.data

    if user_choice == "ger":
        context.user_data["lang"] = "German"
        await query.message.reply_text("German chosen.\nPlease enter the word.")
        return GER
    elif user_choice == "int":
        context.user_data["lang"] = "International"
        await query.message.reply_text("International chosen.\nPlease enter the word.")
        return INTER
    elif user_choice == "again":
        await query.message.reply_text(
            "OK, let's try again.\nWhich spelling do you want?",
            reply_markup=keyboard_main,
        )
        # ???
        # return 0
        return ConversationHandler.END
    else:
        await query.message.reply_text(
            "Thank you for the usage! If you need me again, just click /howtospell. (:"
        )
        return ConversationHandler.END


async def handle_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get("lang")
    text = update.message.text
    spelled = spell_word(text, lang)
    await update.message.reply_text(
        f"{text} would be:\n\n{spelled}\n\n\nWhat would you like to do next?",
        reply_markup=keyboard_after,
    )
    return ConversationHandler.END


async def wrong_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("sorry.. the given value is wrong!")
