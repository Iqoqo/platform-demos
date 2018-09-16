#!/usr/bin/python
# coding=<utf-8>

import pandas as pd 
import sys
import gender

#### Algorithm
## 1. Get filename form cmd
# read file names form arg

## 2. Open file in pandas
## 3. Remove not needed cloumns
## 4. get  publishers list
## 5. foreach publisher in list 
## 5.1 write to file publisher stats (name, #ofpublications) 
## 5.2 send content to "gender" (groupby param)

if len(sys.argv) == 2:
    publication_data = sys.argv[1]
else:
    sys.exit('Error! should have parameter')


df = pd.read_csv(publication_data)

g = df.groupby("publication")

publication_name = g.groups.keys()

for name in publication_name:
	print(name)
	dirname = name.replace(' ', '')
	
	content = g.get_group(name)["content"].tolist()
	num_publications = len(content)
	ftxt = open(name+"_publication_detailes"+".txt","w+")
	ftxt.write("number of publications: "+str(num_publications))
	ftxt.close()

	gender.gender_check(content, dirname)
	
	

	
	
