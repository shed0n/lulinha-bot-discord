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
  value_response = {'ADA':float(jsonResADA['price']),'LRC':float(jsonResLRC['price'])}
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
    lrc_min = 2.50
    lrc_max = 5
    while not client.is_closed():
        price = await get_price()
        if price['ADA'] >= ada_max or price['ADA'] <= ada_min:
            print("Sending Alert to Discord")
            print("{:.2f}".format(price['ADA']))
            await channel.send('ALERTA DE ADA: %s' %price['ADA'])
            await send(price['ADA'])
            ada_max = ada_max + 0.10
            await asyncio.sleep(30) # task runs every 5 minutes
        else:
            print("{:.2f}".format(price['ADA']))

        if price['LRC'] >= lrc_max or price['LRC'] <= lrc_min:
            print("Sending Alert to Discord")
            print("{:.2f}".format(price['LRC']))
            await channel.send('ALERTA DE LRC: %s' %price['LRC'])
            await send(price['LRC'])
            lrc_max = lrc_max + 0.10
            await asyncio.sleep(30) # task runs every 5 minutes
        else:
            print("{:.2f}".format(price['LRC']))

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

  if message.content.lower() == '!ada' or message.content.lower() == '!cardas':
    price = await get_price()
    await message.channel.send('Preço atual da ADA: %s' %price['ADA'])

  if message.content.lower() == '!lrc' or message.content.lower() == '!loopas':
    price = await get_price()
    await message.channel.send('Preço atual do LRC: %s' %price['LRC'])

client.loop.create_task(my_background_task())
client.run(discord_token)
