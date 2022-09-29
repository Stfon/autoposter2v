from pyrogram import Client, filters
import asyncio
import platform
import func
import random
import re

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#  Публикация
async def light(input, output, id):
    m = await app.get_messages(input, id)
    if m:
        if bool(m.media_group_id):
            group = await app.get_media_group(input, id)
            group_text = [x.caption for x in group if x.caption is not None]
            text = group_text[0].markdown

            a = re.search(r"https?", text, flags = re.S)
            b = re.search(r'@[\S]*', text, flags = re.S)

            if a or b:
                await app.copy_media_group(output, input, id, captions = '')
                func.Delete_group_id(id, input, output)
                return 1
            else:

                await app.copy_media_group(output, input, id, captions = '')
                func.Delete_group_id(id, input, output)
                return 1
        else:
            if m.text:
                text = m.text.markdown
                a = re.search(r"https?", text, flags = re.S)
                b = re.search(r'@[\S]*', text, flags = re.S)
                if a or b:


                    func.Delete_msg_id(id, input, output)
                    return 0
                else:

                    await app.copy_message(output, input, id)
                    func.Delete_msg_id(id, input, output)
                    return 1

            elif m.caption:
                text = m.caption.markdown
                a = re.search(r"https?", text, flags = re.S)
                b = re.search(r'@[\S]*', text, flags = re.S)
                if a or b:

                    await app.copy_message(output, input, id, caption = '')
                    func.Delete_msg_id(id, input, output)
                    return 1
                else:

                    await app.copy_message(output, input, id)
                    func.Delete_msg_id(id, input, output)
                    return 1
            else:
                await app.copy_message(output, input, id)
                func.Delete_msg_id(id, input, output)
                return 1
    else:
        return 0


async def hard(input, output, id):

    m = await app.get_messages(input, id)
    if m:
        if bool(m.media_group_id):
            group = await app.get_media_group(m.sender_chat.id, m.id)
            group_text = [x.caption for x in group if x.caption is not None]
            text = group_text[0].markdown

            a = re.search(r"https?", text, flags = re.S)
            b = re.search(r'@[\S]*', text, flags = re.S)

            if a or b:
                func.Delete_group_id(id, input, output)
                return 0
            else:
                await app.copy_media_group(output, input, id)
                func.Delete_group_id(id, input, output)
                return 1

        else:
            if m.text:
                text = m.text.markdown
                a = re.search(r"https?", text, flags = re.S)
                b = re.search(r'@[\S]*', text, flags = re.S)
                if a or b:
                    func.Delete_msg_id(id, input, output)
                    return 0
                else:
                    print("+ сообщение")
                    await app.copy_message(output, input, id)
                    func.Delete_msg_id(id, input, output)
                    return 1

            elif m.caption:
                text = m.caption.markdown
                a = re.search(r"https?", text, flags = re.S)
                b = re.search(r'@[\S]*', text, flags = re.S)
                if a or b:
                    func.Delete_msg_id(id, input, output)
                    return 0

                else:
                    await app.copy_message(output, input, id)
                    func.Delete_msg_id(id, input, output)
                    return 1
            else:
                await app.copy_message(output, input, id)
                func.Delete_msg_id(id, input, output)
                return 1
    else:
        return 0


# async def hard(input, output, id):
#     m = await app.get_messages(input, id)
#
#     if bool(m.)
#
#
# async def light(input, output, id):
#

async def post(input, output, mode):
    async with app:
        messages_id = func.Get_messages_id(input, output)
        group_message_id = func.Get_group_messages_id(input, output)
        rand = random.randint(45, 90)

        ids = group_message_id + messages_id
        ids.sort()
        time = 1 # Время паузы между постами
        tasks = []
        id = ids[0]

        m = await app.get_messages(input, id)

        k = 0
        if mode == "hard":
            while (k == 0):
                k = await hard(input, output, id)
                await asyncio.sleep(1)


        elif mode == 'light':
            while (k == 0):
                k = await light(input, output, id)
                await asyncio.sleep(1)


# Получение каналов
channels = func.Get_channels()

tasks = []

for x, y, z in channels:
    task = post(x, y, z)
    tasks.append(task)

# Создание главного потока
async def main(tasks):
    print(len(tasks))
    await asyncio.gather(*tasks)

# Запуск
if __name__ == '__main__':
    userdir = 'user3'
    user = func.get_api(f'users/{userdir}/user.ini')
    app = Client(user['username'], user['api_id'], user['api_hash'], workdir = f'users/{userdir}')
    print("Клиент запущен")
    loop = asyncio.get_event_loop()
    # app.run(main(tasks))
    loop.run_until_complete(main(tasks))
