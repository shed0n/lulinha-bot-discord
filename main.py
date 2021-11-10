import requests as req
import telegram
import discord
import asyncio
import json
import os


telegram_token = os.getenv('TELEGRAM_TOKEN')
group_id = os.getenv('TELEGRAM_GROUPID')
discord_token = os.getenv('TOKEN')
client = discord.Client()


# Gets the currently ADA Price from Binance
async def get_price():
  response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
  jsonResADA = response.json()
  value_response = dict()
  response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=LRCUSDT')
  jsonResLRC = response.json()
  value_respnse = {'ADA':jsonResADA['price'],'LRC':jsonResLRC['price']}
  return(value_response)

# Send message to a Telegram group
async def send(price):
    bot = telegram.Bot(token=telegram_token)
    print("Sending Alert to Telegram")
    bot.sendMessage(chat_id=group_id, text='ALERTA DE ADA: %s' %price)

# Main task
async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(811733009044733962)
    ada_min = 1.15
    ada_max = 3
    while not client.is_closed():
        price = await get_price()
        if price["ADA"] >= ada_max or price["ADA"] <= ada_min:
            print("Sending Alert to Discord")
            print("{:.2f}".format(price))
            await channel.send('ALERTA DE ADA: %s' %price)
            await send(price)
            ada_max = ada_max + 0.10
            await asyncio.sleep(30) # task runs every 5 minutes
        else:
            print("{:.2f}".format(price))
        await asyncio.sleep(30) # task runs every 30 seconds

# Notifies when connection with Discord is established
@client.event
async def on_ready():
    print('Logged in Discord as {0.user}'.format(client))

# Reply the user on discord when !preço is asked
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content == '!ADA' or message.content == '!cardas':
    price = await get_price()
    await message.channel.send('Preço atual da ADA: %s' %price["ADA"])

  if message.content == '!LRC' or message.content == '!loopas':
    price = await get_price()
    await message.channel.send('Preço atual do LRC: %s' %price["LRC"])

client.loop.create_task(my_background_task())
client.run(discord_token)
