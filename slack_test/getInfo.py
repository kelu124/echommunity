#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Reusing
# CTEC 121 / Intro to Programming and Problem Solving
# Lab - Using the Slack API
# by Bruce Elgort, 2016
# -------------------------



# pip install slackclient to install SlackClient library
from slackclient import SlackClient
import json
# the mySlackIDs.py file contains two lines:
# token = "mytoken"
# username = "myusername"
from mySlackIDs import *
import re	
import subprocess
import os

def test_slack(sc):
    # use for debugging
    print("Testing API")
    print(80 * "=")
    print (sc.api_call("api.test"))

def get_channel_info(sc,channel):
    # get info about the channel
    print("Getting Channel Info")
    print(80 * "=")
    print (sc.api_call("channels.info", channel=channel))

def get_list_of_channels(sc):
    print("Getting List of Channels")
    print(80 * "=")
    # get list of channels
    channels = sc.api_call("channels.list")
    channels = json.dumps(channels)
    channels = json.loads(str(channels))
    return channels

def display_channels(channels):
    ListOfChannels = []
    print("Display Channels")
    print(80 * "=")
    print channels 
    for i in channels['channels']:
        print("Channel:",i['name'],i['id'])

	if i['is_general']:
		print "General COMMZ "+i['id']
	if (not i['is_archived']) and (not ("newsfeed" in i['name'])) and (not ("open_calendar" in i['name'])):
		ListOfChannels.append(i['id'])
		print "Adding "+i['name']
    return ListOfChannels

def post_message(sc,text,channel,icon_url,username):
    print("Posting Message to Slack")
    print(80 * "=")
    # post a message into the #general channel
    print (sc.api_call("chat.postMessage",channel=channel,text=text,username=username,icon_url=icon_url,unfurl_links="true"))

def delete_message(sc,tmstp,channel):
    print (sc.api_call("chat.delete",channel=channel,ts=tmstp))	

def getLastMessages(sc,chnl,lasttimestamp,item,update):
    log = ""

    if not update:
    	Msgs = sc.api_call("channels.history",channel=chnl,latest=lasttimestamp,count=item)
    else:
        Msgs = sc.api_call("channels.history",channel=chnl,oldest=lasttimestamp,count=item)


    try:
	Hasmore = json.dumps(Msgs["has_more"])
	Hasmore = json.loads(str(Hasmore))
    except KeyError:
	Hasmore = 0
	
    try:
    	Msgs = json.dumps(Msgs["messages"])
    	Msgs = json.loads(str(Msgs))
    except KeyError:
	Msgs = []
    print Msgs
    LastTimeStamp = 0

    if len(Msgs):
	    for oneMsg in Msgs:
		#print i
		WhoReacted = []
		if "message" in oneMsg['type']:
		    try:
			UserNick = str(oneMsg['user'])	 	
		    except KeyError:
			UserNick = "Hyacinthe"

		    OneMessage = re.sub('\|.*>', '>', oneMsg['text'])
		    OneMessage = OneMessage.replace('\n',' ')
		    OneMessage = OneMessage.replace('\t',' ')
		    OneMessage = OneMessage.replace('\r',' ')



		    try:
			Reactions = oneMsg['reactions']	
		    	Reactions = json.dumps(Reactions)
		    	Reactions = json.loads(Reactions)
		    except KeyError:
			Reactions = []
		    if len(Reactions):
 		    	print Reactions
			for reac in Reactions:
				print reac
				for user in reac['users']:
					WhoReacted.append("@"+user)
		    if len(Reactions):
			log = oneMsg['ts'] +"> @"+UserNick+": "+OneMessage+" (reactions: "+",".join(WhoReacted)+")\n"+log
			print ",".join(WhoReacted)
		    else:
			log = oneMsg['ts'] +"> @"+UserNick+": "+OneMessage+"\n"+log
	    LastTimeStamp = oneMsg['ts']

    log = log.encode("utf8")
    return Msgs,log,LastTimeStamp,Hasmore


def get_users(sc):
    print("Get Users")
    print(80 * "=")
    #call the users.list api call and get list of users
    users = (sc.api_call("users.list"))
    users = json.dumps(users)
    users = json.loads(str(users))
    return users

def createUsers(sc,users):
    print("Create User List")
    print(80 * "=")
    List=[]
    for i in users['members']:
 	List.append(i['id'])

    f = open("logs/users.log","w+")
    f.write("\n".join(List))
    f.close()

    return List

def display_users(sc,users):
    print("User List")
    print(80 * "=")
    # display active users
    for i in users['members']:
        # don't display slackbot
        if i['profile']['real_name'] != "slackbot":
            # don't display deleted users
            if not i['deleted']:
                # display real name
		#print i
		print i['id']
                #print (i['profile']['real_name'])   

def getLastTS(sc,ChannelID):
	filename = "logs/"+ChannelID+".log"
	line = subprocess.check_output(['tail', '-1', filename]).split(">")[0]
	print line
	Results = getLastMessages(sc,ChannelID,line,"100",1)
	LogChannel =  Results[1]
	print LogChannel
	with open(filename, "a") as myfile:
	    myfile.write(LogChannel)



def getChannelHistory(sc,ChannelID):
    LastTimeStamp = ""
    LogChannel = ""
    StillMoreMessages = True
    while StillMoreMessages:
    	Results = getLastMessages(sc,ChannelID,LastTimeStamp,"100",0) # general channel for echopen
	LogChannel =  Results[1]+LogChannel
	LastTimeStamp = Results[2]
	StillMoreMessages = Results[3]
   	print Results[1]
    appendLog(ChannelID,LogChannel)

def appendLog(ChannelID,LogChannel):
    f = open("logs/"+ChannelID+".log","w+")
    f.write(LogChannel)
    f.close()
 
def main():
    # define variables

    icon_url = "icon url for message function"
    channel = "general"
    # connect to Slack
    sc = SlackClient(token)
    # test slack
    test_slack(sc)
    # get channel info
    get_channel_info(sc,channel)
    # get list of channels
    channels = get_list_of_channels(sc)
    # display channels
    OurChannels = display_channels(channels)
    # get users
    users = get_users(sc)
    print sc
    # display users
    createUsers(sc,users)
    # get last 10 messages



    #getChannelHistory(sc,"C04DFTZ7X")

    for myCanal in OurChannels:
	print "=== Going for "+ myCanal
	if not os.path.exists("./logs/"+myCanal+".log"):
		print "Generating logs"
        	getChannelHistory(sc,myCanal)
	else:
		print "Updating logs"
		getLastTS(sc,myCanal)
main()





