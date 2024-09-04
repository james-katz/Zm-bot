import discord
import os
import random
from dotenv import load_dotenv
from unidecode import unidecode
from peewee import *
from datetime import datetime, timedelta
from tabulate import tabulate

load_dotenv()
my_token = os.getenv("DISCORD_TOKEN")

# Configuração do banco de dados
db = SqliteDatabase("banco.sqlite3")

class Interacao(Model):
    id = AutoField() 
    user_id = IntegerField()  
    data_interacao = DateTimeField(default=datetime.now)

    class Meta:
        database = db  

db.create_tables([Interacao])

# Função para registrar uma nova interação
def registrar_interacao(user_id):
    try:
        interacao, created = Interacao.get_or_create(user_id=user_id)
        if not created:
            interacao.data_interacao = datetime.now()
            interacao.save()
            print(f"Interação atualizada: ID do usuário: {interacao.user_id}, Nova data: {interacao.data_interacao}")
        else:
            print(f"Nova interação registrada: ID do usuário: {interacao.user_id}, Data: {interacao.data_interacao}")
    except Exception as e:
        print(f"Erro ao registrar interação: {e}")

# Função para buscar a interação mais recente no banco de dados
def buscar_ultima_interacao():
    try:
        return Interacao.select().order_by(Interacao.data_interacao.desc()).get()
    except Interacao.DoesNotExist:
        return None
    
# Função para gerar a tabela de interações
def gerar_tabela_interacoes():
    interacoes = Interacao.select()

    dados = []
    for interacao in interacoes:
        dados.append([interacao.id, interacao.user_id, interacao.data_interacao])
    
    cabecalhos = ["ID", "User ID", "Data da Interação"]
    
    return tabulate(dados, headers=cabecalhos, tablefmt="grid")

# Função para enviar a tabela de interações como arquivo
async def enviar_tabela_como_arquivo(channel, tabela):
    with open("tabela_interacoes.txt", "w") as f:
        f.write(tabela)
    
    await channel.send(file=discord.File("tabela_interacoes.txt"))

# Nova função para deletar todas as interações
def deletar_todas_interacoes():
    query = Interacao.delete()
    query.execute()
    print("Todas as interações foram deletadas.")


lista_comandos = ["zm","gm","Good morning","Morning","Gmorning","bom dia ", "dia bom","dia","Buenos días","Feliz día","Buen día","Annyeonghaseyo","안녕하세요","Joh eun achim","좋은 아침","Annyeong hasimnikka","안녕하십니까","Buongiorno","Buon mattino","Buona giornata"]

lista_comandos_n = ["zn","gn","Good night","Nighty night","Boa noite","Boa noitinha","noite","Buenas noches","annyeonghi jumuseyo","안녕히 주무세요","gutbam","굿밤","Buona notte"]

lista_respostas = ["Zm Zcasher","Zm zfriend","gm Zfriend", "gm Zcasher"]

lista_respostas_n = ["Zn Zcasher","Zn zfriend","gn Zfriend", "gn Zcasher"]

PALAVRA_GATILHO_TABELA = ["tabela"]
PALAVRA_GATILHO_DELETAR = ["deletar"]

total_gatilhos = lista_comandos + lista_comandos_n

contador = 0

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print (f'estou pronto!zm meu ID é {client.user.id}')
    
@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return 
    
    replied = False 
    awarded = False

    global contador
    target = random.randint(200,250)
    if(contador >= target):
        print("ganhou!!!!")
        awarded = True


    print(f"Contador: {contador} | Target: {target}")
    
    
    

    sticker_d = [1189750838722301952, 1213028820320522280]
    sticker_n = [1187411015642648737, 1187415785761669120, 1189751078292553748, 1189751207661682758, 1212889809283194900]
    stickers_ian = [1235994545448288336, 1260616198735925248]
    
    

    portuguese_role = message.guild.get_role(979779292026261554)
    zcash_role = message.guild.get_role(1078741799306268727)
    dev_id = 1095310806385700905
    
    
    sticker_list = await message.guild.fetch_stickers()
    random_sticker = random.choice(sticker_list)
    
    if message.author.id == 564292989984440350:
      random_ian = random.choice(stickers_ian)
      random_sticker = await message.guild.fetch_sticker(random_ian)

    # Verifica se há um prêmio para enviar
    ultima_interacao = buscar_ultima_interacao()  

    if message.channel.id == 1080161118384820358:
     for cmd in lista_comandos:
        if unidecode(cmd.lower().replace(" ", "")) in unidecode(message.content.lower().replace(" ", "")):
            replied = True
            if awarded and portuguese_role in message.author.roles and zcash_role not in message.author.roles and message.author.id != dev_id:
                if ultima_interacao:
                        diferenca = datetime.now() - ultima_interacao.data_interacao
                        if diferenca.days >= 15:
                            if ultima_interacao.user_id != message.author.id:
                                await message.reply(content="Parabéns, você ganhou um prêmio!", file=discord.File('./imagem/Golden_Ticket.png'))                
                                contador = 0                
                                return
                            else:
                                print("Usuário já ganhou o prêmio recentemente. Nenhum prêmio enviado.")
                        else:
                            print("Menos de 15 dias desde o último prêmio. Nenhum prêmio enviado.")    
                else:  
                    await message.reply(content="Parabéns, você ganhou um prêmio!", file=discord.File('./imagem/Golden_Ticket.png'))                
                    registrar_interacao(message.author.id)
                    contador = 0                
                    return 
            else:
                contador += 1     
        
            while random_sticker.id in sticker_n:
                  random_sticker = random.choice(sticker_list) 
        
            try:
                await message.add_reaction ('<:SunIcon:1189330981866451035>') 
                resposta = random.choice(lista_respostas)
                await message.reply(content=resposta,stickers=[random_sticker])
            except:
                print ('erro ao tentar add reação')
            
            break

     for cmdn in lista_comandos_n:
        if replied:
            break 

        if unidecode(cmdn.lower().replace(" ", "")) in unidecode(message.content.lower().replace(" ", "")):
            if awarded and portuguese_role in message.author.roles and zcash_role not in message.author.roles and message.author.id != dev_id: 
                if ultima_interacao:
                        diferenca = datetime.now() - ultima_interacao.data_interacao
                        if diferenca.days >= 15:
                            if ultima_interacao.user_id != message.author.id:
                                await message.reply(content="Parabéns, você ganhou um prêmio!", file=discord.File('./imagem/Golden_Ticket.png'))
                                registrar_interacao(message.author.id)
                                contador = 0                
                                return                
                            else:
                                print("Usuário já ganhou o prêmio recentemente. Nenhum prêmio enviado.")
                        else:
                            print("Menos de 15 dias desde o último prêmio. Nenhum prêmio enviado.")
                else:  
                        await message.reply(content="Parabéns, você ganhou um prêmio!", file=discord.File('./imagem/Golden_Ticket.png'))                
                        registrar_interacao(message.author.id)
                        contador = 0                
                        return  
            else:
                contador += 1  
            
            while random_sticker.id in sticker_d:
                random_sticker = random.choice(sticker_list)            
           
            try:
             await message.add_reaction ('<:MoonIcon:1189330979156930702>') 
             resposta = random.choice(lista_respostas_n)
             await message.reply(content=resposta,stickers=[random_sticker])
            except:
                print ('erro ao tentar add reação')
        
            break

     if "zm" in unidecode(message.content).replace(" ", "").lower():
        try :
         await message.add_reaction ('<:Coffee01:1189301205021769758>') 
        except :
            print ('erro ao tentar add reação')    
     elif "zn" in unidecode(message.content).replace(" ", "").lower():
        try :
         await message.add_reaction ('<:Tea01:1189331115106902027>') 
        except :
            print ('erro ao tentar add reação') 
    # Gerar e enviar tabela de interações
    for palavra in PALAVRA_GATILHO_TABELA:
        if palavra in message.content.lower() and message.channel.id == 1094939925721403443:
            tabela = gerar_tabela_interacoes()
            if tabela:
                await enviar_tabela_como_arquivo(message.channel, tabela)
            else:
                await message.channel.send("Nenhuma interação registrada até agora.")
            break

    # Deletar interações ID de permissao dev cassia 
    if message.author.id == 1094939925721403443:
        for palavra in PALAVRA_GATILHO_DELETAR:
            if palavra in message.content.lower() and message.channel.id == 1173374501086572675:
                deletar_todas_interacoes()
                await message.channel.send("Todas as interações foram deletadas.")
                break

client.run(my_token)