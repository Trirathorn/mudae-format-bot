import discord, re, os, threading
from flask import Flask

# --- Health Check Server (Keeps UptimeRobot Happy) ---
app = Flask(__name__)
@app.route('/')
def health(): return "OK", 200

def run_web():
    app.run(host='0.0.0.0', port=8000)

threading.Thread(target=run_web, daemon=True).start()
# -----------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

def clean_mudae_line(line):
    # 1. Remove Discord bold markdown
    line = line.replace("**", "").strip()
    if not line: return None
    
    # 2. Remove Rank Prefix (e.g., "#4 - " or "#4 ")
    line = re.sub(r"^#\d+\s+(?:-\s+)?", "", line)
    
    # 3. Remove Values (ka / sp) -> catches " 1,244 ka" and " 1,244 ka 4,000 sp"
    line = re.sub(r"\s+\d[\d,]*\s*(?:ka|sp).*$", "", line)
    
    # 4. Remove Keys (· :bronzekey: (1) or · <:bronzekey:id>)
    line = re.sub(r"\s+·\s+.*$", "", line)
    
    # 5. Remove Emojis and percentages
    line = re.sub(r"\s+[❌✅🔐⭐+%].*$", "", line)
    
    # 6. Remove Series Name (Standard Format: "Name - Series")
    # Splits from the right to protect character names that contain hyphens
    if " - " in line:
        line = line.rsplit(" - ", 1)[0]
        
    return line.strip()

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
            cleaned_name = clean_mudae_line(line)
            if cleaned_name:
                names.append(cleaned_name)

        if names:
            await message.channel.send(f"```{'$'.join(names)}```")

client.run(os.environ.get('TOKEN'))
