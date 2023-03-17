import os
import discord
from utils.constants import *
from dotenv import load_dotenv
from loggingConfig import configure_logging, logging


load_dotenv()
configure_logging()

token = os.getenv('discordBotToken')
intents = discord.Intents.default()

# inililzing discord client with default intents
client = discord.Client(intents=intents, logging=logging)

# Global message variable to be set externally and bot to be triggered
message = ""
channelName = DISCORD_APPLICATION_CHANNEL


# event triggered when the bot is ready
@client.event
async def on_ready():
    logging.info(f"Sending message to channel {channelName}")
    # find the channel with the channel ID
    channel = client.get_channel(int(os.getenv(channelName)))
    await channel.send(message)  # send the message from the global variable
    await client.close()  # close the client to stop the client blocking code


# method to be executed from an external file
def botRun(content="", channel=DISCORD_APPLICATION_CHANNEL):
    global message, channelName
    message = content
    channelName = channel
    client.run(token)
