#!/usr/bin/env python
""" Print all of the clone-urls for a GitHub organization.
It requires the pygithub3 module, which you can install like this::
    $ sudo yum -y install python-virtualenv
    $ mkdir scratch
    $ cd scratch
    $ virtualenv my-virtualenv
    $ source my-virtualenv/bin/activate
    $ pip install pygithub3
Usage example::
    $ python list-all-repos.py
Advanced usage.  This will actually clone all the repos for a
GitHub organization or user::
    $ for url in $(python list-all-repos.py); do git clone $url; done
"""

import pygithub3
import json
import urllib2
import os
import pprint

gh = None

def write_jsons(url,name,filename):

	response = urllib2.urlopen(url).read()
	directory = "./data/"+name+"/"
	f = open(directory+filename,"w") 
	f.write(response)
	f.close() 
	print "Writing: "+directory+filename

def gather_clone_urls(organization, no_forks=False):

    output = []

    all_repos = gh.repos.list(user=organization).all()

    for repo in all_repos:
        result = []
	directory = "./data/"+repo.name+"/"
	if not os.path.exists(directory):
	    os.makedirs(directory)

	#print repo.__dict__ 
	result.append(repo.name)
	result.append(repo.forks)
	result.append(repo.watchers)
	output.append(result)

	write_jsons(repo.forks_url,repo.name,"forks.json")
	write_jsons(repo.events_url,repo.name,"events.json")
	write_jsons(repo.stargazers_url,repo.name,"stargazers.json")
	write_jsons(repo.subscribers_url,repo.name,"suscribers.json")

    return output



if __name__ == '__main__':
    gh = pygithub3.Github()
    if True:
	clone_urls = gather_clone_urls("echopen")
	for items in clone_urls:
	    print items
	
