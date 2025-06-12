
from code import interact
import requests
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import aiohttp
from discord import app_commands
import asyncio

GUILD_ID = discord.Object(id=1371802271503093770)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

assign_role = "Donkey"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

    await bot.tree.sync()
    print(f"Synced slash commands for {bot.user}")


async def main():
    await bot.load_extension("cogs.space")
    print("done !!")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome Mother *Nature* Lover <3 {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} Senpaiiiiii very bad ;-; , i deleted the message")

    await bot.process_commands(message)


@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


@bot.command()
async def assign(ctx):
    roles = discord.utils.get(ctx.guild.roles, name=assign_role)
    if roles:
        await ctx.author.add_roles(roles)
        await ctx.send(f"{assign_role} Senpaiiiii Role has been updated :3 {ctx.author.mention}")
    else:
        await ctx.send(
            f"𝕾𝖊𝖓𝖕𝖆𝖎 ;-; , 𝕽𝖔𝖑𝖊 𝕯𝖔𝖊𝖘 𝖓𝖔𝖙 𝖊𝖝𝖎𝖘𝖙 𝖔𝖗 𝖍𝖆𝖘 𝖓𝖔 𝖕𝖊𝖗𝖒𝖎𝖘𝖘𝖎𝖔𝖓 𝖙𝖔 𝖉𝖔 / 𝕮𝖗𝖊𝖆𝖙𝖊 𝖆 𝕽𝖔𝖑𝖊 𝖔𝖗 𝖌𝖎𝖛𝖊 𝖙𝖍𝖊 𝖕𝖊𝖗𝖒𝖎𝖘𝖘𝖎𝖔𝖓 𝖙𝖔 𝖆𝖘𝖘𝖎𝖌𝖓 𝖗𝖔𝖑𝖊𝖘 :3 {ctx.author.mention}")
        await ctx.send(
            f"{ctx.author.mention} 𝐈𝐅 𝐓𝐇𝐄 𝐈𝐒𝐒𝐔𝐄 𝐈𝐒𝐍’𝐓 𝐑𝐄𝐒𝐎𝐋𝐕𝐄𝐃 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 : @𝐢𝟐𝐰𝐨𝐠 𝐢𝐧 𝐃𝐢𝐬𝐜𝐨𝐫𝐝")


@bot.command()
async def remove(ctx):
    roles = discord.utils.get(ctx.guild.roles, name=assign_role)
    if roles:
        await ctx.author.remove_roles(roles)
        await ctx.send(f"{assign_role} Senpaiiiii Role has been Removed :3 {ctx.author.mention}")
    else:
        await ctx.send(
            f"{assign_role} Senpai ;-; , Role Dose not exist or has the permission to do / Create a Role or give the permission to Remove Roles :3 {ctx.author.mention}")


@bot.command()
@commands.has_role(assign_role)
async def admin(ctx):
    await ctx.send(f"IM THE ADMIN OF THE SERVER {ctx.author.mention}")


@admin.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"You are not the Owner of the bot {ctx.author.mention} ")


@bot.tree.command(name="love_you", description="Say ily ")
async def love_you(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"Loveeeeee you {member.mention} ")


@bot.command()
async def dms(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")


@bot.command()
async def reply(ctx):
    await ctx.reply(f"This is a Reply to your message")


# this command creates a poll with reaction

@bot.tree.command(name="poll", description="Create a poll")  # wont work bcus im using ctx and interaction here
async def poll(Interaction: discord.Interaction, question: str):
    embed = discord.Embed(title="Poll Time~!", description=question, color=0x00ffcc)
    poll_msg = await Interaction.channel.send(embed=embed)
    await poll_msg.add_reaction("💀")
    await poll_msg.add_reaction("⚡")

    await Interaction.response.send_message("Poll created~!", ephemeral=True)


@bot.tree.command(name="command_list", description="gives the list of commands")
async def command_list(interaction: discord.Interaction):
    await interaction.response.send_message("""here is the list of commands

    1 : !hello
    2 : !assign
    3 : !remove
    4 : !admin
    5 : !love_you
    6 : !dms
    7 : !reply
    8 : !poll
    9: !stats


    """)


# tells about the stats {bot.user.avater} shows the bots ava and {round(bot.latency * 1000)} shows the ping
# this {sum(g.member_count for g in bot.guilds)} shows the total num of members in the server
@bot.tree.command(name="stats", description="Gives the Stats")
async def stats(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌸 Bot Stats Panel 🌸",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")
    embed.add_field(name="🟢 Ping", value=f"{round(bot.latency * 1000)} ms", inline=True)
    embed.add_field(name="🖥️ Servers", value=f"{len(bot.guilds)}", inline=True)
    embed.add_field(name="👤 Users", value=f"{sum(g.member_count for g in bot.guilds)}", inline=False)
    embed.set_footer(text="Made with love by COSNT 💻💜")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="image", description="Sends a random image")
async def image(interaction: discord.Interaction):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    image_url = data["message"]

    embed = discord.Embed(title="Here is a good boogo for you :3", color=0x00ffcc)
    embed.set_image(url=image_url)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="waifu", description="Gives you a waifu pics")
async def waifu(interaction: discord.Interaction):
    response_1 = requests.get("https://api.waifu.pics/sfw/waifu")
    data_1 = response_1.json()
    image_url1 = data_1["url"]
    await interaction.response.defer()

    embed = discord.Embed(title="Waifu here !!! ", colour=0xff69b4)
    embed.set_image(url=image_url1)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="kick", description="Kick them out of your server")
async def kick(interaction: discord.Interaction, member: discord.Member, *,
               reason: str = "Kicked because of creating trouble in the server"):
    try:
        await interaction.response.defer()
        await member.kick(reason=reason)
        await interaction.followup.send(f" {member.mention} Has been kicked out of this server")
    except discord.Forbidden:
        await interaction.followup.send(f"You dont have permission to kick {member.mention}")
    except discord.HTTPException:
        await interaction.followup.send(f"GOT AN ERROR")


NASA_API_KEY = "Key Here"


@bot.tree.command(name="space", description="Here is an image of Space ;>")
async def space(interaction: discord.Interaction):
    await interaction.response.defer()
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("NASA ghosted us 🥲")
                return
            data = await resp.json()

    embed = discord.Embed(
        title=data["title"],
        description=data["explanation"][:2048],
        color=discord.Color.dark_blue()
    )
    embed.set_image(url=data["url"])
    embed.set_footer(text=f"📅 {data['date']} • from NASA")
    await interaction.followup.send(embed=embed)


bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
