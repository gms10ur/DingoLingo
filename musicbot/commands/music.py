import asyncio

import discord
from config import config
from discord.ext import commands
from musicbot import linkutils, utils


class Music(commands.Cog):
    """ A collection of the commands related to music playback.

        Attributes:
            bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', description=config.HELP_YT_LONG, help=config.HELP_YT_SHORT,
                      aliases=['p', 'yt', 'pl', 'cal', 'c'])
    async def _play_song(self, ctx, *, track: str):

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) == False:
            return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            await ctx.send("Dongu açık. {}dongu ile kapatabilirsin".format(config.BOT_PREFIX))
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)

    @commands.command(name='dongu', description=config.HELP_LOOP_LONG, help=config.HELP_LOOP_SHORT, aliases=['l'])
    async def _loop(self, ctx):

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            await ctx.send("Bişi çalmamı istemedin ki!")
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            await ctx.send("Döngü açık :white_check_mark: , ölene kadar dinleyin!")
        else:
            audiocontroller.playlist.loop = False
            await ctx.send("Döngü kapalı :x:")

    @commands.command(name='karistir', description=config.HELP_SHUFFLE_LONG, help=config.HELP_SHUFFLE_SHORT,
                      aliases=["sh"])
    async def _shuffle(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Bişi çalmamı istemedin gardaş!")
            return

        audiocontroller.playlist.shuffle()
        await ctx.send("SALLA SALLA KARIŞTIRRRRRR :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @commands.command(name='bekle', description=config.HELP_PAUSE_LONG, help=config.HELP_PAUSE_SHORT)
    async def _pause(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.send("Bekliyom gardaş :pause_button:")

    @commands.command(name='liste', description=config.HELP_QUEUE_LONG, help=config.HELP_QUEUE_SHORT,
                      aliases=['playlist', 'q', 'sira'])
    async def _queue(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Henüz bişi çalmıyom. YOK MU Bİ İSTEK PARÇA?")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        # Embeds are limited to 25 fields
        if config.MAX_SONG_PRELOAD > 25:
            config.MAX_SONG_PRELOAD = 25

        embed = discord.Embed(title=":scroll: Istek Listesi [{}]".format(
            len(playlist.playque)), color=config.EMBED_COLOR, inline=False)

        for counter, song in enumerate(list(playlist.playque)[:config.MAX_SONG_PRELOAD], start=1):
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='dur', description=config.HELP_STOP_LONG, help=config.HELP_STOP_SHORT, aliases=['st'])
    async def _stop(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.send("Hadi EYW :octagonal_sign:")

    @commands.command(name='tasi', description=config.HELP_MOVE_LONG, help=config.HELP_MOVE_SHORT, aliases=['mv', 'deis'])
    async def _move(self, ctx, *args):
        if len(args) != 2:
            ctx.send("2 tane sayi söylücen mal mısın")
            return

        try:
            oldindex, newindex = map(int, args)
        except ValueError:
            ctx.send("sayı diyom sayıııı")
            return

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Bişi çalmıyom ki :x:")
            return
        try:
            audiocontroller.playlist.move(oldindex - 1, newindex - 1)
        except IndexError:
            await ctx.send("yok orda bi şarkı")
            return
        await ctx.send("değiştim")

    @commands.command(name='gec', description=config.HELP_SKIP_LONG, help=config.HELP_SKIP_SHORT, aliases=['s', 'skip'])
    async def _skip(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Sırada bi şarkı kalmadı gardaş :x:")
            return
        current_guild.voice_client.stop()
        await ctx.send("SI RA DA Kİİİİ :fast_forward:")

    @commands.command(name='temizle', description=config.HELP_CLEAR_LONG, help=config.HELP_CLEAR_SHORT, aliases=['cl'])
    async def _clear(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.send("Sıra pırıl pırıl oldu :no_entry_sign:")

    @commands.command(name='onceki', description=config.HELP_PREV_LONG, help=config.HELP_PREV_SHORT, aliases=['back', 'geri', 'prev'])
    async def _prev(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await ctx.send("GEÇMİŞİ GERİ GETİREMEZSİN AMA OLSUN :track_previous:")

    @commands.command(name='devam', description=config.HELP_RESUME_LONG, help=config.HELP_RESUME_SHORT)
    async def _resume(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()
        await ctx.send("Rİ Rİ Rİ RİTİM SHOWW :arrow_forward:")

    @commands.command(name='sarki', description=config.HELP_SONGINFO_LONG, help=config.HELP_SONGINFO_SHORT,
                      aliases=["np"])
    async def _songinfo(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output(config.SONGINFO_SONGINFO))

    @commands.command(name='gecmis', description=config.HELP_HISTORY_LONG, help=config.HELP_HISTORY_SHORT)
    async def _history(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await ctx.send(utils.guild_to_audiocontroller[current_guild].track_history())

    @commands.command(name='ses', aliases=["vol"], description=config.HELP_VOL_LONG, help=config.HELP_VOL_SHORT)
    async def _volume(self, ctx, *args):
        if ctx.guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return

        if await utils.play_check(ctx) == False:
            return

        if len(args) == 0:
            await ctx.send("ŞU ANKİ SES YÜKSEKLİĞİ: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume))
            return

        try:
            volume = args[0]
            volume = int(volume)
            if volume > 100 or volume < 0:
                raise Exception('')
            current_guild = utils.get_guild(self.bot, ctx.message)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                await ctx.send('böyle kısıyorsun, ayıp ediyorsun beni kayıp ediyorsun karşim')
            else:
                await ctx.send('RİTİM SHOOOOOOWWW LETS GOOO')
            utils.guild_to_audiocontroller[current_guild].volume = volume
        except:
            await ctx.send("La denyo sıfırla yüz arasında bi sayı tutcan la altı üstü")

    @commands.command(name='ritimshow', description="Rİ Rİ Rİ Rİ Rİ RİTİM SHOWW AMAN UZAYLILAR BİLE DİNLİYOR", help="ritim show",
                      aliases=['ritim', 'r', 'ritimşov', 'ritimsov', 'rt'])
    async def _ritim_show(self, ctx):

        track = "https://www.youtube.com/watch?v=gTnunmBj8FQ"
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        await ctx.send("HAYDİ BAKALIM RİTİM SHOW GELSİN RİTİM SHOW")

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)

def setup(bot):
    bot.add_cog(Music(bot))