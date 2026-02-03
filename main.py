import discord, re, os, threading
from flask import Flask

# --- Tiny Web Server for Health Checks ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_web():
    # Koyeb uses port 8000 by default for health checks
    app.run(host='0.0.0.0', port=8000)

# Start the web server in a separate thread
threading.Thread(target=run_web, daemon=True).start()
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user: return
    
    if message.content.startswith("-f"):
        raw_text = message.content[2:].strip()
        names = []
        for line in raw_text.split('\n'):
            line = line.strip()
            if not line: continue
            
            # Updated Regex: Priority to standard # - Name - Series
            std_match = re.search(r"^#\d+\s+-\s+(.*?)\s+-\s+.*", line)
            mmrk_match = re.search(r"^#\d+\s+-\s+(.*?)(?:\s+\d[\d,]*\s+ka|$)", line)
            emoji_match = re.search(r"^(.*?)(?:\s+[❌✅🔐⭐+%]|$)", line)

            if std_match:
                names.append(std_match.group(1).strip())
            elif mmrk_match:
                names.append(mmrk_match.group(1).strip())
            elif emoji_match:
                name = emoji_match.group(1).strip()
                if name and not name.startswith("#"):
                    names.append(name)

        if names:
            await message.channel.send(f"```{'$'.join(names)}```")

client.run(os.environ.get('TOKEN'))
