import discord
import random
from replit import db
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import discord.ext.commands as commands

client = commands.Bot("!")
DiscordComponents(client)

# send a message with Button components
# involve some attributes
# recieve an interaction

def seleciona_capitao(cap):
  retorno = "Capitão adicionado: " + cap
  if len(db["capitao"]) >= 2:
      retorno = "Os 2 capitães já foram selecionados: \n " + " \n ".join(db["capitao"])

  else:
    if "capitao" in db.keys():
      capitao = db["capitao"]
      capitao.append(cap)
      db["capitao"] = capitao
    else: 
      db["capitao"] = [cap]
    
  return retorno

db["mapaslist"] = ["Infernal Shrines","Cursed Hollow","Dragon Shrine",
             "Battlefield of Eternity","Tomb of Spider Queen",
             "Towers of Doom","Sky Temple","Alterac Pass",
             "Volskaya Foundry","Braxis Holdout","Garden of Terror"]

def mapas():
    options = []
    for i in db["mapaslist"]:
      selectop = SelectOption(label= i, value= i)
      if i in db["banidos"] or i in db["selecionados"]:
        continue
      options.append(selectop)
    return options

def limpa_tudo():
  db["capitao"] = []
  db["banidos"] = []
  db["randomCap"] = ""
  db["randomNotCap"] = ""
  db["banfirst"] = ["",0]
  db["bansecond"] = ["",0]
  db["primeirodraft"] = 0
  db["selecionados"] = []
  db["randomCap"] = ""
  db["randomNotCap"] = ""
  db["banfirst"] = ["",0]
  db["bansecond"] = ["",0]
  db["md"] = 0
  
def naotemdoiscaps():
  if len(db["capitao"]) < 2:
    return True
  else:
    return False

def mapasbans():
    retorno = "Mapas banidos \n ".join(db["banidos"])
    return retorno

@client.command()
async def join(ctx):
    await ctx.channel.send(seleciona_capitao(str(ctx.author)))
    if len(db["capitao"]) >= 2:
      await ctx.channel.send("Digite !draft para começar o draft")

@client.command()
async def reset(ctx):
    limpa_tudo()
    await ctx.channel.send("Tudo foi resetado!")

@client.command()
async def bans(ctx):
    await ctx.channel.send(mapasbans())
  
@client.command()
async def md(ctx):
    await ctx.send("MD", components = [
        [Button(label="MD1", style="1", custom_id="MD1"), 
        Button(label="MD2", style="2", custom_id="MD2"),
        Button(label="MD3", style="3", custom_id="MD3"),
        Button(label="MD5", style="4", custom_id="MD5"),
        Button(label="MD7", style="4", custom_id="MD7")]])
    
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "MD1" or i.custom_id == "MD2" or i.custom_id == "MD3" or i.custom_id == "MD5" or i.custom_id == "MD7")
    if interaction.custom_id == "MD1":
      await interaction.send(content = "Selecionado modo de jogo: MD1" , ephemeral=False)
      db["md"] = 1
    if interaction.custom_id == "MD2":
      await interaction.send(content = "Selecionado modo de jogo: MD2" , ephemeral=False)
      db["md"] = 2
    if interaction.custom_id == "MD3":
      await interaction.send(content = "Selecionado modo de jogo: MD3" , ephemeral=False)
      db["md"] = 3
    if interaction.custom_id == "MD5":
      await interaction.send(content = "Selecionado modo de jogo: MD5" , ephemeral=False)
      db["md"] = 5
    if interaction.custom_id == "MD7":
      await interaction.send(content = "Selecionado modo de jogo: MD7" , ephemeral=False)
      db["md"] = 7
      
@client.command()
async def draft(ctx):
    if db["primeirodraft"] == 0:
      if naotemdoiscaps():
        await ctx.channel.send("Verifique se os capitãoes foram selecionados!")
      else:
        db["randomCap"] = str(random.choice(db["capitao"]))
        if db["capitao"].index(db["randomCap"]) == 0:
          db["randomNotCap"] = db["capitao"][1]
        else:
          db["randomNotCap"] = db["capitao"][0]
        await ctx.send(db["randomCap"]+", escolha Fist Pick ou Mapa", components = [
            [Button(label="Fist Pick", style="3", custom_id="button1"), Button(label="Mapa", style="4", custom_id="button2")]
            ])
        interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1" or i.custom_id == "button2")
        if interaction.custom_id == "button1":
          db["banfirst"][0] = db["randomNotCap"]
          db["bansecond"][0] = db["randomCap"]
          await interaction.send(content = str(interaction.author) + " selecionou First Pick! \n" + db["randomNotCap"] + " digite !ban, para banir um mapa!", ephemeral=False)
        
        if interaction.custom_id == "button2":
          db["banfirst"][0] = db["randomCap"]
          db["bansecond"][0] = db["randomNotCap"]
          await interaction.send(content = str(interaction.author) + " selecionou Mapa! \n" + db["randomCap"] + " digite !ban, para banir um mapa!", ephemeral=False)
    else:
        selecionando = ""
        await ctx.send(str(ctx.author)+", escolha Fist Pick ou Mapa", components = [
            [Button(label="Fist Pick", style="3", custom_id="button1"), Button(label="Mapa", style="4", custom_id="button2")]
            ])
        interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1" or i.custom_id == "button2")
        if interaction.custom_id == "button1":
          if str(interaction.author) == db["capitao"][0]: 
            selecionando = db["capitao"][1] 
          else: 
            selecionando = db["capitao"][0]
          await interaction.send(content = str(interaction.author) + " selecionou First Pick! \n" + selecionando + " digite !select, para selecionar um mapa!", ephemeral=False)
        if interaction.custom_id == "button2":
          if str(interaction.author) == db["capitao"][0]: 
            selecionando = db["capitao"][0] 
          else: 
            selecionando = db["capitao"][1]
          await interaction.send(content = str(interaction.author) + " selecionou Mapa! \n" + selecionando + " digite !select, para selecionar um mapa!", ephemeral=False)

      
@client.command()
async def bolo(ctx):
    lista = ["Você foi infectado ☢️☢️☢️",
             "Tomou mofada do dodeka",
             "Digitou, mofou",
             "Você caiu no conto de Chernoyl",
             "Você acabou de tomar o E do Stukov no Pé",
             "Estamos higienizando nossas formas no rio Tietê, favor esperar",
             "Não estamos atendendo pedidos no momento, estamos recolhendo temperos em Pripyat para melhor atendê-los"
            ]
    await ctx.channel.send(random.choice(lista))

@client.command()
async def hello(ctx):
    await ctx.respond("hello", components = [
        [Button(label="Hi", style="3", emoji = "🥴", custom_id="button1"), Button(label="Bye", style="4", emoji = "😔", custom_id="button2")]
        ], ephemeral=True)
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1" or i.custom_id == "button2")
    if interaction.custom_id == "button1":
      await interaction.send(content = "Felizzzzzzz", ephemeral=False)
    if interaction.custom_id == "button2":
      await interaction.send(content = "Fica tisti não", ephemeral=False)


@client.command()
async def ban(ctx):
    if len(db["banidos"]) < 4:
      await ctx.send("Selecione um mapa para banir:", components = [
          Select(
              placeholder = "Banir um mapa:",
              options = mapas()
          )
      ])
      
    while True:
        try:
            if len(db["banidos"]) < 4:
              select_interaction = await client.wait_for("select_option")
              await select_interaction.send(content = f"{select_interaction.values[0]} foi banido por: "+ str(select_interaction.author), ephemeral = False)
              db["banidos"].append(select_interaction.values[0])
              if len(db["banidos"]) == 4:
                 await ctx.send(db["bansecond"] + " digite !select, para selecionar um mapa.")
              if len(db["banidos"]) < 4:
                if (db["banfirst"][1] < db["bansecond"][1]):
                  db["banfirst"][1] += 1        
                  await ctx.send(db["banfirst"][0] + " digite !ban, para banir outro mapa!")
                else:
                  db["bansecond"][1] += 1
                  await ctx.send(db["bansecond"][0] + " digite !ban, para banir outro mapa!")
            else:
              await ctx.send("Todos os mapas foram banidos! \n Você pode digitar !bans, para ver quais mapas foram banidos \n" + db["randomNotCap"] + " digite !select, para selecionar um mapa!")
              
              db["primeirodraft"] = 1
            break
        except:
            pass

@client.command()
async def select(ctx):
    await ctx.send("Selecione um mapa", components = [
        Select(
            placeholder = "Mapas:",
            options = mapas()
        )
    ])
    while True:
        try:
            select_interaction = await client.wait_for("select_option")
            await select_interaction.send(content = f"{select_interaction.values[0]} selecionado por: "+ str(select_interaction.author), ephemeral = False)
            db["selecionados"].append(select_interaction.values[0])
            break
        except:
            await ctx.send("Algo deu errado")

client.run('TOKEN')

