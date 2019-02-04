# run with python2
import urllib2
import re
import csv

# to implement --- convert into TSV file. 
def makeLine(filename, obj):
	with open('records.tsv', 'w') as tsvfile:
    	writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
    	writer.writerow(obj.)

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
	return obj



def main():
	print "Running Main ... "
	

	with open("230_scraping_test_all_categories", "r") as myfile:
  		data = myfile.read().decode("utf-8")
	pattern = "\n([\w\W\s]+?)\n\n"
	matches = re.findall(pattern, data)

	for entry in matches:
		obj = createObject(entry)


	


	


if __name__ == "__main__":
	main()