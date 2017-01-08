#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Examining slack log files
# Creates the users stats
# -------------------------



from os import walk
import json 
from pprint import pprint
import operator
from operator import itemgetter

import os
from glob import glob
import markdown
import re
import graphviz as gv
import functools
# Wand for SVG to PNG Conversion
from wand.api import library
import wand.color
import wand.image
import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import urllib2

############# Graphing

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')
GraphIntro = digraph()

def Svg2Png(svgfile):
	output_filename = svgfile+'.png'
	input_filename = svgfile+'.svg'

	svg_file = open(input_filename,"r")

	with wand.image.Image() as image:
	    with wand.color.Color('transparent') as background_color:
		library.MagickSetBackgroundColor(image.wand, background_color.resource) 
	    image.read(blob=svg_file.read())
	    png_image = image.make_blob("png32")

	with open(output_filename, "wb") as out:
	    out.write(png_image)

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

styles = {
    'graph': {
        'label': 'the echOmmunity',
	'layout':"twopi",
	'fontsize':"12",
	#'outputorder':'edgesfirst',
	"overlap":"false",
        'rankdir': 'BT',
	"splines":"true",
    }
}

##########

Header = UserPage = "[Home](https://kelu124.github.io/echommunity/)\n\n"

def getThreeInter(Contrib,MainJSON,usernames):
	s = []

	    
	#ListOfReactions = MainJSON["MainData"][k]["reactions"]
	#ListOfReactions = sorted(ListOfReactions, key=operator.itemgetter(1))

	ListOfReactions = sorted(MainJSON["MainData"][Contrib]["reactions"].items(), key=operator.itemgetter(1))

	if len(ListOfReactions):
		ListOfReactions.reverse()

	for i in range(3):
		s.append(usernames[ListOfReactions[i][0]])

	return s

def getChannelLogs(mypath):
	f = []
	for (dirpath, dirnames, filenames) in walk(mypath):
	    f.extend(filenames)
	    good = [x for x in f if (("C" in x) and ".json" in x)]
	    break
	return good

def GetPeople():
	People = []
	usernames = {}
	with open("./logs/users.log") as users:  
		for user in users:
			WhoIs = user.strip().split(";")
			People.append(WhoIs[0])
			usernames[WhoIs[0]] = WhoIs[1]
	return People,usernames

def CreatePage(PeopleID,usernames,PeopleJSON):
	k = 0
	UserPage = Header
	UserPage += "# Some info on __"+usernames[PeopleID]+"__ (_@"+PeopleID+"_)\n\n\n"
	UserPage += "## [Send me a Slack Direct message](https://echopen.slack.com/messages/@"+usernames[PeopleID]+"/)."
	UserPage += "\n\n## Topics of interest\n\n"
	UserPage += "### Posts: \n\nNumber of posts: "+str(PeopleJSON["posts"]["posts"])
	UserPage += "\n\n### Topics:\n\n"

	PPLPost = sorted(PeopleJSON["posts"].items(), key=operator.itemgetter(1))
	if len(PPLPost):
		PPLPost.reverse()

	for post in PPLPost:
	    if post[1]:
		UserPage += "* __"+post[0]+"__: " + str(post[1])+" posts\n"

	UserPage += "\n## Key interactions \n\n"

	PPLReaction = sorted(PeopleJSON["reactions"].items(), key=operator.itemgetter(1))

	if len(PPLReaction):
		PPLReaction.reverse()

	for ppl in PPLReaction:
		UserPage += "* [@"+usernames[ppl[0]]+"](./"+ppl[0]+".md): " + str(ppl[1])+" mention and/or reactions\n"	

	f = open("../gh-pages/"+PeopleID+".md","w+")
	f.write(UserPage)
	f.close()


	return k


##
#
##

PPList, usernames = GetPeople()

MainJSON = {"MainData":{}}
HighScorePostsJSON = []


for PeopleID in PPList:
	TopicsNames = []
	PeopleJSON = {"id":usernames[PeopleID],"reactions":{},"posts":{}}

	for ppl in PPList:
		PeopleJSON["reactions"][ppl]=0
		


	PeopleJSON["posts"]["hardware"]=0	
	PeopleJSON["posts"]["software"]=0
	PeopleJSON["posts"]["legal"]=0
	PeopleJSON["posts"]["medical"]=0
	PeopleJSON["posts"]["design"]=0
	PeopleJSON["posts"]["community"]=0
	PeopleJSON["posts"]["posts"]=0

	AllLogs = getChannelLogs("./logs/")
	
	for JsonFile in AllLogs:
		with open('./logs/'+JsonFile) as data_file:    
		    data = json.load(data_file)
		if PeopleID in data["users"]:
			for mention in data['mentions']:
				if PeopleID == mention["user_id"]:
					PeopleJSON["reactions"][mention["mentioned_user_id"]] += 1

			for reaction in data['reactions']:
				if PeopleID == reaction["user_id"]:
					PeopleJSON["reactions"][reaction["mentioned_user_id"]] += 1

			for UserID in data['users_info']:
			    for i in UserID:
				if (i == PeopleID):
					for subject in UserID[i]:
					    if (int(UserID[i][subject])):
						#print JsonFile+" - "+UserID[i][subject]+" "+subject+" -- "+i
					    	PeopleJSON["posts"][subject] += int(UserID[i][subject])
	Vector = [PeopleID]
	for subject in UserID[i]:
		Vector.append(int(PeopleJSON["posts"][subject]))
		TopicsNames.append(str(subject))
	HighScorePostsJSON.append(Vector)
	#print HighScorePostsJSON

	for ppl in PPList:
		if not PeopleJSON["reactions"][ppl]:
			del PeopleJSON["reactions"][ppl]

	MainJSON["MainData"][PeopleID] = PeopleJSON

	CreatePage(PeopleID,usernames,PeopleJSON)

#print HighScorePostsJSON



MainPage = Header
TopContrib = []
TopContribName = []
MainPage += "# What is it?\n This page shows the different spokepersons for the different themes of the project.\n"

for i in range(len(TopicsNames)):
	Post =  sorted(HighScorePostsJSON,key=itemgetter(i+1))
	Post.reverse()
	MainPage += "\n### "+TopicsNames[i]+"\n\n"
	GraphIntro.node(TopicsNames[i], style="filled", fillcolor="blue", shape="box",fontsize="22")


	for j in range(5):
		MainPage += "* [@"+usernames[Post[j][0]]+"](./"+Post[j][0]+".md): " + str(Post[j][i+1])+" posts\n"
		GraphIntro.node(usernames[Post[j][0]], style="filled", fillcolor="yellow")
		GraphIntro.edge(TopicsNames[i], usernames[Post[j][0]])
		if Post[j][0] not in TopContrib:
			TopContrib.append(Post[j][0])
			TopContribName.append(usernames[Post[j][0]])






#MainPage += "\n\n# Graph of main contributors\n\n ## List of key connections:\n\n"

#print TopContribName
#for i in range(len(TopContrib)):
#	Connected = getThreeInter(TopContrib[i],MainJSON,usernames)
#	MainPage += "* __"+TopContribName[i]+"__: " +", ".join(Connected)+"\n"
#	for connec in Connected:
#		GraphIntro.node(connec, style="filled", fillcolor="yellow")
#		GraphIntro.edge(TopContribName[i], connec)
	



MainPage += "\n## Graph \n\n![](images/Intro.png)"


print MainPage
f = open("../gh-pages/README.md","w+")
f.write(MainPage)
f.close()


json_data = json.dumps(MainJSON, sort_keys=True, indent=4)
f = open("logs/MainUsers.jason","w+")
f.write(json_data)
f.close()

# Creation du graphe


GraphPath = "../gh-pages/images/Intro"
GraphIntro = apply_styles(GraphIntro,styles)

GraphIntro.render(GraphPath)	
Svg2Png(GraphPath)
