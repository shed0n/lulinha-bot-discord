import requests as req
import telegram
import discord
import asyncio
import json
import os


telegram_token = os.getenv('TELEGRAM_TOKEN')
group_id = os.getenv('TELEGRAM_GROUPID')

client = discord.Client()

async def get_price():
  response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
  jsonRes = response.json()
  value_response = jsonRes['price']
  value = float(value_response)
  return(value)

# Send a message to a telegram user or group 
async def send(price):
    bot = telegram.Bot(token=telegram_token)
    bot.sendMessage(chat_id=group_id, text='ALERTA DE ADA: %s' %price)


async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(811733009044733962)
    ada_min = 1.60
    ada_max = 2
    while not client.is_closed():
        price = await get_price()
        if price >= ada_max or price <= ada_min:
            print("Sending Alert do Discord and Telegram")
            print("{:.2f}".format(price))
            await channel.send('ALERTA DE ADA: %s' %price)
            await send(price)
            ada_min = ada_min - 0.15
            await asyncio.sleep(30) # task runs every 5 minutes
        else:
            print("{:.2f}".format(price))
        await asyncio.sleep(30) # task runs every 30 seconds

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!preço'):
    price = await get_price()
    await message.channel.send('Preço atual da ADA: %s' %price)

client.loop.create_task(my_background_task())
client.run(os.getenv('TOKEN'))
