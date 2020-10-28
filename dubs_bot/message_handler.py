import sys
from random import choice, randint

from dubs_bot.settings import Settings

owner_id = int(Settings().get_config("owner_id"))

dubs_dict = {
    2: ["CHECK 'EM", "nice dubs!!!", "2 same number", "top dubs!!", "in dubs we trust!!"],
    3: ["CHECK 'EM!!!", "sweet trips", "TRIPS!!!", "oh baby a trips!!", "top trips!!!"],
    4: ["sexy quads!!", "HOLY COW QUADS!!!", "SWEET QUADS FREN!!!"],
    5: ["CHECKIN' QUINTS!!!", "QUINTS WOW!!!", "Sweet quints fren!!"],
    6: ["SEX!!", "CHECKIN' SEXTUPLES!!!!!!", "SIX SAME NUMBER WOW!!!"],
    7: ["CHECKIN' SEPTUPLES!!!", "7 SAME NUMBE HOLY MOLY!!!", "NICE SEPTS FREN!!!"],
    8: ["HOLY SHIT 8 SAME NUMBER", "OCTUPLES CHECKED!!!!"],
    9: ["HOW"],
    10: ["WHAT THE FUCK!?!?!"]
}

special_dubs_dict = {
    666: ["absolutely demonic", "I dont like those numbers"],
    777: ["holy trips!!", "blessed trips"],
    555: ["angelic trips!!"],
    333: ["three threes"],
    22: ["two twos"],
    4444: ["4 by 4", "four fours"]
}


async def handle_message(event):
    if event.sender_id == owner_id and event.raw_text == "c.shutdown":
        await event.reply("Shutting down...")
        await event.client.disconnect()
        sys.exit()

    digit_result = check_digits(str(event.id), str(event.chat.id))

    if digit_result:
        await event.respond(digit_result)


def check_digits(message_id: str, chat_id: str):
    last_digit = message_id[-1]
    digit_count = 1
    digit_place = -2
    digit_str = last_digit

    while message_id[digit_place] == last_digit:
        digit_str += last_digit
        digit_count += 1
        digit_place -= 1

    if digit_count == 1:
        return

    if digit_count in (2, 3):
        if randint(1, 100) < 130 / digit_count:
            return

    if int(digit_str) in special_dubs_dict.keys():
        return f"[>>{message_id}](https://t.me/c/{chat_id}/{message_id})\n{choice(special_dubs_dict.get(int(digit_str)))}"

    return f"[>>{message_id}](https://t.me/c/{chat_id}/{message_id})\n{choice(dubs_dict.get(digit_count))}"
