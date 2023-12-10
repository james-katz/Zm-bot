import discord
import os
import random
from dotenv import load_dotenv
from unidecode import unidecode

load_dotenv()
my_token = os.getenv("DISCORD_TOKEN")

lista_comandos = ["zm","gm","Good morning","Morning","Gmorning","bom dia ", "dia bom","dia","Buenos días","Feliz día","Buen día","Annyeonghaseyo","안녕하세요","Joh eun achim","좋은 아침","Annyeong hasimnikka","안녕하십니까","Dobroye utro","Доброе утро","Zdravstvuyte utrom","Здравствуйте утром","Dobroye utrechko","Утро доброе","Buongiorno","Buon mattino","Buona giornata","Bonjour","bonne journée","Salut","Ina kwana","Ẹ kú aro","Ọma ụtụtụ"]

lista_comandos_n = ["zn","gn","Good night","Nighty night","Boa noite","Boa noitinha","noite","Buenas noches","annyeonghi jumuseyo","안녕히 주무세요","gutbam","굿밤","Spokoynoy nochi","Спокойной ночи","Dobroy nochi","Доброй ночи","Buona notte","Bonne nuit","Douce nuit","Ina kwana","Ẹ ku alẹ","Ku ale","Ka chi fo"]

lista_respostas = ["Zm Zcasher","Zm zfriend","gm Zfriend", "gm Zcasher"]

lista_respostas_n = ["Zn Zcasher","Zn zfriend","gn Zfriend", "gn Zcasher"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print (f'estou pronto!zm meu ID é {client.user.id}')
    
@client.event
async def on_message(message):

    if message.author == client.user :
     return 
    
    lista_stk = await message.guild.fetch_stickers()
    random_sticker = random.choice(lista_stk)

    for cmd in lista_comandos:
     if unidecode(cmd.lower().replace(" ", "")) in unidecode(message.content.lower().replace(" ", "")):
        await message.add_reaction ('☀️') 
        await message.add_reaction("<:zcash:1060629265961472080>")
        resposta = random.choice(lista_respostas)
        await message.reply(content=resposta,stickers=[random_sticker])
        break
     
    for cmdn in lista_comandos_n:
        if unidecode(message.content).replace(" ", "").lower().startswith(unidecode(cmdn).replace(" ", "").lower()):
            await message.add_reaction ('🌘') 
            await message.add_reaction("<:zcash:1060629265961472080>")
            resposta = random.choice(lista_respostas_n)
            await message.reply(content=resposta,stickers=[random_sticker])
            break
        
    if unidecode(message.content).replace(" ", "").lower().startswith("zm"):
      await message.add_reaction ('☕')

    if unidecode(message.content).replace(" ", "").lower().startswith("zn"):
      await message.add_reaction ('🍵')

client.run(my_token)       