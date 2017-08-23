import discord
from discord.ext import commands
import random
import weather
import urllib
import config
import asyncio  

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

roles = ['Overwatch', 'PUBG']

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

    	# Check for role
    	role_string = message.content[1:]
    	if role_string not in roles:
    		print(role_string + " not in roles!")
    		await bot.send_message(message.channel, "Beep boop! Command not found!")
    		return

    	# Find role
    	role = None
    	for _role in message.server.roles:
    		if _role.name == role_string:
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
