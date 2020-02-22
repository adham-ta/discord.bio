# Imports
import asyncio
import datetime
import json
import logging
import random

import aiohttp
import discord
from discord.ext import commands

import Config


class Bio(commands.Cog):



    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def profile(self, ctx, profile = None):
        """
        View a user's profile.
        """
        if profile == None:
            profile = ctx.author.id
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.discord.bio/v1/userDetails/{profile}") as resp1:
                if resp1.status == 200:
                    data1 = await resp1.text()
                    data1 = json.loads(data1)
                    if data1["success"] != False:
                        data1 = data1
                    else:
                        data1 = None
                else:
                    data1 = None
            async with session.get(f"https://api.discord.bio/v1/userConnections/{profile}") as resp2:
                if resp2.status == 200:
                    data2 = await resp2.text()
                    data2 = json.loads(data2)
            async with session.get(f"https://api.discord.bio/v1/discordConnections/{profile}") as resp3:
                if resp3.status == 200:
                    data3 = await resp3.text()
                    data3 = json.loads(data3)
        if data1 == None:
            if profile == ctx.author.id:
                embed = discord.Embed(
                        title = "Profile Not Found",
                        description = "You don't have a profile set up on [discord.bio](https://discord.bio/), please set one up and then try again!",
                        color = Config.ERRORCOLOR
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                        title = "Profile Not Found",
                        description = "Profile not found, please enter a valid user ID or slug!",
                        color = Config.ERRORCOLOR
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                    title = "Slug: " + data1["settings"]["name"],
                    url = f"https://discord.bio/p/{data1['settings']['name']}",
                    color = Config.MAINCOLOR
            )
            embed.set_author(name = "Profile")
            async with aiohttp.ClientSession() as session:
                id = data1["discord"]["id"]
                name = data1["discord"]["avatar"]
                async with session.get(f"https://cdn.discordapp.com/avatars/{id}/{name}.gif") as resp4:
                    if resp4.status == 200:
                        embed.set_thumbnail(url = f"https://cdn.discordapp.com/avatars/{id}/{name}.gif")
                    if resp4.status == 415:
                        embed.set_thumbnail(url = f"https://cdn.discordapp.com/avatars/{id}/{name}")
            if data1["settings"]["status"] == None:
                embed.add_field(name = "☁️ Status", value = "No status set.")
            else:
                embed.add_field(name = "☁️ Status", value = data1["settings"]["status"])
            if data1["settings"]["description"] == None:
                embed.add_field(name = "✏️ Description", value = "No descrption set.")
            else:
                embed.add_field(name = "✏️ Description", value = data1["settings"]["description"], inline = False)
            if data1["settings"]["email"] != None:
                embed.add_field(name = "📧 Email", value = data1["settings"]["email"], inline = False)
            badges = ""
            if data1["settings"]["verified"] == 1:
                badges = badges + "[<:verified:680351714301575178>](https://discordbio.typeform.com/to/DtEvyx)"
            if data1["settings"]["premium_status"] == 1:
                badges = badges + "[💎](https://discord.bio/plans)"
            if data1["settings"]["name"] == "polar":
                badges = badges + "[<a:polar:680353468510109705>](https://discord.bio/p/polar)"
            if data1["settings"]["name"] == "v":
                badges = badges + "[<:ven:680352094149935235>](https://discord.bio/p/v)"
            if data1["settings"]["name"] == "princess":
                badges = badges + "[<:ravy:680353379008249878>](https://discord.bio/p/princess)"
            if badges != "":
                embed.add_field(name = "Badges", value = badges)
            if data1["settings"]["location"] != None:
                embed.add_field(name = "🗺️ Location", value = data1["settings"]["location"])
            if data1["settings"]["birthday"] != None:
                date = data1["settings"]["birthday"]
                date = datetime.datetime.strptime(date[:10], "%Y-%M-%d").strftime("%B %d, %Y")
                if datetime.datetime.utcnow().strftime("%B %d, %Y") == date:
                    date = f"**🎉 {date}**"
                embed.add_field(name = "🎂 Birthday", value = date)
            if data1["settings"]["occupation"] != None:
                embed.add_field(name = "💼 Occupation", value = data1["settings"]["occupation"])
            if data1["settings"]["banner"] != None:
                if data1["settings"]["premium_status"] == 1:
                    embed.set_image(url = data1["settings"]["banner"])
            embed.add_field(name = "<:upvote:680349321727705113> Upvotes", value = str(data1["settings"]["upvotes"]))
            if data1["settings"]["gender"] != None:
                if data1["settings"]["gender"] == 1:
                    gender = "Male"
                if data1["settings"]["gender"] == 2:
                    gender = "Female"
                embed.add_field(name = "Gender", value = gender)
            connections = ""
            if data2["github"]["name"] != None:
                name = data2["github"]["name"]
                connections = connections + f"[<:github:680572757020639243>](https://github.com/{name})"
            if data2["website"]["name"] != None:
                url = data2["website"]["name"]
                connections = connections + f"[🌐]({url})"
            if data2["instagram"]["name"] != None:
                name = data2["instagram"]["name"]
                connections = connections + f"[<:instagram:680574384662118451>](https://www.instagram.com/{name})"
            if data2["snapchat"]["name"] != None:
                name = data2["snapchat"]["name"]
                connections = connections + f"[<:snapchat:680574977095106635>](https://www.snapchat.com/add/{name})"
            if data2["linkedin"]["name"] != None:
                name = data2["linkedin"]["name"]
                connections = connections + f"[<:linkedin:680576207171223577>](www.linkedin.com/in/{name})"
            if connections != "":
                embed.add_field(name = "Connections", value = connections)
            if data3 == []:
                pass
            else:
                discord_connections = ""
                for connection in data3:
                    if connection["url"] != None:
                        if connection["connection_type"] == "reddit":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:reddit:680628175792898121>]({url})"
                        if connection["connection_type"] == "spotify":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:spotify:680628639947423755>]({url})"
                        if connection["connection_type"] == "steam":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:steam:680626858768990243>]({url})"
                        if connection["connection_type"] == "twitch":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:twitch:680626858890362891>]({url})"
                        if connection["connection_type"] == "twitter":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:twitter:680627166501011477>]({url})"
                        if connection["connection_type"] == "youtube":
                            url = connection["url"]
                            discord_connections = discord_connections + f"[<:youtube:680626858810802177>]({url})"
                    else:
                        if connection["connection_type"] == "xbox":
                            discord_connections = discord_connections + f"<:xbox:680626858840293439>"
                        if connection["connection_type"] == "battlenet":
                            discord_connections = discord_connections + f"<:battlenet:680626859171643440>"
                        if connection["connection_type"] == "leagueoflegends":
                            discord_connections = discord_connections + f"<:league:680626860111298578>"
                if discord_connections != "":
                    embed.add_field(name = "Discord Connections", value = discord_connections)
            embed.set_footer(text = "This bot is not part of discord.bio or Discord, but rather an application based around both.")
            await ctx.send(embed = embed)
    
    @commands.command()
    async def leaderboard(self, ctx):
        """
        View the top ten people on the leaderboard upvote wise.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.discord.bio/v1/topUpvoted") as resp:
                if resp.status == 200:
                    data = await resp.text()
                    data = json.loads(data)
        embed = discord.Embed(
                color = Config.MAINCOLOR
        )
        embed.set_author(name = "Leaderboard")
        embed.set_footer(text = "This bot is not part of discord.bio or Discord, but rather an application based around both.")
        number = 1
        for profile in data:
            embed.add_field(name = f"Number {number}", value = f"[{profile['user']['name'].title()}](https://discord.bio/p/{profile['user']['name']})")
            number += 1
        await ctx.send(embed = embed)
        

def setup(bot):
    bot.add_cog(Bio(bot))
