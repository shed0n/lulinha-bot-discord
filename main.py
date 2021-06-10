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
    print('We have logged in as {0.user}'.format(client))
    print('------')

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = client.get_channel(811733009044733962)
    print(channel)
    print('antes do while')
    while not client.is_closed():
        print('got in while')
        ada_min = 1.60
        ada_max = 2
        response = req.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
        print("Value:", response.json())
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
client.run('Nzc4Nzc1NTczNzM5ODY0MTE0.X7W5RQ.yCGRpVj7IAuTzuCOZnakuSbwRDY')
