import requests
from bs4 import BeautifulSoup
import discord
import asyncio

# Discord bot token
DISCORD_TOKEN = 'OTkzNTM4NTcyODY5MTc3MzQ0.G-8TBW.z9fNSqz8v2lf_c1D1kM8O_aobRI8P3gOmIwz8k'

# Twitter account URL
TWITTER_URL = 'https://twitter.com/NovaNationReal'

# Discord channel ID
CHANNEL_ID = 1082537960966209599

# Authenticate with Discord
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')

async def check_tweets():
    while True:
        try:
            tweet_text = get_latest_tweet()
            if tweet_text:
                channel = client.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(f'New tweet: {tweet_text}')
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(300)  # Check every 5 minutes

def get_latest_tweet():
    response = requests.get(TWITTER_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tweet_element = soup.find('div', class_='css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
        if tweet_element:
            return tweet_element.text.strip()
    return None

if __name__ == "__main__":
    client.loop.create_task(check_tweets())
    client.run(DISCORD_TOKEN)
