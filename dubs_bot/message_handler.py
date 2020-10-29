import sys
from random import choice, randint

from telethon import events

from .check_strings import (dubs_dict, not_dubs_but_funny_dict,
                            special_dubs_dict)


class MessageHandler:
    def __init__(self, client, settings):
        self.client = client
        self.settings = settings

        bot_username = client.loop.run_until_complete(client.get_me()).username
        owner_id = int(settings.get_config("owner_id"))
        template = "(?is)^{0}(?: |$|@{1}(?: |$))(.*)"

        client.add_event_handler(self.dubs_check, events.NewMessage(incoming=True, func=lambda e: not e.is_private))
        client.add_event_handler(self.set_min_get, events.NewMessage(incoming=True, pattern=template.format("/minget", bot_username), func=lambda e: not e.is_private))
        client.add_event_handler(self.shutdown, events.NewMessage(incoming=True, pattern=template.format("/nodubs", bot_username), func=lambda e: e.sender_id == owner_id))

    async def dubs_check(self, event):
        digit_result = self.check_digits(str(event.id), str(event.chat.id))

        if digit_result:
            await event.respond(digit_result)

    async def set_min_get(self, event):
        if not (await event.client.get_permissions(event.chat, event.sender_id)).is_admin:
            await event.reply("That command requires admin permissions!")
            return

        if not event.pattern_match.groups()[-1]:
            await event.reply(f"Syntax: /minget <number>\nCurrent config: {self.settings.get_config(f'{event.chat.id}_minget', 2)}")
            return

        try:
            newminget = int(event.pattern_match.groups()[-1])

            if newminget <= 1 or newminget >= 8:
                raise Exception
        except:
            await event.reply("Invalid value, expected an integer between 1 and 8!")
            return

        self.settings.set_config(f'{event.chat.id}_minget', newminget)
        await event.reply(f"Successfully set this groups min get to {newminget}!")

    async def shutdown(self, event):
        await event.reply("Shutting down...")
        await self.client.disconnect()
        sys.exit()

    def check_digits(self, message_id: str, chat_id: str):
        last_digit = message_id[-1]
        digit_place = -2
        digit_str = last_digit

        try:
            while message_id[digit_place] == last_digit and len(digit_str) + 1 in dubs_dict.keys():
                digit_str += last_digit
                digit_place -= 1
        except IndexError:
            pass

        for key, value in not_dubs_but_funny_dict.items():
            if message_id.endswith(str(key)):
                if randint(1, 100) > 25:
                    return f"[>>{message_id}](https://t.me/c/{chat_id}/{message_id})\n{choice(value)}"

        if len(digit_str) == 1 or len(digit_str) < int(self.settings.get_config(f"{chat_id}_minget", 2)):
            return

        if len(digit_str) in (2, 3):
            if randint(1, 100) < 130 / len(digit_str):
                return

        if int(digit_str) in special_dubs_dict.keys():
            return f"[>>{message_id}](https://t.me/c/{chat_id}/{message_id})\n{choice(special_dubs_dict.get(int(digit_str)))}"

        return f"[>>{message_id}](https://t.me/c/{chat_id}/{message_id})\n{choice(dubs_dict.get(len(digit_str)))}"
