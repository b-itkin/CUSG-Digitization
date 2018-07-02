#!/usr/bin/python
#In testing stages for now, but we're getting there
#USAGE: python xmltodb.py xmlfile [test.db]
import sys
import newbill
import sqlite3

dbconn=sqlite3.connect('test.db')
billInstance=newbill.Bill(sys.argv[1],True)
curs=dbconn.cursor()
billNumber=billInstance.billNumber
sessionNumber=billInstance.billSession
billType=billInstance.billType
history=billInstance.billHistoryString
summary=billInstance.billSummaryString
billText=billInstance.billText
introducedDate=billInstance.introducedDate
curs.execute("INSERT INTO TestBillRecords VALUES(?,?,?,?,?,?,?)",
	(billNumber,billType,sessionNumber,history,summary,billText,introducedDate))
dbconn.commit()
dbconn.close()

print "READ OF"+str(billInstance.billSession)+"_"+str(billInstance.billType) +"_"+str(billInstance.billNumber)
print "FROM: " + billInstance.infile + "- Successful"

print "____________"
