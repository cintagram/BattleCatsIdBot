import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption, SyncWebhook
import json
import os
from enum import Enum
import sys
import numpy
import pandas as pd
import csv
from os import walk
from modules import CONFIG, addjson
from modules.modalclass import TCInputModal, loadsave, makeinfo
import remotepath

class CashUse(Enum):
  활성화="True"
  비활성화="False"
  
async def SendDisallowedMsg(interaction: Interaction):
  embed = discord.Embed(title="사용금지됨", description="서버가 봇 개발자에 의해 사용금지처리되었습니다.\n개발자에게 문의해주새요.")
  await interaction.response.send_message(embed=embed)

def serverpath(id: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), id))

def srvmemberpath(srvid: str, memid: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), srvid), memid))

def loadsrvset_all():
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj
  
def savesrvset_all(data):
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(data))

def loadsrvset(srvid: str):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj[srvid]
  
def savesrvset(srvid: str, newset):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  setobj[srvid] = newset
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(setobj))
  
def chksrvallowed(id: str):
  set = loadsrvset(id)
  if set["UsingAllowed"] == "True":
    return True
  else:
    return False

class MyClient(discord.Client):
  async def on_ready(self):
    await self.wait_until_ready()
    await tree.sync()
    if not os.path.exists(os.path.abspath(os.path.join(os.path.curdir, "bc_saves"))):
      os.mkdir(os.path.abspath(os.path.join(os.path.curdir, "bc_saves")))
      os.mkdir(os.path.abspath(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers")))
    print(f"{self.user} 에 로그인하였습니다!")
intents= discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="sendp", description="시작 버튼을 보냅니다.")
@app_commands.checks.has_permissions(administrator=True)
async def sendbtn(interaction:Interaction):
  button = ui.Button(style=ButtonStyle.green,label="에딧시작",disabled=False)
  view = ui.View(timeout=None)
  view.add_item(button)
  embed = discord.Embed(title="냥코 세이브 백업/복구봇", description="아래 버튼을 눌러 작업을 시작하세요.")
  async def loadfile_cb(interaction:Interaction):
    select = ui.Select(placeholder="세이브파일 선택")
    userid = str(interaction.user.id)
    serverid = str(interaction.guild_id)
    mypath = srvmemberpath(serverid, userid)
    i = -1
    num = 0
    filelist = ""
    text = ""
    filenames=os.listdir(mypath)
    filenamesnum=len(filenames)
    print(filenamesnum)
		#count = len(filenamesnum)
    while i <= filenamesnum:
      i += 1
      if i == filenamesnum or filenames[i] == None:
        print("i is None")
        break
      else:
        if not filenames[i] == "userdata.csv":
          text1 = str(i+1) + ". " + filenames[i] + "\n"
          select.add_option(label=text1, value=str(i+1), description="세이브 파일입니다.")
    view = ui.View()
    view.add_item(select)
    await interaction.response.send_message(ephemeral=True, view=view, delete_after=120.0, content="2분 안에 파일을 선택해주세요.")
    async def loadfile_select_cb(interaction:Interaction):
      filenum = int(select.values[0])
      selectedfile = filenames[filenum-1]
      savefilepath = os.path.join(mypath, selectedfile)
      await loadsave(interaction, savefilepath)
    select.callback=loadfile_select_cb

  async def button_callback(interaction:Interaction):
    set = loadsrvset(str(interaction.guild_id))
    if not chksrvallowed(str(interaction.guild_id)):
      await SendDisallowedMsg(interaction)
    else:
      usr = int(interaction.user.id)
      userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
      if not os.path.exists(userpath):
            embed = discord.Embed(title="처리불가", description="서버DB에 가입되지 않은 사용자입니다.\n`/가입` 명령어로 가입 후 사용해주세요.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
            usr = int(interaction.user.id)
            userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
            typeselect = ui.Select(placeholder="메뉴를 선택해주세요.")
            typeselect.add_option(label="기종변경 코드로 백업", value="tc", description="기종변경 코드로 백업.")
            typeselect.add_option(label="복구하기", value="lf", description="백업본으로 복구")
            view_m = ui.View()
            view_m.add_item(typeselect)
            async def type_cb(interaction: Interaction):
              if typeselect.values[0] == "lf":
                await loadfile_cb(interaction)
              elif typeselect.values[0] == "tc":
                select = ui.Select(placeholder="국가 코드 선택")
                select.add_option(label="kr",value="kr",description="한국판")
                select.add_option(label="en",value="en",description="영미판")
                select.add_option(label="jp",value="jp",description="일본판")
                select.add_option(label="tw",value="tw",description="타이완판")
                view=ui.View()
                view.add_item(select)
                async def select_callback(interaction:Interaction):
                  country = select.values[0]
                  print(country)
                  await interaction.response.send_modal(TCInputModal(country))
                select.callback=select_callback
                await interaction.response.send_message(ephemeral=True,view=view,delete_after=30.0,content="30초 안에 국가코드를 선택해주세요.")
            typeselect.callback=type_cb
            await interaction.response.send_message(view=view_m, delete_after=30.0, ephemeral=True, content="30초 안에 메뉴를 선택해주세요.")
  button.callback=button_callback
  await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="정보", description="유저의 서버정보를 표시합니다.")
async def userinfosend(interaction: Interaction, usr: discord.User):
  srvid = str(interaction.guild_id)
  memid = str(usr.id)
  if os.path.exists(srvmemberpath(srvid, memid)):
    csvpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
    data = open(csvpath, "r", encoding="utf-8").read()
    embed = discord.Embed(title="서버 유저정보입니다.", description=data)
  else:
    embed = discord.Embed(title="서버DB에 가입되지 않은 유저입니다.")
  await interaction.response.send_message(embed=embed)
  
@tree.command(name="가입", description="[필수] 이 서버에서 유저가 가입합니다.")
async def RegisterMem(interaction: Interaction):
  srvid = str(interaction.guild_id)
  memid = str(interaction.user.id)
  if not os.path.exists(srvmemberpath(srvid, memid)):
    os.mkdir(srvmemberpath(srvid, memid))
    csvdata = makeinfo(memid)
    csvpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
    with open(csvpath, "w+", encoding="utf-8") as csvwriter:
      csvwriter.write(csvdata)
    embed = discord.Embed(title="서버 멤버 가입 성공", description="서버DB에 성공적으로 가입되었습니다.")
  else:
    embed = discord.Embed(title="서버DB에 이미 가입되어 있습니다.")
  await interaction.response.send_message(embed=embed)

@tree.command(name="서버등록", description="서버를 등록합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def RegisterSrv(interaction: Interaction):
  srvid = str(interaction.guild_id)
  if not os.path.exists(serverpath(srvid)):
    os.mkdir(serverpath(srvid))
    curset = loadsrvset_all()
    newdata = addjson.adddata(curset, srvid)
    savesrvset_all(newdata)
    embed = discord.Embed(title="서버등록 성공", description="서버가 성공적으로 등록되었습니다.\n꼭 봇 설정을 해주세요.")
  else:
    embed = discord.Embed(title="서버가 이미 등록되어 있습니다.")
  await interaction.response.send_message(embed=embed)

@tree.command(name="bcrgadd", description="???")
async def AddIserkd(interaction: Interaction, userid: str, userpw: str):
    if str(interaction.user.id) in CONFIG.botdev:
        open(os.path.join(remotepath.siteres_path, "bcrg_users.txt"), "a", encoding="utf-8").write("\n"+userid+":"+userpw)
        embed = discord.Embed(title="Sucess")
    else:
        embed = discord.Embed(title="Access Denied")
    await interaction.response.send_message(embed=embed)
    
@tree.command(name="냥코검색", description="냥코 아이디검색")
async def CatSearchCommand(interaction: Interaction, usr_input: str):
	catdb = open("catdb.csv", "r", encoding="utf-8").read().split("\n")
	line_len = len(catdb)
	ctx = []
	for i in range(line_len-1):
		catname = str(catdb[i]).split(",")[0]
		catid = str(catdb[i]).split(",")[1]
		if usr_input in catname:
			ctx.append(str(catname)+": "+str(catid)+"\n")
		else:
			pass
	if len(ctx) == 0:
		embed_body = "검색결과가 없습니다"
	else:
		embed_body = ""
		for k in range(len(ctx)):
			embed_body += ctx[k]
	embed = discord.Embed(title="검색결과", description=embed_body)
	await interaction.response.send_message(embed=embed)
			

client.run(CONFIG.token)
