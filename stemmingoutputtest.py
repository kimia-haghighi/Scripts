import json
import csv
import urllib
import urllib.request as ur

#open and setup output file
outputfile = open('outputstemmingoutputtest.csv', 'w')
testoutput = csv.writer(outputfile)

#header file for output, names data
header = ["SEARCH", "RESPONSE", "CATEGORY"]
testoutput.writerow(header)

query = input ('SOLR Query search: ')
url = "http://localhost:8983/solr/dbNew/select?q=id%3A+"+ query +"&wt=json&indent=true"

r = urllib.request.urlopen('http://localhost:8983/solr/dbNew/select?q=id%3A+'+ query +'&wt=json&indent=true')
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
r.close()


#call JSON data, response and docs
response = data.get("response")
docs = response.get("docs")

numdoc = len(docs)
for i in range (0, numdoc):
	term = docs[i].get("id")
	termin = term.replace(" ", "+")
	category = docs[i].get("category").lower()
	print(termin)

	rowdata = [query, term, category, "RESULTS FROM SEARCH", "CATEGORY RESULTS"]
	print (rowdata)
	testoutput.writerow(rowdata)
	url = "http://localhost:8983/solr/dbNew/select?q=id%3A+"+ termin +"&wt=json&indent=true"
	
	rsearch = urllib.request.urlopen('http://localhost:8983/solr/dbNew/select?q=id%3A+'+ termin +'&wt=json&indent=true')
	datasearch = json.loads(rsearch.read().decode(rsearch.info().get_param('charset') or 'utf-8'))
	rsearch.close()

	responsesearch = datasearch.get("response")
	docssearch = responsesearch.get("docs")

	numsearch = len(docssearch)
	for j in range (0, numsearch):
		term2 = docssearch[j].get("id")
		category2 = docssearch[j].get("category").lower()
		rowdata2 = ["", "", "", term2, category2]
		testoutput.writerow(rowdata2)

outputfile.close()






