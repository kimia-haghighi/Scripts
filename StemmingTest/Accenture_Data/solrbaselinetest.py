import json
import csv
import urllib
import urllib.request as ur
import time

#open and setup output file
outputfile = open('output.csv', 'w')
testoutput = csv.writer(outputfile)

#open and setup candidates file
inputfile = open('Candidates_All_28.csv', 'r')
testinput =csv.reader(inputfile)
inputlist = list(testinput)

#header file for output, names data
header = ["CID","CANDIDATE TITLE", "CANDIDATE CATEGORY","JID", "JOB TITLE", "JOB CATEGORY", "SCORE", "MAX SCORE", "CATEGORY MATCH"]
testoutput.writerow(header)

#Loop through candidates and search
for master_row in inputlist:

#Replace special characters and spaces in title with '+'
	cid = master_row[0]
	query = master_row[1]
	query2 = master_row[1]
	for letter in query2:
		if ord(letter)>128:
			query2 = query2.replace(letter,"")
	for ch in [' ','-', ',','_','/','&',':',';','(',')','@','.','%']:
		if ch in query2:
			query2 = query2.replace(ch,"+")
	print(query2)
	
	categorydesired = master_row[2]

	#input query and category of query and enter into SOLR
	#query = input('enter query: ')

	url = "http://localhost:8983/solr/dbAccenturesmall/select?q=title%3A+"+ query2 +"&rows=20&fl=*%2C+score&wt=json&indent=true"
	#print(url)

	#run SOLR search and store JSON data
	r = urllib.request.urlopen('http://localhost:8983/solr/dbAccenturesmall/select?q=title%3A+'+ query2 +'&rows=20&fl=*%2C+score&wt=json&indent=true')
	data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
	r.close()


	#call JSON data, response and docs
	response = data.get("response")
	docs = response.get("docs")
	maxscore = response.get("maxScore")

	numdoc = len(docs)

	#loop through docs (search results)
	for i in range (0, numdoc):
		term = docs[i].get("title")
		category = docs[i].get("description")
		score = docs[i].get("score")
		jid = docs[i].get("id")
		print(term)

		if category == categorydesired:
			rowdata = [cid,query, categorydesired,jid, term, category, score, maxscore, "1"]
			testoutput.writerow(rowdata)
		else:
			rowdata = [cid,query, categorydesired,jid, term, category, score, maxscore, "0"]
			testoutput.writerow(rowdata)

outputfile.close()







