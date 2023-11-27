import os
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import BadRequest
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BANHAMMER_TOKEN')
ALLOWED_USER_IDS = [int(user_id) for user_id in os.getenv('BANHAMMER_ALLOWED_USER_IDS', '').split(',')]
HELP_TEXT = '''/ban [time] [message]\ntime {1m; 2h; 3d; 4w; always}\nmessage {спам и оскорбления; политика; иди нахуй}'''


async def get_id(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text('Иди нахуй')
        return

    await update.message.reply_text(f'{update.message.from_user.id}')


async def ban(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text('Иди нахуй')
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(HELP_TEXT)
        return

    if len(context.args) < 2:
        await update.message.reply_text(HELP_TEXT)
        return

    user = update.message.reply_to_message.from_user
    user_id = user.id

    duration_str, *reason = context.args
    reason = ' '.join(reason)

    if duration_str[-1] == 'm':
        duration = int(duration_str[:-1])
        unit = 'минуту' if duration == 1 else 'минуты' if 1 < duration < 5 else 'минут'
        end_time = datetime.now() + timedelta(minutes=duration)
    elif duration_str[-1] == 'h':
        duration = int(duration_str[:-1])
        unit = 'час' if duration == 1 else 'часа' if 1 < duration < 5 else 'часов'
        end_time = datetime.now() + timedelta(hours=duration)
    elif duration_str[-1] == 'd':
        duration = int(duration_str[:-1])
        unit = 'день' if duration == 1 else 'дня' if 1 < duration < 5 else 'дней'
        end_time = datetime.now() + timedelta(days=duration)
    elif duration_str[-1] == 'w':
        duration = int(duration_str[:-1])
        unit = 'неделю' if duration == 1 else 'недели' if 1 < duration < 5 else 'недель'
        end_time = datetime.now() + timedelta(weeks=duration)
    elif duration_str == "always":
        duration = None
        unit = ''
        end_time = None
    else:
        await update.message.reply_text(HELP_TEXT)
        return

    try:
        await context.bot.restrict_chat_member(update.message.chat_id, user_id,
                                               permissions=ChatPermissions(
                                                   can_send_messages=False,
                                                   can_send_polls=False,
                                                   can_send_other_messages=False,
                                                   can_add_web_page_previews=False,
                                                   can_invite_users=False,
                                                   can_send_audios=False,
                                                   can_send_documents=False,
                                                   can_send_photos=False,
                                                   can_send_videos=False,
                                                   can_send_video_notes=False,
                                                   can_send_voice_notes=False,
                                               ),
                                               until_date=end_time)

        mention_html = user.mention_html()
        duration_text = f'на {duration} {unit}' if duration is not None else 'навсегда'
        await update.message.reply_to_message.reply_text(f'Пользователь {mention_html} забанен {duration_text} по причине {reason}', parse_mode='HTML')
        return

    except BadRequest as e:
        if e.message == "Not enough rights to restrict/unrestrict chat member":
            await update.message.reply_text("У бота недостаточно прав")
            return
        else:
            await update.message.reply_text(f"Неизвестная ошибка: {e}")
            return
    except Exception as e:
        await update.message.reply_text(f"Неизвестная ошибка: {e}")
        return


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("ban", ban))

    application.run_polling()


if __name__ == '__main__':
    main()
