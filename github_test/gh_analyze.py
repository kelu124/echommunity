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


		print temp["type"]+" "+ temp['actor']["login"]

	return Events


AllRepos = getRepos("./")
AllJsons = getJsons("./")


#loadEventsJson(AllJsons[0])

GHPage = "\n# GitHub information \n\n"
for repo in AllRepos:
	GHPage += "\n## "+repo+"\n\n"
	GHPage += "### ["+repo+"](https://github.com/echopen/"+repo+")\n\n"
	if True:
		for eachJson in AllJsons:
		    print eachJson
		    if repo in eachJson:
			if "events.json" in eachJson:
			    GHPage += "#### Events:\n\n"

		            content = loadEventsJson(eachJson)

			    for category in content:
				GHPage += " * "+category+": "
				for people in content[category]:
				    print people+" - "+category
				    GHPage += people+ "("+str(content[category][people])+"), "
				GHPage += "\n"
			    GHPage += "\n\n"
				
#print GHPage
f = open("../gh-pages/github.md","w+")
f.write(Header+GHPage)
f.close()
