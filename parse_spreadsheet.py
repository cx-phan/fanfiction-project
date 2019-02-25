# run with python2
# for CS 230 
import urllib2
import re
import csv
import os
import sys

# placeholder function for any data processing ... 
def interpretObject(obj, headers): 
	for i, entry in enumerate(obj):
		print headers[i] + ": " + entry

# takes dictionary & converts all values into an array to write into a TSV file
def makeLine(filename, obj):
	edited_obj = []
	for value in obj.values():
		edited_obj.append(value.encode('utf-8'))

	return edited_obj

# takes the header, all entries and writes into a TSV (filename)
def writeTSV(filename, obj, headers): 
	headers = ['entry'] + headers
	with open(filename, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow(headers)
		for i, entry in enumerate(obj): 
			writer.writerow([i] + entry)

# converts into object/dictionary form, from string entry
def createObject(entry): 
	# clean up if necessary ... 
	entry = re.sub(u"(\u201c|\u201d|\u2019)", "'", entry)
	obj = {} 
	pattern = "\*~\*([^a-z]+?)\*~\*([\w\s\W]+?)\*~\*[^a-z]+?\*~\*"
	matches = re.findall(pattern, entry)

	# added delineation for explicit tag
	for elem in matches: 
		if elem[0] == 'TAGS':
			array = elem[1].split(",")
			obj['MAINTAG'] = array[0]
			obj[elem[0]] = ','.join(array[1:])
		else:
			obj[elem[0]] = elem[1].strip(',')

	print obj['TITLE'] + " now printed."
	return obj


def main():
	print "put in values for first and second argument, 1 ????"
	
	values = 12
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	filename = "./data/records:" + str(start) +"-" + str(end) +".tsv"
	openfile = "./data/230_scraping_test_all_categories_range:" + str(start) + "-" + str(end)
    
	if os.path.exists(filename):
  		os.remove(filename)

	with open(openfile, "r") as myfile:
  		data = myfile.read().decode("utf-8")
	
	# data to parse out all types 
	pattern = "(\*~\*[\w\W\s]+?\*~\*\n\n)"
	matches = re.findall(pattern, data)

	all_entries = []
	headers = []
	for i, entry in enumerate(matches):
		obj = createObject(entry)
		headers = obj.keys()
		all_entries.append(makeLine(filename, obj))

		# debugging: check here & remove later
		if len(obj.values()) != values:
			print "ERROR HERE, LEN IS " + str(len(obj.values()))
			for key in obj.keys():
				val = obj[key]
				print key + ": " + val
			
	writeTSV(filename, all_entries, headers)


	


	


if __name__ == "__main__":
	main()