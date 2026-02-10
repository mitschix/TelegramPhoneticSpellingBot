#!/usr/bin/env python3
#
# Title: Telegram Bot Spelling Alphabet
#
# Desc: Telegram bot that returns the spelling alphabet to a given string
#
# Requires:
#   + token: A telegram token from the @BotFather


from handlers import (
    GER,
    INTER,
    buttons_control,
    handle_words,
    help_command,
    spelling_start,
    start,
    wrong_input,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from tel_tokens import token


def main() -> None:
    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CallbackQueryHandler(buttons_control)],
        states={
            GER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_words)],
            INTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_words)],
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, wrong_input)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("howtospell", spelling_start))
    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
    print("User forced me to stop... i am sorrey ):")
