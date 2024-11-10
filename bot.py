import discord
from datetime import datetime
import random
import os
import json
from botToken import botToken

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

SENT_MESSAGE_FILE = "./sent_messages.json"
MESSAGE_ARCHIVE_FILE = "./archive.json" 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.display_name == "UB3R-SP4MBOT":
        return

    if message.content.startswith('.test'):
        print(message.author)
        await message.channel.send("Working")
    
    if message.content.startswith('.expose'):
        pass


    if message.content.startswith('.grab-memory'):
        print("==== " + message.author.name + " =============================")
        allowedUsers = [".eek", "kurkon", "luddelino", "popapea", "zyrbz", "sandin9", "ejctom", "gurkface"]
        archiveFile = get_channel_archive_filename(message.channel.id)
        sentMessagesFile = get_channel_sent_filename(message.channel.id)

        messageIds = get_all_messages(archiveFile)
        if len(messageIds) == 0:
            before = datetime(2017, 10, 20)
            async for x in message.channel.history(limit=None, before=before):
                store_message(x.id, archiveFile)
                messageIds.append(x.id)
        
        if len(messageIds) == 0:
            await message.channel.send("No messages are old enough")
            return

        random_index = random.randint(0, len(messageIds) - 1)
        id = messageIds[random_index]

        sentMessagesIds = get_all_messages(sentMessagesFile)

        msg = await message.channel.fetch_message(id)

        nonAllowedMessageIds = sentMessagesIds

        i = 0
        #Only try 10 times
        for i in range(0, 10):
            while id in nonAllowedMessageIds:
                messageIds.pop(random_index)
                random_index = random.randint(0, len(messageIds) - 1)
                print("Try new index: " + str(random_index))
                id = messageIds[random_index]

            msg = await message.channel.fetch_message(id)
            print("New message, id: " + str(msg.id))
            print("Author: " + msg.author.name)

            #Also allow to find messages of the person who runs the command
            if msg.author.name == message.author.name:
                break
            #Prevent @-ing randos
            if msg.author.name in allowedUsers:
                break
            if i >= 10:
                break

            nonAllowedMessageIds.append(msg.id)
            print("\n")

        print("\n")
        if i >= 9:
            await message.channel.send("Seems hard to find a suitable message...")
            return

        reference = discord.MessageReference.from_message(msg)

        await msg.channel.send(str(msg.created_at.strftime('%Y-%m-%d %H:%M')) + "\n\n" + msg.content, reference=reference, files=[await x.to_file() for x in msg.attachments])
        store_message(msg.id, sentMessagesFile)




def create_file_if_not_exists(file_path: str):
    #Create directory
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Create file
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

def store_message(message: str, file: str):
    create_file_if_not_exists(file)   

    with open(file, 'r') as f:
        messages = json.load(f)
    
    messages.append(message)
    
    with open(file, 'w') as f:
        json.dump(messages, f)

def id_exists_in_file(message: str, file: str) -> bool:
    create_file_if_not_exists(file)

    with open(file, 'r') as f:
        messages = json.load(f)
    
    return message in messages

def get_all_messages(file: str) -> list:
    create_file_if_not_exists(file)  # Ensure the file exists
    
    # Read the current list from the JSON file
    with open(file, 'r') as f:
        messages = json.load(f)
    
    return messages

def get_channel_archive_filename(id: int):
    return "./Archives/" + str(id) + ".json"

def get_channel_sent_filename(id: int):
    return "./SentMessages/" + str(id) + ".json"


client.run(botToken)