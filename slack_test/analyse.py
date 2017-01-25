#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Analyse the slack data
# -------------------------

import re	
import subprocess
import os
from os import walk
import json



# List of keywords
Hardware = ["pcb","fpga","electronic","cpld","stm32","arduino","kicad","tgc","adc","hardware","transistor","kit", "boards","redpitaya","dsp","amplifier","quad","cortex","embedded","zynq","altera", "mcu"]
Software = ["android","java","code","python","script","merge","software",'app',"gpu", "machine learning","neural", "deep learning","opengl","scan conversion", "scanconversion"]
Legal = ["patent", "agreement", "cla","licence","license","legal","copyright"] 
Medical = ["doctor", "patient",'médecin',"medical","medecin","health", "healthcare","physician","diagnosis","diabet","pregnant","pregnancy","liver","prevalence", "blood","fetal","midwi","epidemio", "biolog","clinic"]
Design = ["design", "user","interface"] 
Community = ["graph", "community", "communication", "event", "contribution", "contributor", "wiki","documentation","presentation","contributeur","gitbook","onboard","knowledge "]


def getChannelLogs(mypath):
	# getChannelLogs("./logs/")
	f = []
	for (dirpath, dirnames, filenames) in walk(mypath):
	    f.extend(filenames)
	    good = [x for x in f if (("C" in x) and ".log" in x)]
	    break
	return good

def GetUserList(list):
	People = []
	usernames = {}
	with open("./logs/users.log") as users:  
		for user in users:
			WhoIs = user.strip().split(";")
			People.append(WhoIs[0])
			usernames[WhoIs[0]] = WhoIs[1]
	#print usernames
	return People

def OpenLog(logfile):
	f = open("./logs/"+logfile,'r')
	text = f.read()
	f.close()
	return text

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Initiate user list
Users = GetUserList("users.log")
# Get logs
Files = getChannelLogs("./logs/")

MainJSON = {"id":"MainJSON"} 

# Process each log
for ChannelID in Files:
	Log = OpenLog(ChannelID)
	ChannelID = ChannelID.split(".")[0]
	ChannelData = {"channel_id":ChannelID} 
	ChannelUsers = []
	ChannelUserMentions = []
	ChannelUserReactions = []
	ChannelUserInfos = []
	for User in Users:
		CountSoft = 0
		CountHard = 0
		CountLegal = 0
		CountMedical = 0
		CountDesign = 0
		CountCommunity = 0
		for line in Log.split("\n"):
		    if User in line.split(":")[0]:
			for hard in Hardware:
				CountHard += line.lower().count(hard)
			for soft in Software:
				CountSoft += line.lower().count(soft)
			for legal in Legal:
				CountLegal += line.lower().count(legal)
			for medical in Medical:
				CountMedical += line.lower().count(medical)
			for design in Design:
				CountDesign += line.lower().count(design)
			for community  in Community:
				CountCommunity += line.lower().count(community)
			if "(reactions: " in line:
				reacted = find_between( line, "(reactions: ", ")" ).split(",")
				for reac in reacted:
					reactions = {'user_id': User, 'mentioned_user_id': reac.replace("@",""), "ts" : line.split(">")[0]}
					ChannelUserReactions.append(reactions)
			if "<@" in line:
				m = re.findall ( '<@(.*?)>', line, re.DOTALL)
				for mentions in m:
				    if not (User == mentions): 
					mentionsJSON = {'user_id': User, 'mentioned_user_id' : mentions.replace("@",""), "ts" : line.split(">")[0]}
					ChannelUserMentions.append(mentionsJSON)

		UserInfo = {User : {'posts': str(Log.count(User)), 'software': str(CountSoft), 'hardware': str(CountHard), 'legal': str(CountLegal), 'medical': str(CountMedical), 'design': str(CountDesign), 'community': str(CountCommunity)}}


		if Log.count(User):
			ChannelUsers.append(User)


		ChannelUserInfos.append(UserInfo)
		ChannelData["mentions"] = ChannelUserMentions
		ChannelData["reactions"] = ChannelUserReactions

	ChannelData["users_info"] = ChannelUserInfos
	ChannelData["users"] = ChannelUsers
	#dumping channel-wise json
	json_data = json.dumps(ChannelData, sort_keys=True, indent=4)
	f = open("logs/"+ChannelID.split(".")[0]+".json","w+")
	f.write(json_data)
	f.close()

# Dumping main json
#json_data = json.dumps(MainJSON, sort_keys=True, indent=4)
#f = open("logs/MainJSON.json","w+")
#f.write(json_data)
#f.close()
