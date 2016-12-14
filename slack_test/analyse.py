#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Examining slack log files
# -------------------------

import re	
import subprocess
import os
from os import walk
import json

data = {}

Hardware = ["pcb","fpga","electronic","cpld","stm32","arduino","kicad"]
Software = ["android","java","code"]
Legal = ["patent", "agreement", "cla"] 
Medical = ["doctor", "patient"]
Design = ["design", "user"] 
Community = ["graph", "community", "communication", "event", "contribution", "contributor", "wiki"]

def getChannelLogs(mypath):
	# getChannelLogs("./logs/")
	f = []
	for (dirpath, dirnames, filenames) in walk(mypath):
	    f.extend(filenames)
	    good = [x for x in f if (("C" in x) and ".log" in x)]
	    break
	return good

def GetUserList(list):
	f = open("./logs/"+list,'r')
	text = f.read().split("\n")
	f.close()
	return text

def OpenLog(logfile):
	f = open("./logs/"+logfile,'r')
	text = f.read()
	f.close()
	return text



Users = GetUserList("users.log")
Files = getChannelLogs("./logs/")
print Files
for ChannelID in Files:
	
	Log = OpenLog(ChannelID)
	data["Stats"] = [ ]

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

		entry = {'user': User, 'info' : {'posts': str(Log.count(User)), 'software': str(CountSoft), 'hardware': str(CountHard), 'legal': str(CountLegal), 'medical': str(CountMedical), 'design': str(CountDesign), 'community': str(CountCommunity)}}
		data["Stats"].append(entry)
		print User+": "+str(Log.count(User))


	json_data = json.dumps(data, sort_keys=True, indent=4)
	print 'JSON: ', json_data


	f = open("logs/"+ChannelID+".json","w+")
	f.write(json_data)
	f.close()
