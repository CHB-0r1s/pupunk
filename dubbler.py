import random
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


class FatFingerNotFound(Exception):
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Dubbler(metaclass=Singleton):
    def __init__(self, token):
        self.app = Application.builder().token(token).build()

        self.app.add_handler(
            CommandHandler("dubl", Dubbler.roll_dubl_cmd)
        )  # меня бесит что код дублируется, но я хз как это масштабировать
        self.app.add_handler(CommandHandler("triple", Dubbler.roll_triple_cmd))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, Dubbler.chat_flow)
        )

    def poll(self):
        self.app.run_polling()

    @staticmethod
    def get_dubl():
        return "{:02d}".format(random.randint(0, 99))

    @staticmethod
    def get_triple():
        return "{:03d}".format(random.randint(0, 999))

    @staticmethod
    async def roll_dubl_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Dubbler.get_dubl()
        )

    @staticmethod
    async def roll_triple_cmd(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Dubbler.get_triple()
        )

    @staticmethod
    async def chat_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        text = update.message.text

        # тут тоже можно как то упростить, но я не ебу асинки

        if text.lower().startswith("на дабл"):
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=Dubbler.get_dubl()
            )
            return
        elif text.lower().startswith("на трипл"):
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=Dubbler.get_triple()
            )
            return
        if text.startswith("на "):
            raise FatFingerNotFound(text)
        return
