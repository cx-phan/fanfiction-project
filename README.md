# CS 230: Fanfiction Parse

This is an in-progress project for CS 230: Deep Learning. 

# Instructions
Instructions to run each file 

1. To scrape and get updated files from website: run 
python data_scraping_230.py [Var1] [Var2]
These two variables describe the number of pages you are pulling from. For the first to second page, var1 = 1, var2 = 2 

2. To parse from the data into a TSV: run 
python parse_spreadsheet.py [Var1] [Var2]
These two variables are the same as the ones you inputted above. 

You can access both the pre and post-parsed data in the ./data folder. 

3. To run the main file, run:
python CS_230_project.py 
To run any other file in the data folder (records:X-Y.tsv), change the name of the filename. 
