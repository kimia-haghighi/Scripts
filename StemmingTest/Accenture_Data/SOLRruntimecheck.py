import json
import csv
import urllib
import urllib.request as ur
import time
import statistics

time0 = time.time()
#open and setup candidates file
inputfile = open('Candidates_All_500.csv', 'r')
print("yup1")
testinput = csv.reader(inputfile)
inputlist = list(testinput)
print("yup2")


looptimes = []
#Loop through candidates and search
for master_row in inputlist:
	loopstart = time.time()
#Replace special characters and spaces in title with '+'
	cid = master_row[0]
	query = master_row[1]
	query2 = master_row[1]
	print(query)
	for letter in query2:
		if ord(letter)>128:
			query2 = query2.replace(letter,"")
	for ch in [' ','-', ',','_','/','&','\n','\r',':',';','(',')','@','.','%','?','#']:
		if ch in query2:
			query2 = query2.replace(ch,"+")
	
	categorydesired = master_row[2]

	#input query and category of query and enter into SOLR
	#query = input('enter query: ')

	url = "http://localhost:8983/solr/dbAccenture/select?q=title%3A+"+ query2 +"&rows=20&fl=*%2C+score&wt=json&indent=true"
	#print(url)

	#run SOLR search and store JSON data
	r = urllib.request.urlopen('http://localhost:8983/solr/dbAccenture/select?q=title%3A+'+ query2 +'&rows=20&fl=*%2C+score&wt=json&indent=true')
	data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
	r.close()


	#call JSON data, response and docs
	response = data.get("response")
	docs = response.get("docs")
	maxscore = response.get("maxScore")

	numdoc = len(docs)
#	print(str(numdoc))
	loopend = time.time()
	loopdif = loopend-loopstart
	looptimes.append(loopdif)
	

avgloop = statistics.mean(looptimes)
print("AVERAGE LOOP TIME: "+str(avgloop))
print("STANDARD DEV: "+str(statistics.stdev(looptimes)))
timeend = time.time()
timeout = timeend-time0
print("TOTAL TIME ELAPSED: "+str(timeout)+">>>") 


