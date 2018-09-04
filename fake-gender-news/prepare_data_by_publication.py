#!/usr/bin/python
# coding=<utf-8>

import subprocess
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import io

path = "/Users/tempuser/Downloads/articles/"
file = path+"articles1.csv"
df = pd.read_csv(file)
#print(df)
#columns=["id","title", "publication", "author", "date", "year", "month", "url", "content"]

g = df.groupby("publication")

#for publication, publication_df in g:
#	print(publication)
#	print(publication_df)

#print(g.get_group("CNN"))
#print(df["publication"].value_counts())
#print(g.groups.keys())

publication_name = g.groups.keys()
counter = 0
for name in publication_name:
	print(name)
	dirname = name.replace(' ', '')
	p = subprocess.Popen("mkdir -p "+path+"singles/"+dirname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	# print out,err
	content = g.get_group(name)["content"].tolist()
	#counter = 0
	for item in range(0,len(content)):
		#counter = counter + 1
		ftxt = open(path+"singles/"+dirname+"/"+str(item)+".txt","w+")
		ftxt.write(content[item].decode('utf-8').encode('ascii','ignore'))
		ftxt.close()
	  


