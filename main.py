import requests as req
import json
import discord
import os
import asyncio

client = discord.Client()

async def get_price():
  response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
  jsonRes = response.json()
  value_response = jsonRes['price']
  value = float(value_response)
  return(value)

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(811733009044733962)
    while not client.is_closed():
        ada_min = 1.40
        ada_max = 2
        price = await get_price()
        if price >= ada_max or price <= ada_min:
            print("Sending Alert do Discord and Telegram")
            print("{:.2f}".format(price))
            await channel.send('ALERTA DE ADA: %s' %price)
            await asyncio.sleep(900) # task runs every 15 minutes
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
