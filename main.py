import requests as req
import json
import time
import discord
import os
import asyncio

client = discord.Client()

async def get_price():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
  jsonRes = response.json()
  value_response = jsonRes['price']
  value = float(value_response)
  return(value)
 
async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(811733009044733962)
    while not client.is_closed():
        ada_min = 1.20
        ada_max = 2
        response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
        jsonRes = response.json()
        value_response = jsonRes['price']
        value = float(value_response)

        if value >= ada_max or value <= ada_min:
            print("Sending Alert do Discord and Telegram")
            print("{:.2f}".format(value))
            await channel.send('@here ALERTA DE ADA: %s' %value)
            await asyncio.sleep(300) # task runs every 300 seconds
        else:
            print("{:.2f}".format(value))
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
