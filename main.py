import discord
import re
import os

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-f"):
        raw_text = message.content[2:].strip()
        names = []
        lines = raw_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # This regex handles MMRK, standard lists, and wishlists with emojis
            match = re.search(r"^#\d+\s+-\s+(.*?)(?:\s+\d[\d,]*\s+ka|$)|^(.*?)(?:\s+[❌✅🔐⭐+%]|$)", line)
            if match:
                name = match.group(1) or match.group(2)
                if name and not name.startswith("#"):
                    names.append(name.strip())

        if names:
            await message.channel.send(f"```$wish {'$'.join(names)}```")

# This pulls the token from the host's settings
client.run(os.environ.get('TOKEN'))