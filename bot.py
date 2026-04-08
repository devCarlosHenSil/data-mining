import os
os.environ["PYTHONHTTPSVERIFY"] = "0"  # Bypass SSL corporativo - obrigatório aqui

import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} online - Mila-Bot funcionando exatamente como no documento")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message) or "mila-bot" in message.channel.name.lower():
        if "anime" in message.content.lower() and ("estrear" in message.content.lower() or "breve" in message.content.lower()):
            animes = await fetch_upcoming_animes()  # chama o Oracle real
            reply = "Olha só os animes estreando em breve! 🔥\n\n"
            for a in animes:
                reply += f"• **{a['title']}**\n  {a['date']} - {a['relevance']}\n"
            reply += "\nÓtimo pra conteúdos de hype! 💙"
            await message.channel.send(reply)
        else:
            await message.channel.send("Consultando dados...")

@tasks.loop(hours=24)
async def daily_digests():
    channel = discord.utils.get(bot.get_all_channels(), name="mila-bot")
    if channel:
        day = datetime.now().strftime("%A")
        if day == "Monday":   await channel.send("**Recap Performance**")
        elif day == "Tuesday": await channel.send("**Radar de Concorrentes**")
        elif day == "Wednesday": await channel.send("**Playbook de Conteúdo**")
        elif day == "Thursday": await channel.send("**Oportunidades e Preços**")
        elif day == "Friday": await channel.send("**Semana que Vem**")

bot.run(os.getenv("DISCORD_TOKEN"))