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

class MyClient(discord.Client):
  async def on_ready(self):
    await self.wait_until_ready()
    await tree.sync()
    print(f"{self.user} 에 로그인하였습니다!")
intents= discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
    
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
			

client.run("TOKEN HERE")
