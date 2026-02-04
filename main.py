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
            
            # --- STRICT PATTERN MATCHING ---
            
            # 1. Standard Pattern: #123 - Name - Series
            # Logic: Look for "#<digits> - ", then capture content, then force a " - " after it.
            std_match = re.search(r"^#\d+\s+-\s+(.*?)\s+-\s+.*$", line)
            
            # 2. MMRK Pattern: #4 - Name 1,244 ka
            # Logic: Look for "#<digits> - ", capture content, and MUST end with "ka".
            # The '$' at the end is crucial—it prevents it from matching standard lines.
            mmrk_match = re.search(r"^#\d+\s+-\s+(.*?)\s+\d[\d,]*\s+ka$", line)
            
            # 3. Wishlist Pattern: Kirby ❌
            # Logic: Grab everything until it hits a known Mudae emoji.
            emoji_match = re.search(r"^(.*?)(?:\s+[❌✅🔐⭐+%]|$)", line)

            if std_match:
                names.append(std_match.group(1).strip())
            elif mmrk_match:
                names.append(mmrk_match.group(1).strip())
            elif emoji_match:
                # Fallback: Only accept if it doesn't look like a broken # rank line
                val = emoji_match.group(1).strip()
                if val and not val.startswith("#"):
                    names.append(val)

        if names:
            # Send the clean list
            await message.channel.send(f"```{'$'.join(names)}```")

client.run(os.environ.get('TOKEN'))
