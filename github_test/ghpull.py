#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Pulls data from GitHub
# to create user stats for the 
# community 
# -------------------------

import pygithub3
import json
import urllib2
import os
import pprint

gh = None

def write_jsons(url,name,filename):
	response = urllib2.urlopen(url).read()
	#json_data = json.dumps(response, sort_keys=True, indent=4)
	directory = "./data/"+name+"/"
	f = open(directory+filename,"w") 
	f.write(response)
	f.close() 
	print "Writing: "+directory+filename
	return 1

def gather_clone_urls(organization, no_forks=False):
    output = []
    all_repos = gh.repos.list(user=organization).all()
    for repo in all_repos:
        result = []
	directory = "./data/"+repo.name+"/"
	# Checks if repertories do not exist yet
	if not os.path.exists(directory):
	    os.makedirs(directory)
  	# Debug outputs
	result.append(repo.name)
	result.append(repo.forks)
	result.append(repo.watchers)
	output.append(result)
	# Write the JSon data
	write_jsons(repo.forks_url,repo.name,"forks.json")
	write_jsons(repo.events_url,repo.name,"events.json")
	write_jsons(repo.stargazers_url,repo.name,"stargazers.json")
	write_jsons(repo.subscribers_url,repo.name,"suscribers.json")
    # Returns a debug list
    return output



if __name__ == '__main__':
    gh = pygithub3.Github()
    if True:
	clone_urls = gather_clone_urls("echopen")
	for items in clone_urls:
	    print items
	
