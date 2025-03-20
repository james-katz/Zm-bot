import discord
import os 
import random
from dotenv import load_dotenv
from unidecode import unidecode
from models import *
from peewee import fn
from tabulate import tabulate

load_dotenv()
my_token = os.getenv("DISCORD_TOKEN")

# Função para registrar uma nova interação
def registrar_interacao(user_id):
    try:
        _, created = User.get_or_create(id=user_id)
        if created:
            print(f"Novo usuário registrado: ID do usuário: {user_id}")

        # Cria uma nova interação para o usuário
        interacao = Interacao.create(user_id=user_id)
        print(f"Interação criada para o usuário {user_id}.")
        
        return interacao
    except Exception as e:
        print(f"Erro ao registrar interação: {e}")
        return None

# Função para registrar uma nova premiação
def registrar_premiacao(user_id):
    premiacao = None

    # Verifica se o usuário existe
    user, created = User.get_or_create(id=user_id)
    if user or created:
        # Insere o id do usuário na tabela Award
        premiacao = Premiacao.create(user_id=user.id)
    
    # Apaga a tabela de interações, para iniciar uma nova rodada
    deletar_todas_interacoes()

    # Aparaga as interações do ganhador, assim o usuário vai para o "fim da fila"
    # deletar_interacoes_usuario(user_id)

    return premiacao

# Função para buscar a premiação mais recente no banco de dados
def buscar_ultima_premiacao():
    try:
        return Premiacao.select().order_by(Premiacao.data_premiacao.desc()).get()
    except Premiacao.DoesNotExist:
        # Insere um usuário e uma premiação falsa
        # Assim, é possível contar 15 dias a partir do primeiro uso do bot
        user = User.create(id=0)
        premio = registrar_premiacao(0)
        return premio
    
# Função para gerar a tabela de interações
def gerar_tabela_premicao():
    premiacoes = Premiacao.select()
    dados = []
    for premio in premiacoes:
        dados.append([premio.id, premio.user_id, premio.data_premiacao])
    
    cabecalhos = ["ID", "User ID", "Data da Premiação"]
    
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

# Função para deletar todas as interações de um usuário
def deletar_interacoes_usuario(user_id):
    query = Interacao.delete().where(Interacao.user_id == user_id)
    query.execute()
    print("Todas as interações foram deletadas.")


# Função para pegar um vencedor baseado no número de interações
def selecionar_ganhador():
    # Esse código foi gerado com o auxílo do ChatGPT
    # Fetch all users and their interaction counts
    print("Pegando lista de usuários participantes ...")
    users = (
    User.select(
        User.id,
        fn.COUNT(Interacao.id).alias('interaction_count')
    )
    .join(Interacao, on=(User.id == Interacao.user_id))
    .group_by(User.id)  # Group by user ID
)
    
    # Convert query results to a list of tuples (user_id, interaction_count)
    user_weights = [(user.id, user.interaction_count) for user in users]

    if not user_weights:
        return None  # No users available

    # Extract user IDs and weights
    user_ids, weights = zip(*user_weights)

    # Securely choose a user with weighted probability
    selected_user = random.choices(user_ids, weights=weights, k=1)[0]
    print(f"ID selecionado: {selected_user}")
    return int(selected_user)

def get_top_users(limit=10):
    top_users = (
        User.select(
            User.id,
            fn.COUNT(Interacao.id).alias('interaction_count')
        )
        .join(Interacao, on=(User.id == Interacao.user_id))
        .group_by(User.id)
        .order_by(fn.COUNT(Interacao.id).desc())
        .limit(limit)
    )

    # Format output with rankings
    ranked_users = [
        {"rank": i + 1, "user_id": int(user.id), "interactions": user.interaction_count}
        for i, user in enumerate(top_users)
    ]

    return ranked_users

def get_user_rank(user_id):
    # Get the full ranked list (no limit)
    ranked_users = get_top_users(limit=None)  # Fetch all users, ordered by rank

    # Search for the specific user in the ranked list
    for user in ranked_users:
        if user["user_id"] == user_id:
            return user  # Return user's rank and interaction count

    return None  # User not found

def get_golden_ticket_rank():
# Query to count awards per user and order by highest award count
    awarded_users = (
        User.select(
            User.id,
            fn.COUNT(Premiacao.id).alias('award_count')  # Count number of awards
        )
        .join(Premiacao, on=(User.id == Premiacao.user_id))
        .group_by(User.id)
        .order_by(fn.COUNT(Premiacao.id).desc())  # Order by award count (highest first)
        .limit(10)
    )

    # Format output with rankings
    ranked_awarded_users = [
        {"rank": i + 1, "user_id": int(user.id), "awards": user.award_count}
        for i, user in enumerate(awarded_users)
    ]

    return ranked_awarded_users
# Pega o total de interações do usuário
# def get_user_interaction_count(user_id):
    # return Interacao.select().where(Interacao.user_id == user_id).count()

# Listas de comandos
lista_comandos = ["zm","gm","Good morning","Morning","Gmorning","bom dia", "dia bom","dia","Buenos días","Feliz día","Buen día","Annyeonghaseyo","안녕하세요","Joh eun achim","좋은 아침","Annyeong hasimnikka","안녕하십니까","Buongiorno","Buon mattino","Buona giornata"]
lista_comandos_n = ["zn","gn","Good night","Nighty night","Boa noite","Boa noitinha","noite","Buenas noches","annyeonghi jumuseyo","안녕히 주무세요","gutbam","굿밤","Buona notte"]
lista_respostas = ["Zm Zcasher","Zm zfriend","Zm Zeep", "Zm Zepe","gm Zfriend", "gm Zcasher", "gm Zeep", "gm Zepe"]
lista_respostas_n = ["Zn Zcasher","Zn zfriend","Zn Zeep", "Zn Zepe","gn Zfriend", "gn Zcasher" "gn Zeep", "gn Zepe"]

PALAVRA_GATILHO_TABELA = ["tabela"]
PALAVRA_GATILHO_DELETAR = ["deletar"]
PALAVRA_GATILHO_INTERACOES = ["cccr", "!zm"]
PALAVRA_GATILHO_RANK = ["!zmrank"]
PALAVRA_GATILHO_RANK_GT = ["!gt"]

total_gatilhos = lista_comandos + lista_comandos_n

next_prize = 15

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print(f'Estou pronto! zm meu ID é {client.user.id}')
    
@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return 

    replied = False
    awarded = False
    
    sticker_d = [1189750838722301952, 1213028820320522280]
    sticker_n = [1187411015642648737, 1187415785761669120, 1189751078292553748, 1189751207661682758, 1212889809283194900]
    stickers_ian = [1235994545448288336, 1260616198735925248]
    
    portuguese_role = message.guild.get_role(979779292026261554)
    zcash_role = message.guild.get_role(1078741799306268727)
    
    sticker_list = await message.guild.fetch_stickers()
    random_sticker = random.choice(sticker_list)

    # Vito
    if message.author.id == 564292989984440350:
        random_ian = random.choice(stickers_ian)
        random_sticker = await message.guild.fetch_sticker(random_ian)    

    if message.channel.id == 1080161118384820358 or message.channel.id == 1094939925721403443:
    # if message:
        # Pega a última premiação guardada no banco de dados
        ultima_premiacao = buscar_ultima_premiacao() 
        global next_prize

        for cmd in lista_comandos:
            if unidecode(cmd.lower().replace(" ", "")) in unidecode(message.content.lower().replace(" ", "")):
                replied = True
                # Se o usuário não for da equipe Zcash, verificar a possibilidade de enviar um prêmio
                if portuguese_role in message.author.roles and zcash_role not in message.author.roles:
                    if ultima_premiacao:
                        diferenca = datetime.now() - ultima_premiacao.data_premiacao                                                
                        if diferenca.days >= next_prize:
                        # diferenca_minutos = diferenca.total_seconds() / 60  # Convert seconds to minutes
                        # if diferenca_minutos >= next_prize:
                            ganhador_id = selecionar_ganhador()
                            if ganhador_id == message.author.id and int(ultima_premiacao.user_id.id) != message.author.id:
                                registrar_premiacao(ganhador_id)
                                await message.reply(content=f"Parabéns, você ganhou um prêmio!\n Em breve um membro", file=discord.File('./imagem/Golden_Ticket.png'))                
                                awarded = True
                            else:
                                print("Não é pra você")
                        
                # Caso contrário, enviar uma mensagem normal de bom dia (incluindo equipe zcash)
                if not awarded:
                    # Registra a interação do usuário
                    registrar_interacao(message.author.id)
                    
                    while random_sticker.id in sticker_n:
                        random_sticker = random.choice(sticker_list)                     
                    try:
                        await message.add_reaction('<:SunIcon:1189330981866451035>') 
                        resposta = random.choice(lista_respostas)
                        await message.reply(content=resposta, stickers=[random_sticker])
                        # await message.reply(content=resposta)
                    except Exception as e:
                        print('Erro ao tentar adicionar reação:', e)                
                break          

        for cmdn in lista_comandos_n:
            if replied:
                break 

            if unidecode(cmdn.lower().replace(" ", "")) in unidecode(message.content.lower().replace(" ", "")):
                # Se o usuário não for da equipe Zcash, verificar a possibilidade de enviar um prêmio
                if portuguese_role in message.author.roles and zcash_role not in message.author.roles:
                    if ultima_premiacao:
                        diferenca = datetime.now() - ultima_premiacao.data_premiacao                                                
                        if diferenca.days >= next_prize:
                            ganhador_id = selecionar_ganhador()
                            if ganhador_id == message.author.id and int(ultima_premiacao.user_id.id) != message.author.id:
                                registrar_premiacao(ganhador_id)
                                await message.reply(content="Parabéns, você ganhou um prêmio!", file=discord.File('./imagem/Golden_Ticket.png'))                
                                awarded = True
                            else:
                                print("Não é pra você")
                
                # Caso contrário, enviar uma mensagem normal de boa noite
                if not awarded:  
                    # Registra a interação do usuário
                    registrar_interacao(message.author.id)
                    
                    while random_sticker.id in sticker_d:
                        random_sticker = random.choice(sticker_list) 

                    try:
                        await message.add_reaction('<:MoonIcon:1189330979156930702>') 
                        resposta = random.choice(lista_respostas_n)
                        await message.reply(content=resposta, stickers=[random_sticker])
                    except Exception as e:
                        print('Erro ao tentar adicionar reação:', e)                
                break 
        
        if "zm" in unidecode(message.content).replace(" ", "").lower():
            try:
                await message.add_reaction('<:Coffee01:1189301205021769758>') 
            except Exception as e:
                print('Erro ao tentar adicionar reação:', e)    
        elif "zn" in unidecode(message.content).replace(" ", "").lower():
            try:
                await message.add_reaction('<:Tea01:1189331115106902027>') 
            except Exception as e:
                print('Erro ao tentar adicionar reação:', e)          
        
    # Gerar e enviar tabela de interações
    for palavra in PALAVRA_GATILHO_TABELA:
        # if palavra in message.content.lower() and message.channel.id == 1094939925721403443:
        if palavra in message.content.lower():
            tabela = gerar_tabela_premicao()
            if tabela:
                await enviar_tabela_como_arquivo(message.channel, tabela)
            else:
                await message.channel.send("Nenhuma interação registrada até agora.")
            break

    for palavra in PALAVRA_GATILHO_INTERACOES:
        if palavra == message.content.lower():
            user_rank = get_user_rank(message.author.id)
            if user_rank:
                myEmbed = discord.Embed(title="Your ZM ranking", description="See how many times you interacted with ZM", color=0xffff00)
                myEmbed.set_author(name=client.user.display_name, icon_url=client.user.avatar.url, url=None)
                myEmbed.add_field(name="Rank", value=f"#{user_rank['rank']}", inline=True)
                myEmbed.add_field(name="Number of interactions", value=f"{user_rank['interactions']}", inline=True)
                myEmbed.set_footer(text="Interactions are cleared every new Golden Ticket cycle.")
            else:
                await message.reply("You don't have any interactions yet.")

            await message.reply(embed=myEmbed)

    # Gerar o embed do rank de interações
    for palavra in PALAVRA_GATILHO_RANK:
        if palavra == message.content.lower():
            description = ""
            ranked = get_top_users()
            for user in ranked:
                description += f"- # {user['rank']} <@{user['user_id']}>: {user['interactions']} interactions.\n"
            myEmbed = discord.Embed(title="Global ZM ranking", description=f"See the ZM leaders:\n{description}", color=0xffff00)
            myEmbed.set_author(name=client.user.display_name, icon_url=client.user.avatar.url, url=None)    
            myEmbed.set_footer(text="Interactions are cleared every new Golden Ticket cycle.")

            await message.reply(embed=myEmbed)

    for palavra in PALAVRA_GATILHO_RANK_GT:
        if palavra == message.content.lower():
            description = ""
            gt_rank = get_golden_ticket_rank()
            for user in gt_rank:
                if(user['user_id']) != 0:
                    description += f"- # {user['rank']} <@{user['user_id']}>: {user['awards']} Golden {'Tickets' if user['awards'] > 1 else 'Ticket'}.\n"
            myEmbed = discord.Embed(title="Top 10 Golden Ticket Winners", description=f"Golden Ticket leaderboard:\n{description}", color=0xffff00)
            myEmbed.set_author(name=client.user.display_name, icon_url=client.user.avatar.url, url=None)    
            # myEmbed.set_footer(text="Interactions are cleared every new Golden Ticket cycle.")
            
            await message.reply(embed=myEmbed)

    # Deletar interações ID de permissao dev cassia 
    if message.author.id == 1094939925721403443:
        for palavra in PALAVRA_GATILHO_DELETAR:
            if palavra in message.content.lower() and message.channel.id == 1173374501086572675:
                deletar_todas_interacoes()
                await message.channel.send("Todas as interações foram deletadas.")
                break

client.run(my_token)