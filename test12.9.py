import json
with open('Data/test12.9.txt') as json_data:
	d = json.load(json_data)
	json_data.close()
with open('Data/test12.9_2.txt') as json_data2:
	d2 = json.load(json_data2)
	json_data2.close()
        
	response = d.get("response")
	docs =response.get("docs")
	countreal = response.get("numFound")

	response2 = d2.get("response")
	docs2 = response2.get("docs")
	countreal2 = response2.get("numFound")
	
	print(countreal-countreal2)
