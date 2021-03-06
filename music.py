import discord
from discord.ext import commands
import wget
from youtube_dl import YoutubeDL
import youtube_dl
import datetime
import ondaURL
import random

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #all the music related stuff
        self.is_playing = False
  
        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
    def getImg():
        destination = 'C:/Users\chana\Desktop\Discord'
        def downloadfile(filename):
            try:
                wget.download(filename, out = destination)
            except:
                pass
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url=song['url'], 
            download=False)
        thumbfiles = meta['thumbnails']
        for i in thumbfiles:
            downloadfile(i['url'])
     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title'], 'duration': info['duration']}
        

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def tellMeUnit(self):
        if int(self.durationTime) >= 3600:
            self.unitTime = 'h'
        elif int(self.durationTime) <= 59:
            self.unitTime = 's'
        elif int(self.durationTime) >= 60 and int(self.durationTime) >= 3599:
            self.unitTime = 'm'
        return self.unitTime

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        global song, durationTime
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("?????????????????????????????? ???????????????????????????????????????????????????????????? ????????????????????????")
        else:
            song = self.search_yt(query)
            durationTime = song['duration']
            unitTime = []
            if int(durationTime) >= 3600:
                unitTime = 'h'
                
            elif int(durationTime) >= 60 and int(durationTime) >= 3599:
                unitTime = 'm'
            else:
                unitTime = 's'
            duration = str(datetime.timedelta(seconds=int(song['duration'])))
            title = song['title']
            
            embed = discord.Embed(title=f'Added {title} to queue' , description=f'{duration} {unitTime}')
            embed.add_field(name="Request by: ", value=ctx.author.mention)
            Onda = random.choice(ondaURL.OndaURL)
            embed.set_thumbnail(url=Onda)
            
                
            if type(song) == type(True):
                await ctx.send("??????????????????????????????????????????")
            else:
                await ctx.send(embed=embed)
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()
    



    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
        
        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await ctx.send("Skipped")
            await self.play_music()
    @commands.command(name="stop", help="stop music for playing ?????????????????????")
    async def stop(self, ctx):
        if self.is_playing():
            await self.vc.stop()
        else:
            await ctx.send("?????????????????????????????????????????????????????????????????????????????? uwu")