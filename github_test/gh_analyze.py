#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Analyse the github data
# -------------------------

import re	
import subprocess
import os
from os import walk
import json
from glob import glob

Header = "[Home](https://kelu124.github.io/echommunity/) | [Slack info](https://kelu124.github.io/echommunity/) | [GitHub Info](https://kelu124.github.io/echommunity/github.html)\n\n"

Debug = True

def GetPeople():
	usernames = {}
	with open("./user.log") as users:  
		for user in users:
		    if len(user):
			WhoIs = user.strip().split(";") 
			usernames[WhoIs[0]] = WhoIs[1]
	return usernames

def getJsons(mypath):
	# getChannelLogs("./logs/")
	results = [y for x in os.walk(mypath) for y in glob(os.path.join(x[0], '*.json'))]
	return results

def getRepos(mypath):
	AllJson = getJsons(mypath)
	Repos = []
	for item in AllJson:
		Repos.append(item.split("/")[2])
	Repos = sorted(set(Repos))
	return Repos

def loadEventsJson(path):
	# ForkEvent - PushEvent, PullRequestEvent
	json_data = open(path)
	data = json.load(json_data)
	Events = {"PullRequestEvent":{},"PushEvent":{},"ForkEvent":{},"WatchEvent":{}}
	for temp in data:
	#print temp
	    for typeEvent in ["PullRequestEvent","PushEvent","ForkEvent","WatchEvent"]:
		if temp["type"] == typeEvent:
		    if not temp['actor']["login"] in Events[typeEvent]:
			Events[typeEvent][temp['actor']["login"]] = 1
		    else:
			Events[typeEvent][temp['actor']["login"]] += 1

		#print temp["type"]+" "+ temp['actor']["login"]
	return Events

def loadStarJson(path):
	# ForkEvent - PushEvent, PullRequestEvent
	json_data = open(path)
	Stars = []
	data = json.load(json_data)
	for gazer in data:
		Stars.append(gazer["login"])
	return Stars


if __name__ == '__main__':
	AllRepos = getRepos("./")
	AllJsons = getJsons("./")
	Ppl = GetPeople()

	#loadEventsJson(AllJsons[0])

	GHPage = "\n# GitHub information \n\n"
	for repo in AllRepos:
	    GHPage += "\n## "+repo+"\n\n"
	    GHPage += "### ["+repo+"](https://github.com/echopen/"+repo+")\n\n"
	    if Debug:
		for eachJson in AllJsons:
		    if repo in eachJson:
			if "events.json" in eachJson:
			    content = loadEventsJson(eachJson)
			    if len(content):
				    GHPage += "\n\n#### Events:\n\n"
				    for category in content:
					if len(content[category]):
						GHPage += "* "+category+": "
						for people in content[category]:
							if people in Ppl:
							    who = "["+people+"](./"+Ppl[people]+".md)"
							else:
							    who = people
						GHPage += "_"+who+ "_ ("+str(content[category][people])+"), "
						GHPage += "\n"

			if "stargazers.json" in eachJson:
			    content = loadStarJson(eachJson)
			    for i in range(len(content)):
				if content[i] in Ppl:
				    content[i] = "["+content[i]+"](./"+Ppl[content[i]]+".md)"
			    if len(content):
				    GHPage += "\n\n#### Starred by:\n\n"
				    GHPage += "* Stargazer: _"+ ", ".join(content)+"_\n"		    
				
	f = open("../gh-pages/github.md","w+")
	f.write(Header+GHPage)
	f.close()

