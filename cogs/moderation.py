import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime

load_dotenv("../.env")


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.footer_text = "Made by Voidsudo"
        
    async def send_embed(self, ctx, title, description, color):
        embed = discord.Embed(
            title=title,
            description=description,
            color=0x4863A0
        )
        embed.set_footer(text=self.footer_text)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="ban", description="Ban a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = None):
        await ctx.defer()
        try:
            await member.ban(reason=reason)
            await self.send_embed(ctx, "Member Banned", f"{member.mention} was banned", discord.Color.red())
        except discord.Forbidden:
            await self.send_embed(ctx, "Error", "Need Higher Permissions", discord.Color.red())

    @discord.slash_command(name="kick", description="Kick a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        await ctx.defer()
        try:
            await member.kick(reason=reason)
            await self.send_embed(ctx, "Member Kicked", f"{member.mention} was kicked", discord.Color.orange())
        except discord.Forbidden:
            await self.send_embed(ctx, "Error", "Need Higher Permissions", discord.Color.red())

    @discord.slash_command(name="timeout", description="Timeout a member from the server.")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: int, reason: str = None):
        await ctx.defer(ephemeral=True)
        try:
            timeout_duration = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_duration, reason=reason)
            await self.send_embed(ctx, "Member Timed Out", f"{member.mention} was timed out for {duration} minutes", discord.Color.blue())
        except discord.Forbidden:
            await self.send_embed(ctx, "Error", "Need Higher Permissions", discord.Color.red())
        except Exception as e:
            await self.send_embed(ctx, "Error", str(e), discord.Color.red())

    @commands.slash_command(name="unban", description="Unban a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, reason: str = None):
        await ctx.defer()
        try:
            await ctx.guild.unban(member, reason=reason)
            await self.send_embed(ctx, "Member Unbanned", f"{member.mention} was unbanned", discord.Color.green())
        except discord.Forbidden:
            await self.send_embed(ctx, "Error", "Need Higher Permissions", discord.Color.red())
        except discord.NotFound:
            await self.send_embed(ctx, "Error", "Member not found or not banned", discord.Color.red())

    @commands.slash_command(name="untimeout", description="Unmute a member from the server.")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, reason: str = None):
        await ctx.defer(ephemeral=True)
        try:
            await member.remove_timeout(reason=reason)
            await self.send_embed(ctx, "Member Untimed Out", f"{member.mention} was unmuted", discord.Color.green())
        except discord.Forbidden:
            await self.send_embed(ctx, "Error", "Need Higher Permissions", discord.Color.red())
        except Exception as e:
            await self.send_embed(ctx, "Error", str(e), discord.Color.red())

def setup(bot):
    bot.add_cog(Mod(bot))
