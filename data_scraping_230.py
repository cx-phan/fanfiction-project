#run with python2
import urllib2
import re

#opens url with 20 fluff/angst search results
#adds tags from the search result page
#passes url of the story to addText
def scrapeURL(url, file):
    response = urllib2.urlopen(url)
    page_source = response.read()
    lines = page_source.split("\n")
    currentWorkID = 0
    print "Length is" + str(len(lines))
    for line in lines:
        possID = re.findall(idRegex, line)
        if len(possID)>0:
            currentWorkID = possID[0]
            addStory(possID[0],file)

def addTitle(page_source,file):
    #write title
    title = re.search(titleRegex,page_source)
    file.write("*~*TITLE*~*"+title.group(1).strip()+"*~*TITLE*~*\n")
    
def addTags(page_source,file):
    #write tags, comma-separated
    file.write("*~*TAGS*~*")
    tags = re.findall(tagRegex,page_source)
    for tag in tags:
        file.write(tag+",")
    file.write("*~*TAGS*~*\n")
def addSummary(page_source,file):
    #write summary if available w/o html tags
    summary = re.search(summaryRegex,page_source)
    if summary == None:
        stripped_summary = [""]
    else:
        stripped_summary = re.findall(betweenHTMLRegex,summary.group(1))
    file.write("*~*SUMMARY*~*")
    for phrase in stripped_summary:
        file.write(phrase+" ")
    file.write("*~*SUMMARY*~*\n")
def addText(page_source,file):
    #write text w/o html tags
    text = re.search(textRegex,page_source)
    stripped_text = re.findall(betweenHTMLRegex,text.group(1))
    file.write("*~*TEXT*~*")
    for phrase in stripped_text:
        file.write(phrase+" ")
    file.write("*~*TEXT*~*\n")
def addMetadata(page_source,file):
    #grabs metadata (kudos, hits, comment count, date); hits may not be available
    date = re.search(dateRegex,page_source)
    file.write("*~*DATE*~*"+date.group(1)+"*~*DATE*~*\n")
    wordCount = re.search(wordRegex,page_source)
    file.write("*~*WORDCOUNT*~*"+wordCount.group(1)+"*~*WORDCOUNT*~*\n")
    commentCount = re.search(commentRegex,page_source)
    if commentCount==None:
        file.write("*~*COMMENTS*~*0*~*COMMENTS*~*\n")
    else:
        file.write("*~*COMMENTS*~*"+commentCount.group(1)+"*~*COMMENTS*~*\n")
    kudosCount = re.search(kudosRegex,page_source)
    if kudosCount==None:
        file.write("*~*KUDOS*~*0*~*~KUDOS*~*\n")
    else:
        file.write("*~*KUDOS*~*"+kudosCount.group(1)+"*~*KUDOS*~*\n")
    bookmarkCount = re.search(bookmarksRegex,page_source)
    if bookmarkCount==None:
        file.write("*~*BOOKMARKS*~*0*~*~BOOKMARKS*~*\n")
    else:
        file.write("*~*BOOKMARKS*~*"+bookmarkCount.group(1)+"*~*BOOKMARKS*~*\n")
    hitCount = re.search(hitsRegex,page_source)
    if hitCount==None:
        file.write("*~*HITS*~*UNKNOWN*~*HITS*~*\n")
    else:
        file.write("*~*HITS*~*"+hitCount.group(1)+"*~*HITS*~*\n")
        
    
#opens url of a particular story and grabs text
def addStory(currentWorkID, file):
    response = urllib2.urlopen("https://archiveofourown.org/works/"+currentWorkID+"?view_adult=true")
    page_source=response.read()
    #write ID#
    file.write("\n *~*ID_NUMBER*~*"+str(currentWorkID)+"*~*ID_NUMBER*~*\n")
    addTitle(page_source,file)
    addTags(page_source,file)
    addSummary(page_source,file)    
    addText(page_source,file)
    addMetadata(page_source,file)

idRegex = re.compile(r'<li class="work blurb group" id="work_([0-9]*)"')
titleRegex=re.compile(r'<h2 class="title heading">(.*?)</h2>',re.DOTALL)
tagRegex = re.compile(r'<a class="tag".*?>(.*?)</a>')
dateRegex=re.compile(r'<dd class="published">(.*?)</dd>')
wordRegex=re.compile(r'<dd class="words">(.*?)</dd>')
commentRegex=re.compile(r'<dd class="comments">(.*?)</dd>')
kudosRegex=re.compile(r'<dd class="kudos">(.*?)</dd>')
hitsRegex=re.compile(r'<dd class="hits">(.*?)</dd>')
bookmarksRegex=re.compile(r'<dd class="bookmarks"><.*?>(.*?)</a></dd>')
#this regex actually matches author's notes as well as summary
#but the first match on a story page should be the summary
summaryRegex=re.compile(r'<blockquote class="userstuff">(.*?)</blockquote>',re.DOTALL)
textRegex = re.compile(r'<div class="userstuff(?: module" role="article)?">(.*?)</div>',re.DOTALL)
betweenHTMLRegex = re.compile(r'>(.*?)<')

file = open("230_scraping_test_all_categories","a")
#rating = 0 for g, 1 for t, 2 for m, 3 for e
url_start = "https://archiveofourown.org/works/search?commit=Search&page="
url_middle="&utf8=%E2%9C%93&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5Bcomments_count%5D=&work_search%5Bcomplete%5D=&work_search%5Bcreators%5D=&work_search%5Bcrossover%5D=&work_search%5Bfandom_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bquery%5D=&work_search%5Brating_ids%5D=1"
url_end = "&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=1&work_search%5Bsort_column%5D=created_at&work_search%5Bsort_direction%5D=desc&work_search%5Btitle%5D=&work_search%5Bword_count%5D=100-200"
#range = which pages you want to scrape fics from
#1-2 gets you the 20 most recent fics in a category
#2-4 gets you the 21st through 60th most recent fics in a category, etc.
for rating in range(4):
    for page in range(1,2):
        url=url_start+str(page)+url_middle+str(rating)+url_end
        print("currently scraping stories listed here: "+url)
        scrapeURL(url,file)

