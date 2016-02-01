import unittest
import json
import csv
import urllib
import urllib.request as ur

#open and setup output file
outputfile = open('output.csv', 'w')
testoutput = csv.writer(outputfile)

#open and setup input file
inputfile = open('input.csv', 'r')
testinput =csv.reader(inputfile)
inputlist = list(testinput)

#header file for output, names data
header = ["QUERY", "QUERY CATEGORY", "RESPONSE", "RESPONSE CATEGORY", "MATCH"]
testoutput.writerow(header)

class TestSOLRSynonyms(unittest.TestCase):

	def runSOLR(self, querysearch):
		url = "http://localhost:8983/solr/dbNew/select?q=id%3A+"+ querysearch +"&wt=json&indent=true"	
		r = urllib.request.urlopen(url)
		data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
		r.close()
		return data


	def test_SOLRsynonyms(self):
		failcase = "true"
		for master_row in inputlist:
			query = master_row[0]
			categorydesired = master_row[1].lower()
			sumdesired = int(master_row[2])

			data = self.runSOLR(query)

			#call JSON data, response and docs
			response = data.get("response")
			docs = response.get("docs")

			numgood = 0 
			numdoc = len(docs)

			#loop through docs (search results)
			for i in range (0, numdoc):
				term = docs[i].get("id")
				category = docs[i].get("category").lower()

				if category == categorydesired:
					numgood = numgood+1
			#		print (term)
			#		print (numgood)
					rowdata = [query, categorydesired, term, category, "1"]
			#		print (rowdata)
					testoutput.writerow(rowdata)
				else:
					rowdata = [query, categorydesired, term, category, "0"]
					testoutput.writerow(rowdata)
	
#			if sumdesired == numgood:
#				rowsumgood = [query, categorydesired, "", "", "Passed!"]
#				testoutput.writerow(rowsumgood)
#			else:
#				rowsumfail = [query, categorydesired, "", "", "Failed!"]
#				testoutput.writerow(rowsumfail)
#				print("Test failed for query " + query)
#				failcase = "Test Failed" 
			self.assertEqual(sumdesired, numgood)

		outputfile.close()

if __name__ == '__main__':
    unittest.main()
