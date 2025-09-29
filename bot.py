from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Bot token from environment variable
TOKEN = os.getenv("TOKEN")

async def remove_forward_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg:
        return

    chat = msg.chat
    bot_member = await chat.get_member(context.bot.id)

    # Notify group if bot is not admin
    if not bot_member.can_delete_messages:
        await msg.reply_text(
            "Please make me admin if you want me to process forwarded messages in this group."
        )
        return

    # If the message is forwarded
    if msg.forward_date:
        await context.bot.copy_message(
            chat_id=chat.id,
            from_chat_id=chat.id,
            message_id=msg.message_id,
            caption=msg.caption if msg.caption else None
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & (~filters.StatusUpdate.ALL), remove_forward_tag))
    print("Bot started and listening for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
