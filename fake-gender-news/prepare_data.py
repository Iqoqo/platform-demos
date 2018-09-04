import subprocess
from backports import csv
import io
path = "/Users/tempuser/Downloads/articles/"
index = {"id":1, "content":9}
maxlines = 10
nlines = 1
nsplit = 1 ### should implement

### clean
p = subprocess.Popen("rm -rf "+path+"singles", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
# print out,err
p = subprocess.Popen("mkdir -p "+path+"singles", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
# print out,err


with io.open(path+"articles1.csv", "r", encoding="utf-8") as my_file:
    for row in csv.reader(my_file):
		# print row
		if(nlines>maxlines): break
		id = row[index["id"]]
		if(id=="id"): continue
		print id
		ftxt = open(path+"singles/"+str(id)+".txt","w")
		content = row[index["content"]].encode('ascii',errors='ignore')
		ftxt.write(content)
		ftxt.close()
		nlines += 1

#p = subprocess.Popen("python gender_nodir.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#out, err = p.communicate()
#print out,err
