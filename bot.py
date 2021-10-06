import discord
import random
from discord.ext import commands
from music import music_cog
from discord.ext.commands import has_permissions

client = commands.Bot(command_prefix = ".")
clientUser = discord.Client()


@client.event # Start
async def on_ready():
    print('\nBon bon chocolat')
    print('Go up to the sky\n')
    print("_____\t\t_")
    print('|  _  |         | |')
    print('| | | |_ __   __| | __ _ ')
    print("| | | | '_ \ / _` |/ _` |")
    print('\ \_/ / | | | (_| | (_| |')
    print("\___/|_| |_|\__,_|\__,_|")
    print("\nAll light we're Everglow")
    print("This bot is for personal use")
    print("Made by Somxhai // But most of the music code i copied uwu\n")
    print("The bot is ready now...")


@client.get_context
async def on_message(message):
    games = ["Apex Legends", "Naruto Shippuden", "Satisfactory", "Roblox", "GTA", "Dying light"]
    yes = ["Ok", "โอเค", "ดีมาก", "เยี่ยม"]
    no = ["No", "ไม่", "ไม่เอา", "เบื่อแล้ว"]
    if message.content in yes:
        await message.channel.send("โอเคเยี่ยมมาก งั้นไปนอนละ บาย")
    elif message.content in no:
        count = 0
        while True:
            if count < 2:
                await message.send("งั้นสุ่มอีกรอบนะ" + random.choice(games))
                count += 1
            elif count >= 2:
                await message.channel.send("เรื่องมากก็ไม่ต้องเล่น ไอสัส")
                break
    else:
        await message.channel.send("พูดมากว่ะ กูไปละ")
    

@client.command()
async def booyah(ctx):
    await ctx.send("ลากหัวคม ๆ")


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
@has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, message=None): 
    
    embedMessage = discord.Embed(title="Onda ได้เต้น bon bon chocolat พร้อมพูดว่า", description=message, color=discord.Color.orange())
    await member.send(embed=embedMessage)
    await member.ban(reason = message)


@client.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unbanMessage = discord.Embed(title=f'Unbanned {ctx.author.mention}')
            await ctx.send(embed=unbanMessage)
            return


@client.command(pass_context = True)
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send('เลือกสักห้องไอแก่')
    await ctx.author.voice.channel.connect()
    await ctx.send("ว่าไงไอแก่")


@client.command()
async def disconnect(ctx):
    voicetrue = ctx.author.voice
    mevoice = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('เลือกสักห้องไอแก่')
    if mevoice is None:
        return await ctx.send('ยังไม่ได้เข้าห้องเลย ไอสวะ')
    await ctx.guild.voice_client.disconnect()
    await ctx.send("คามุย", file = discord.File('kamui.jpg'))


@client.command(aliases=["g", "เกม", "G", "gaMe"])
async def game(ctx):
    await ctx.send(f"วันนี้อยากเล่นเกมอะไรหรอ {ctx.author.mention}")
    await ctx.send("เดี๋ยวคิดให้แป๊ปนะ")
    games = ["Apex Legends", "Naruto Shippuden", "Satisfactory", "Roblox", "GTA", "Dying light"]
    await ctx.send(random.choice(games) + " เป็นไงล่ะ?")





client.add_cog(music_cog(client))
client.run('ODk0MDI5ODExMjEzODA3NjI2.YVkEJQ.naxgjmCfv5Yr4H9leaHBqkAV73w')
