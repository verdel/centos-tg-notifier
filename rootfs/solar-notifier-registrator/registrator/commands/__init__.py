import telegram
from registrator.data.models import User
import logging


def start(bot, update, args):
    error = False
    bot.sendChatAction(
        action=telegram.ChatAction.TYPING,
        chat_id=update.message.chat_id
    )

    if args:
        authtoken = args[0]
        try:
            user = User.objects(token=authtoken).first()
        except Exception:
            logging.error('DB connection refused')
            user = None
            error = True

        if user:
            if user.chatId != update.message.chat_id:
                user.update(
                    **{
                        'telegramNick': update.message.from_user.username,
                        'chatId': update.message.chat_id
                    }
                )
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='You register in SolarNotifier!'
                )

            else:
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='You already registered in SolarNotifier!'
                )

        else:
            if error:
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='Temporarily unavailable. Please try later.'
                )

            else:
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='Wrong Auth Token!'
                )
    else:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Please provide auth token!'
        )


def stop(bot, update):
    error = False
    bot.sendChatAction(
        action=telegram.ChatAction.TYPING,
        chat_id=update.message.chat_id
    )

    try:
        user = User.objects(chatId=update.message.chat_id).first()

    except Exception:
        logging.error('DB connection refused')
        user = None
        error = True

    if user:
        user.update(unset__chatId='', unset__telegramNick='')
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='You unregister from SolarNotifier!'
        )

    else:
        if error:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text='Temporarily unavailable. Please try later.'
            )

        else:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text='You are not register in SolarNotifier!'
            )


def unknown(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Sorry, I didn\'t understand that command.'
    )
