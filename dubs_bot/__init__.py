import sys
from logging import INFO, basicConfig, getLogger

from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.network.connection.tcpabridged import \
    ConnectionTcpAbridged as CTA

from dubs_bot.message_handler import handle_message
from dubs_bot.settings import Settings


class DubsCheckerBot:
    settings = Settings()

    def __init__(self):
        basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)
        self.logger = getLogger(__name__)
        self._start_client()

    def run_until_done(self):
        self.logger.info("Client successfully started.")
        self.client.add_event_handler(handle_message, events.NewMessage(incoming=True, func=lambda e: not e.is_private))
        self.logger.info("Dubs checker successfully started.")
        self.client.run_until_disconnected()

    def _check_config(self):
        api_key = self.settings.get_config("api_key")
        api_hash = self.settings.get_config("api_hash")
        bot_token = self.settings.get_config("bot_token")

        while not api_key:
            api_key = input("Enter your API key: ")

        self.settings.set_config("api_key", api_key)

        while not api_hash:
            api_hash = input("Enter your API hash: ")

        self.settings.set_config("api_hash", api_hash)

        while not bot_token:
            bot_token = input("Enter your bot token: ")

        self.settings.set_config("bot_token", bot_token)

        return api_key, api_hash, bot_token

    def _start_client(self):
        api_key, api_hash, bot_token = self._check_config()
        self.client = TelegramClient("dubs_bot", api_key, api_hash, connection=CTA)

        try:
            self.client.start(bot_token=bot_token)
        except PhoneNumberInvalidError:
            print("The bot token provided is invalid, exiting.")
            sys.exit(2)

    async def stop_client(self):
        await self.client.disconnect()


dubs_bot = DubsCheckerBot()

try:
    dubs_bot.run_until_done()
except:
    dubs_bot.client.loop.run_until_complete(dubs_bot.stop_client())
