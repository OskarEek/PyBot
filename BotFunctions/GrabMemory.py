from datetime import datetime
import random
import discord

from Services import FileService
from Models.MessageData import MessageData

async def grab_memory(message):
    print("==== " + message.author.name + " =============================")
    allowedUsers = [".eek", "kurkon", "luddelino", "popapea", "zyrbz", "sandin9", "ejctom", "gurkface"]
    archiveFile = FileService.get_archive_filename(message.channel.id, message.created_at)
    sentMessagesFile = FileService.get_channel_sent_filename(message.channel.id)

    numberOfFiles = FileService.count_items_in_folder(archiveFile)
    if numberOfFiles == 0:
        before = datetime(2017, 10, 20)
        async for x in message.channel.history(limit=None, before=before):
            messageData = MessageData(x.id, x.author.id, x.author.name, x.channel.id, len(x.attachments) > 0, x.created_at)
            FileService.store_archive_message(messageData, FileService.get_archive_filename(x.channel.id, x.created_at))
        
    numberOfFiles = FileService.count_items_in_folder(archiveFile)
    if numberOfFiles == 0:
        await message.channel.send("No messages are old enough")
        return

    random_file_index = random.randint(0, numberOfFiles-1)
    random_file = FileService.get_file_by_index(random_file_index, archiveFile)


    messages = FileService.get_archive_messages(random_file)
    random_message_index = random.randint(0, len(messages) - 1)

    dataMsg = messages[random_message_index]

    sentMessagesIds = FileService.get_sent_messagesIds(sentMessagesFile)
    nonAllowedMessageIds = sentMessagesIds

    i = 0
    #Only try 10 times
    for i in range(0, 10):
        while dataMsg.id in nonAllowedMessageIds:
            messages.pop(random_message_index)
            random_index = random.randint(0, len(messages) - 1)
            print("Try new index: " + str(random_message_index))
            dataMsg = messages[random_message_index]

        print("New message, id: " + str(dataMsg.id))
        print("Author: " + dataMsg.authorName)

        #Also allow to find messages of the person who runs the command
        if dataMsg.authorName == message.author.name:
            break
        #Prevent @-ing randos
        if dataMsg.authorName in allowedUsers:
            break
        if i >= 10:
            break

        nonAllowedMessageIds.append(dataMsg.id)
        print("\n")

    print("\n")
    if i >= 9:
        await message.channel.send("Seems hard to find a suitable message...")
        return

    msg = await message.channel.fetch_message(dataMsg.id)
    reference = discord.MessageReference.from_message(msg)

    await msg.channel.send(str(msg.created_at.strftime('%Y-%m-%d %H:%M')) + "\n\n" + msg.content, reference=reference, files=[await x.to_file() for x in msg.attachments])
    FileService.store_sent_messageId(msg.id, sentMessagesFile)