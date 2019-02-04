# run with python2
# for CS 230 
import urllib2
import re
import csv
import os

# to implement --- convert into TSV file; not working right now. 
def makeLine(filename, obj):
	edited_obj = []
	for value in obj.values():
		edited_obj.append(value.encode('utf-8'))

	return edited_obj
	

	tsvfile.close()

def writeTSV(filename, obj, headers): 
	headers = ['entry'] + headers
	with open(filename, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow(headers)
		for i, entry in enumerate(obj): 
			writer.writerow([i] + entry)

# converts into object/dictionary form
def createObject(entry): 
	# object manipulation for future review, plus features 
	# clean up if necessary ... 
	entry = re.sub(u"(\u201c|\u201d|\u2019)", "'", entry)
	obj = {} 
	pattern = "\*~\*([^a-z]+?)\*~\*([\w\s\W]+?)\*~\*[^a-z]+?\*~\*"
	matches = re.findall(pattern, entry)
	for elem in matches: 
		obj[elem[0]] = elem[1]

	print obj
	return obj



def main():
	filename = "records.tsv"
	if os.path.exists(filename):
  		os.remove(filename)

	print "Running Main ... "
	

	with open("230_scraping_test_all_categories", "r") as myfile:
  		data = myfile.read().decode("utf-8")
	pattern = "\n([\w\W\s]+?)\n\n"
	matches = re.findall(pattern, data)

	all_entries = []
	headers = []
	for i, entry in enumerate(matches):
		obj = createObject(entry)
		headers = obj.keys()
		all_entries.append(makeLine(filename, obj))

	writeTSV(filename, all_entries, headers)


	


	


if __name__ == "__main__":
	main()