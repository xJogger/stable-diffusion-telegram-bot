from pyrogram import Client, filters
from pyrogram.types import *
import os
import json
import requests
import io
import random
from PIL import Image, PngImagePlugin
import base64

with open("config.txt",'r') as f:
    config_list = f.read().split('\n')

API_ID   = config_list[0]
API_HASH = config_list[1]
TOKEN    = config_list[2]
SD_URL   = config_list[3]
USER_ID  = int(config_list[4])

negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet"

app = Client(
    "stable",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

@app.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    await message.reply_text("Hello!")



# @app.on_message(filters.command(["draw"]))
@app.on_message(filters.text)
def draw(client, message):
    if message.from_user.id == USER_ID:
        # msgs = message.text.split(' ', 1)
        # if len(msgs) == 1:
        #     message.reply_text("Format : /draw < text to anime image >")
        #     return
        # msg = msgs[1]

        msg = message.text

        K = message.reply_text("Please Wait 10-15 Second")

        payload = {
                "prompt": msg,
                "negative_prompt": negative_prompt,
            }

        r = requests.post(url=f'{SD_URL}/sdapi/v1/txt2img', json=payload).json()

        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars1 = "1234564890"
        gen1 = random.choice(chars)
        gen2 = random.choice(chars)
        gen3 = random.choice(chars1)
        gen4 = random.choice(chars)
        gen5 = random.choice(chars)
        gen6 = random.choice(chars)
        gen7 = random.choice(chars1)
        gen8 = random.choice(chars)
        gen9 = random.choice(chars)
        gen10 = random.choice(chars1)
        word = f"{message.from_user.id}-MOE{gen1}{gen2}{gen3}{gen4}{gen5}{gen6}{gen7}{gen8}{gen9}{gen10}"

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

            png_payload = {"image": "data:image/png;base64," + i}
            response2 = requests.post(url=f'{SD_URL}/sdapi/v1/png-info',
                                      json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save(f'{word}.png', pnginfo=pnginfo)

            message.reply_photo(
                photo=f"{word}.png",
                caption=
                f"Prompt - **{msg}**\n **{message.from_user.first_name}**"
            )
            os.remove(f"{word}.png")
            K.delete()
    else:
        message.reply_text(f"You are not allowed to use this bot.\nYour user id is: {message.from_user.id}")

app.run()
