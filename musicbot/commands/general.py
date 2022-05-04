import discord
from config import config
from discord.ext import commands
from discord.ext.commands import has_permissions
from musicbot import utils
from musicbot.audiocontroller import AudioController
from musicbot.utils import guild_to_audiocontroller, guild_to_settings


class General(commands.Cog):
    """ A collection of the commands for moving the bot around in you server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    # logic is split to uconnect() for wide usage
    @commands.command(name='gel', description=config.HELP_CONNECT_LONG, help=config.HELP_CONNECT_SHORT, aliases=['join', 'baglan'])
    async def _connect(self, ctx):  # dest_channel_name: str
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.uconnect(ctx)
        await ctx.send("{} {} dekiler, RİTİM ŞHOW BAŞLIYOOORR {}".format(":exclamation::exclamation:", ctx.author.voice.channel.name, ":exclamation::exclamation:"))

    @commands.command(name='git', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT, aliases=['leave', 'dc', 'bb'])
    async def _disconnect(self, ctx, guild=False):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.udisconnect()

    @commands.command(name='reset', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT, aliases=['rs', 'kendinegel', 'duzelt'])
    async def _reset(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("OH BE, Bi kendime geldim tşk")

    @commands.command(name='burayagel', description=config.HELP_CHANGECHANNEL_LONG, help=config.HELP_CHANGECHANNEL_SHORT, aliases=['bg'])
    async def _change_channel(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        vchannel = await utils.is_connected(ctx)
        if vchannel == ctx.author.voice.channel:
            await ctx.send("Zaten {} odasındayım kör müsün lan?".format(vchannel.name))
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("HOOP, Nasıl tak diye {} dayım? Saniyede!".format(ctx.author.voice.channel.name))

    @commands.command(name='kobra', description="Kobranın kim olduğunu öğren", help="Kobra?")
    async def _ping(self, ctx):
        await ctx.send("Murat")

    @commands.command(name='romancıkgelsin')
    async def _roman(self, ctx):
        await ctx.send("Romancık yok henüz")

    @commands.command(name='ayarlar', description=config.HELP_SHUFFLE_LONG, help=config.HELP_SETTINGS_SHORT, aliases=['ayarla', 'set'])
    @has_permissions(administrator=True)
    async def _settings(self, ctx, *args):

        sett = guild_to_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response is None:
            await ctx.send("`Hata: Yanlış ayarı değiştirmeye çalışıyorsun gardaş`")
        elif response is True:
            await ctx.send("Ol dedim oldu!")

    @commands.command(name='benicagir', description=config.HELP_ADDBOT_LONG, help=config.HELP_ADDBOT_SHORT)
    async def _addbot(self, ctx):
        embed = discord.Embed(title="Davet Kartı :3", description=config.ADD_MESSAGE +
                              "(https://discordapp.com/oauth2/authorize?client_id={}&scope=bot>)".format(self.bot.user.id))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
