#!/bin/bash
#The way I have been doing this has been hugely bootstrapped
#and just plain inefficient for the ultimate purpose of being able to search
#through everything. The system has been proven to work in terms of content
#extraction. The next step is improving the work-flow of converting PDFs
#to XML/webpages and allowing content to be created.
#New workflow: 
#Run this script with new additions to database. The PDFs will be uploaded
#to the CUSG drive in the organization that it's been done so far.
#Every XML file and HTML file will reside in one folder
#After this has been done enough times, we will work on getting the search
#functionality working beyond grepping by piping cat *.txt into it.

find $1 -name *.pdf -exec "pdftotext {}" \;
find $1 
