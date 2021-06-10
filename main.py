#pip install --upgrade requests
#pip install -U discord.py
#pip install -U python-dotenv
import requests as req
import json
import time
import discord
import os
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(811733009044733962)
    while not client.is_closed():
        ada_min = 1.60
        ada_max = 2
        response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
        jsonRes = response.json()
        value_response = jsonRes['price']
        value = float(value_response)

        if value >= ada_max or value <= ada_min:
            print("Sending Alert do Discord and Telegram")
            print("{:.2f}".format(value))
            await channel.send('ALERTA DE ADA: %s' %value)
            await asyncio.sleep(300) # task runs every 300 seconds
        else:
            print("{:.2f}".format(value))
        await asyncio.sleep(30) # task runs every 30 seconds

client.loop.create_task(my_background_task())
client.run(os.getenv('TOKEN'))
