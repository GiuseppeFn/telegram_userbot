from telethon import TelegramClient, events, errors
from os import environ
import asyncio
import requests
from math import ceil

admin=environ["TELEGRAM_ADMIN1"]
api_id=environ["TELEGRAM_API_ID"]
api_hash=environ["TELEGRAM_API_HASH"]

moons=['🌒ㅤ','🌓ㅤ','🌔ㅤ','🌕ㅤ','🌖ㅤ','🌗ㅤ','🌘ㅤ','🌑ㅤ']
clocks=['🕐ㅤ','🕑ㅤ','🕒ㅤ','🕓ㅤ','🕔ㅤ','🕕ㅤ','🕖ㅤ','🕗ㅤ','🕘ㅤ','🕙ㅤ','🕚ㅤ','🕛ㅤ']
wiwos=['🔴🔴🔴🔴🔴\n🔴🔴🔴🔴🔴\n🔴🔴🔴🔴🔴\n🔴🔴🔴🔴🔴\n🔴🔴🔴🔴🔴','🔵🔵🔵🔵🔵\n🔵🔵🔵🔵🔵\n🔵🔵🔵🔵🔵\n🔵🔵🔵🔵🔵\n🔵🔵🔵🔵🔵']


client=TelegramClient('./name_session.session', api_id, api_hash)

async def dispatch(message, array, times=1):
    for _ in range(0,times):
        for i in array:
            try:
                await message.edit(i)
            except errors.MessageNotModifiedError:
                pass
            await asyncio.sleep(0.1)

async def moon(message):
    await dispatch(message, moons, 2)

async def clock(message):
    await dispatch(message, clocks, 2)

async def wiwo(message):
    await dispatch(message, wiwos, 10)

async def purge(event):
  reply = await event.get_reply_message()
  temp = [event.id]
  for msg in await client.get_messages(event.input_chat, min_id=reply.id-1, max_id=event.id):
    temp.append(msg.id)
  await client.delete_messages(event.input_chat, temp)

async def haste(e):
    if e.is_reply and (await e.get_reply_message()).message:
        link=requests.post("https://hastebin.com/documents", data=((await e.get_reply_message()).text).encode('utf-8'), headers={'Content-type': 'text/plain; charset=utf-8'}).json()['key']
        if e.sender_id == admin:
            await e.edit("[Versione hastebin.com](https://hastebin.com/{})".format(link))
        else:
            await e.reply("[Versione hastebin.com](https://hastebin.com/{})".format(link), link_preview=False)


async def spam(e):
    await e.delete()
    times=int(e.text.split(" ")[1])
    text=" ".join(e.text.split(" ")[2:])
    for _ in range(times):
        await e.respond(text)

async def spamplus(e):
    await e.delete()
    times=int(e.text.split(" ")[1])
    text=" ".join(e.text.split(" ")[2:])
    for i in range(0,times):
        await e.respond(text+(text[-1]*i))
    for i in reversed(range(0, times)):
        await e.respond(text+(text[-1]*i))

async def save(e):
    await e.delete()
    if e.is_reply:
        msg = (await e.get_reply_message())
        await client.send_message('me',msg)

async def count(e):
    await e.delete()
    splitted = e.text.split(" ")
    how_many=int(splitted[1])
    joiner = " " if len(splitted) == 2 else "\n" if len(splitted) == 3 else 0
    if joiner == 0:
        for x in range(how_many):
            await e.respond(str(x + 1))
    else:
        await message_splitter(joiner.join([str(x + 1) for x in range(how_many)]), e)

MAX_LEN=4096
async def message_splitter(msg: str, e):
    if len(msg) < MAX_LEN:
        await e.respond(msg)
        return
    for x in range(1,ceil(len(msg)/MAX_LEN)):
        await e.respond(msg[MAX_LEN*(x-1):MAX_LEN*x])
        await asyncio.sleep(1)


with client:
    client.add_event_handler(moon, events.NewMessage(from_users=admin, pattern=';moon'))
    client.add_event_handler(clock, events.NewMessage(from_users=admin, pattern=';clock'))
    client.add_event_handler(wiwo, events.NewMessage(from_users=admin, pattern=';wiwo'))
    client.add_event_handler(purge, events.NewMessage(from_users=admin, pattern=';purge'))
    client.add_event_handler(haste, events.NewMessage(pattern=';haste'))
    client.add_event_handler(spam, events.NewMessage(from_users=admin, pattern=';spam .*'))
    client.add_event_handler(spamplus, events.NewMessage(from_users=admin, pattern=';spamp .*'))
    client.add_event_handler(save, events.NewMessage(from_users=admin, pattern=';save'))
    client.add_event_handler(count, events.NewMessage(from_users=admin, pattern=';count .*'))
    client.run_until_disconnected()
