# run with python2
# for CS 230 
import urllib2
import re
import csv
import os

# to implement --- convert into TSV file. 
def makeLine(filename, obj):
	edited_obj = []
	for value in obj.values():
		edited_obj.append(value.encode('utf-8'))

	with open(filename, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
		writer.writerow(['1'] + edited_obj)
		writer.writerow(['2'] + edited_obj)
		writer.writerow(['3'] + edited_obj)

	tsvfile.close()

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


	for i, entry in enumerate(matches):
		obj = createObject(entry)
		makeLine(filename, obj)
		if i == 2:
			break


	


	


if __name__ == "__main__":
	main()