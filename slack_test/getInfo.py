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

def getLastMessages(sc,chnl,lasttimestamp,item):
    log = ""
    Msgs = sc.api_call("channels.history",channel=chnl,latest=lasttimestamp,count=item)

    Hasmore = json.dumps(Msgs["has_more"])
    Hasmore = json.loads(str(Hasmore))

    Msgs = json.dumps(Msgs["messages"])
    Msgs = json.loads(str(Msgs))

    
    #print Msgs
    for i in Msgs:
	#print i
	if "message" in i['type']:
	    try:
		UserNick = str(i['user'])	 	
	    except KeyError:
		UserNick = "Hyacinthe"

	    OneMessage = re.sub('\|.*>', '>', i['text'])

	    log = i['ts'] +"> @"+UserNick+": "+OneMessage+"\n"+log
    LastTimeStamp = i['ts']
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
		print i
		print i['name']
                print (i['profile']['real_name'])   

def getChannelHistory(sc,ChannelID):
    LastTimeStamp = ""
    LogChannel = ""
    StillMoreMessages = True
    while StillMoreMessages:
    	Results = getLastMessages(sc,ChannelID,LastTimeStamp,"100") # general channel for echopen
	LogChannel =  Results[1]+LogChannel
	LastTimeStamp = Results[2]
	StillMoreMessages = Results[3]
   	print Results[1]
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
    #display_users(sc,users)
    # get last 10 messages
    for myCanal in OurChannels:
	print "=== Going for "+ myCanal
        getChannelHistory(sc,myCanal)


main()





