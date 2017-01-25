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


AllRepos = getRepos("./")
AllJsons = getJsons("./")


GHPage = "\n# GitHub information \n\n"
for repo in AllRepos:
	GHPage += "\n## "+repo+"\n\n"
	GHPage += "* ["+repo+"](https://github.com/echopen/"+repo+")\n"

#print GHPage
f = open("../gh-pages/github.md","w+")
f.write(GHPage)
f.close()
