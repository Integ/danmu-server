import subprocess
import discord
import re
from websocket import create_connection

ws = create_connection("ws://localhost:8080/ws")
result =  ws.recv()
print("[DISCORD-BOT] WebSocket Received: '%s'" % result)

bot = discord.Client()

@bot.event
async def on_ready():
    print('[DISCORD-BOT] We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    if re_words.search(message.content):
        with subprocess.Popen(['trans', '-b', ':en', message.content], stdout=subprocess.PIPE) as proc:
            output, err = proc.communicate()
    else:
        with subprocess.Popen(['trans', '-b', ':zh', message.content], stdout=subprocess.PIPE) as proc:
            output, err = proc.communicate()

    res = output.decode('utf8').rstrip()
    danmu = 'DANMAKU:{0.author.name}: {0.content} == {1}'.format(message, res)
    ws.send(danmu)
    print('[DISCORD-BOT] {}'.format(danmu))
    await message.channel.send(res)

bot.run('NTY1NjE5MjA3MDg2MDE0NDgy.XK5KvQ.C68B2Qxi4RlB_gGDM7b8kwI9gLo')
