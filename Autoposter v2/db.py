from pyrogram import Client, filters
import asyncio
import platform
import func
import random
import re
import sqlite3

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# input, output = func.get_channels('channels.ini')
# Chanell = (input, output)
# Channels = [(input1, output1), (input2, output2)]

async def add_ids(inp, out, filter_msg):
    ids = func.Get_messages_id(inp, out)
    media_group_ids = func.Get_media_group_id(inp, out)
    async with app:
        async for m in app.get_chat_history(inp):
            if bool(m.media_group_id): #Обработка медиа групп сообщений
                group_id = m.media_group_id
                id = m.id
                if m.caption is not None and group_id not in media_group_ids:
                    if filter_msg(m.caption.markdown):
                        try:
                            func.Insert_group_msg(id, group_id, inp, out)
                        except sqlite3.IntegrityError:
                            print(inp, out)
                            continue
                    else:
                        continue
                else:
                    try:
                        func.Insert_group_msg(id, group_id, inp, out)
                    except sqlite3.IntegrityError:
                        continue

            elif bool(m.text): #Обработка текстовых сообщений
                id = m.id
                if filter_msg(m.text.markdown) and id not in ids:
                    func.Insert_msg(id, inp, out)
                else:
                    continue

            elif bool(m.photo): #Обработка сообщений с фото
                id = m.id
                if m.caption:
                    if filter_msg(m.caption.markdown) and id not in ids:
                        func.Insert_msg(id, inp, out)
                    else:
                        continue
                else:
                    try:
                        func.Insert_msg(id, inp, out)
                    except sqlite3.IntegrityError:
                        continue
            elif bool(m.video):
                id = m.id
                if m.caption:
                    if filter_msg(m.caption.markdown) and id not in ids:
                        func.Insert_msg(id, inp, out)
                    else:
                        continue
                else:
                    try:
                        func.Insert_msg(id, inp, out)
                    except sqlite3.IntegrityError:
                        continue

channels = func.Get_channels()

# channels = [(inp, out), (), () .......]
tasks = []

for x, y, z in channels:
    task = add_ids(x, y, func.filter2)
    tasks.append(task)


async def main():

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    userdir = "user3"
    user = func.get_api(f'users/{userdir}/user.ini')

    app = Client(user['username'], user['api_id'], user['api_hash'], workdir = f'users/{userdir}')
    print('Клиент запущен')
    app.run(main())
