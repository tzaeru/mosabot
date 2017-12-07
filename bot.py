import discord
from discord.ext import commands
import random
import weather
import urllib
import datetime
import config
import time
import asyncio
from tinydb import TinyDB, Query
lan_db = TinyDB('lan_db.json')

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

roles = ['Overwatch', 'PUBG', 'GrimDawn', 'Verdun', 'Kiipeilijät', 'Squad']



@bot.event
async def on_message(message):
    if message.channel.name != "beepboop":
        return

    if message.content.startswith('!deleteme'):
        msg = await bot.send_message(message.channel, 'I will delete myself now...')
        await bot.delete_message(msg)
        await bot.delete_message(message)

    if message.content.startswith('!'):
        # Check for weather
        if message.content.startswith('!sää'):
            print("Location: " + message.content.split(" ", 1)[1].rsplit(" ", 1)[0])
            w, icon = weather.get_weather(message.content.split(" ", 1)[1].rsplit(" ", 1)[0])
            msg = w
            await bot.send_file(message.channel, urllib.request.urlopen("http:"+icon), filename="weather.png", content=w)
            return

        if message.content.startswith('!help'):
            help_msg = "Beep boop!\n\n!sää Espoo\n\n"
            help_msg += "To join/leave a role, type in one of the following:\n"
            for _role in roles:
                help_msg += "!" + _role + "\n"
            await bot.send_message(message.channel, help_msg)
            return

        if message.content.startswith('!lan add'):
            date = datetime.datetime.strptime(message.content[message.content.rfind(' ')+1:], "%d.%m.%Y").date()
            days_to_event = (date-datetime.date(1970,1,1))

            name = message.content[message.content.find(' ', 5)+1:message.content.rfind(' ')]

            lan_db.insert({'name': name, 'date': days_to_event.days, 'participants': []})

            await bot.send_message(message.channel, "Created LAN party " + name + ", " + str(days_to_event.days) + " days from now.")
            return
            
        if message.content.startswith('!lan remove'):
            name = message.content[message.content.find(' ', 5)+1:]
            
            lans = Query()
            lan_db.remove(lans.name == name)
            
            await bot.send_message(message.channel, "Removed LAN party " + name)
            return
        
        if message.content.startswith('!lan participate'):
            name = message.content[message.content.find(' ', 5)+1:]
            
            lans = Query()
            participants = lan_db.search(lans.name==name)[0]["participants"]
            
            # If sender is already in participants, remove them
            removed = False
            if message.author.name in participants:
                participants.remove(message.author.name)
                removed = True
            else:
                participants.append(message.author.name)
                
            lan_db.update({'participants': participants}, lans.name == name)
            
            await bot.send_message(message.channel, "Participants to " + name + " are: " + str(participants))
            return

        if message.content.startswith('!lan'):
            lans = Query()

            lan_msg = ""
            
            if len(message.content) > 4:
                name = message.content[message.content.find(' ')+1:message.content.rfind(' ')]
                lan_msg = lan_db.search({"name": name})            
            else:
                lan_msg = lan_db.search(lans.date > 0)

            await bot.send_message(message.channel, lan_msg)
            return
            
        # Check for role
        role_string = message.content[1:].lower()
        if role_string not in map(str.lower, roles):
            print(role_string + " not in roles!")
            await bot.send_message(message.channel, "Beep boop! Command not found!")
            return

        # Find role
        role = None
        for _role in message.server.roles:
            if _role.name.lower() == role_string.lower():
                role = _role;

        # Check if author already has the role
        author_has_role = False
        for _role in message.author.roles:
            if _role.id == role.id:
                author_has_role = True

        if author_has_role is True:
            await bot.remove_roles(message.author, role)
            await bot.send_message(message.channel, "Beep boop - you're no longer in " + role.name)
        else:
            await bot.add_roles(message.author, role)
            await bot.send_message(message.channel, "Beep boop - you're now in " + role.name)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(config.bot_token)
