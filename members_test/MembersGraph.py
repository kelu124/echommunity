#echOpen processing communitiy
#usage : python creategraphe.py tweets.tsv

from math import *
import sys
import string
import re
import unicodedata

import os
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

try:
    sys.argv[1]
except NameError:
    eptFile = 'Missing an arg'
else:
    eptFile = sys.argv[1]

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')
GraphCommunity = digraph()

styles = {
    'graph': {
        'label': 'the community',
	'layout':"fdp",
	'fontsize':"4",
	'outputorder':'edgesfirst',
	#"overlap":"false",
	#"splines":"true",
	#"size":"11.7,8.3!",
	#"size":"0.75",
	"nodesep":"0.75",
"ranksep":"0.75",
        'rankdir': 'BT',
    }
}

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


ListOfSkills = []
with open(eptFile, 'r') as Tweets:
	for line in Tweets:
		line = unicode(line,'utf-8')
		line = unicodedata.normalize('NFD', line).encode('ascii', 'ignore')     
		line = line.lower()
		line = line.split(';')
		if line[1]:
			Prenom = line[0]+" "+line[1][0]+"."
		else:
			Prenom = line[0]
		del line[-1]
		#print Prenom	
		GraphCommunity.node(Prenom,style="rounded,filled", fillcolor="yellow", penwidth="0",fontsize="28")	
		for i in range(7):
			del line[0]
		line = filter(None, line) 
		#print line	
		for Skill in line:
		    GraphCommunity.node(Skill.strip(),style="rounded,filled", fillcolor="white", penwidth="0",fontsize="14")
		    GraphCommunity.edge(Prenom, Skill.strip(),weight="3", color="grey",style="dashed",arrowType="None")
		    ListOfSkills.append(Skill.strip())

GraphCommunity = apply_styles(GraphCommunity, styles)

GraphCommunity.render("viewme")
Svg2Png("viewme")

SetOfSkills = sorted(list(set(ListOfSkills)))
for skill in SetOfSkills:
	print skill
####









