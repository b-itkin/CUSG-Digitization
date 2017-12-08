#!/usr/bin/python
import sys
import re
import os
import xml.etree.ElementTree as ET
import io
import string
from xml.sax.saxutils import escape

#Things TODO:
#Modularize Bill so that the class can be more inheritable
#Create a working way to parse "Actions" and votes
#Separate names from positions
#Get "Authors" to stop glitching
#Sessions working out of box (minus TODOS and introducedDate): 83-86

class Bill:
	rawinputstr="" #Non ASCIIFied
	inputStr="" #ASCIIFied -- nobody got time for weird unicode errors
	sponsorsString=""
	authorsString=""
	billHistoryString=""
	billSummaryString=""
	billText=""
	billNumber=0
	billType=""
	billSession=0
	tempBillString=""
	introducedDate=""
	sponsors=[]
	authors=[]
	actions=[]
	preAudit=False
	#####Regular Expression search objects Used To Denote Document Structure For Parsing#####
	#####Initialized in self.parseFile()#####
	historyMatch=None
	summaryMatch=None
	beginbillMatch=None
	endbillMatch=None
	authorsMatch=None
	subheaderMatch=None
	#####Regular Expressions Used In Document Searches #####
	HISTORYMATCHRE="(Bill|Resolution) History"
	SUMMARYMATCHRE="(Bill|Resolution) Summary"
	BEGINBILLMATCHRE="WHEREAS"
	BEGINBILLMATCHALTRE="(BE IT ENACTED|SECTION 1)"
	ENDBILLMATCHRE="Vote Count:*\s*[0-9]+\/[0-9]+\/[0-9]+" 
	AUTHORSMATCHRE="Author.*:.*"
	SPONSORSMATCHRE="Sponsor.*:.*"
	SUBHEADERMATCHRE="(Legislative Council|A Resolution|A Bill)"
	ACTIONSMATCHRE="^(\s\S)+(-)+(\s)*(PASSES|FAILS|POSTPONED|.*REFER.*|.*RATIF.*)(\s)*(-)+(\s)*(EXECUTIVE|LEGISLATIVE)(\s)*(COUNCIL)(\s\S)+$" #This needs some srs ironing out, may be better to do this crowdsourced or some type of fuzzy string matching
	def __init__(self,infile):
		with io.open(infile,'r',encoding='utf-8') as f:
			self.rawinputStr=f.read()
		self.tempBillString=os.path.splitext(infile)[0]
		billNameInfo=self.tempBillString.split('_')
		self.billSession=int(billNameInfo[0])
		self.billType=billNameInfo[1]
		self.billNumber=billNameInfo[2]
	def sanitizeInputStr(self):
		#try:
		#	self.inputStr=self.rawinputStr.encode('utf-8','xmlcharrefreplace')
		#except:
		self.rawinputStr=escape(self.rawinputStr)
		tempArray=bytearray(self.rawinputStr,"utf-8")
		for x in tempArray:
			if x>31 and x<128:
				self.inputStr+=chr(x)
		#self.inputStr=self.rawinputStr.decode("utf-8","replace")
		#for x in self.rawinputStr:
		#	if ord(x)<128:
		#		self.inputStr+=x
	def parseFile(self):
		#TODO: actions
		self.historyMatch=re.search(self.HISTORYMATCHRE,self.inputStr, flags=re.I) #possibly resolutions, case insensitive
		self.summaryMatch=re.search(self.SUMMARYMATCHRE,self.inputStr, flags=re.I) #possibly resolutions, case insensitive
		self.beginbillMatch=re.search(self.BEGINBILLMATCHRE,self.inputStr,flags=re.I) #good type of lazy
		if (self.beginbillMatch is None):
			self.beginbillMatch=re.search(self.BEGINBILLMATCHALTRE,self.inputStr,flags=re.I) # It will still have this phrase if it doesn't have preambulatories. Usually applies to early bills
		endbillMatch=re.search(self.ENDBILLMATCHRE,self.inputStr, flags=re.I)
		if (self.endbillMatch is None):
			self.preAudit=True #vote counts and details of action didn't happen necessarily happen pre-audit for legislation after the millenium

		self.authorsMatch=re.search(self.AUTHORSMATCHRE,self.inputStr) #bad type oflazy
		self.sponsorsMatch=re.search(self.SPONSORSMATCHRE,self.inputStr) #bad type of lazy
		self.subheaderMatch=re.search(self.SUBHEADERMATCHRE,self.inputStr,flags=re.I) #lazy?
		
		
		

		#self.unicodifyStrings()
	#def unicodifyStrings(self):
		#self.billSummaryString=self.billSummaryString.decode('utf-8','ignore')
		#self.billText=self.billText.decode('utf-8','ignore')
	def completeParse(self):
		
		#self.inputStr=repr(self.inputStr)
		#self.inputStr.translate(None,'\\n')
		self.sanitizeInputStr()
		self.parseFile()
		self.parseBillHistory()
		self.parseBillSummary()
		self.parseSponsorsAndAuthors()
		self.parseBillText()
		self.parseIntroducedDate()
		self.parseActions()
		self.additionalParsing()
	def parseActions(self):
		
		try:
			unparsedactiontuples=re.findall(self.ACTIONSMATCHRE,self.inputStr, flags=re.I|re.M)
			currentString="-" #Extra dash shouldn't hurt anyone.
			for actiontuple in unparsedactiontuples:
				for x in actiontuple: 
					currentString+=x
				self.actions.append(currentString)
				currentString="-"
		except Exception as e:
			print e
		finally:
			return self.actions
	
	def parseIntroducedDate(self): #This can be specific to a session, and so is left to the driver (for now)
		pass
	def additionalParsing(self): #TODO -- figure out a more graceful way to interact with created XML
		pass
	
	def parseBillText(self):
		if (self.preAudit):
			self.billText=self.inputStr[self.beginbillMatch.start():]
		else:
			self.billText=self.inputStr[self.beginbillMatch.start():self.endbillMatch.start()]
			#self.addActions
	def parseBillHistory(self):
		try:
			self.billHistoryString=self.inputStr[self.historyMatch.end():self.summaryMatch.start()]
		except:
			print "Woops! Probably need to rework the code pertaining to 'historyMatch' and 'summaryMatch' in the Bill class\nThe document may also be malformed\n"
		finally:		
			return self.billHistoryString
	def parseBillSummary(self):
		try:
			self.billSummaryString=self.inputStr[self.summaryMatch.end():self.beginbillMatch.start()]
		except:
			print "Woops! Probably need to rework the code pertaining to 'summaryMatch' and 'beginbillMatch' in the Bill class\nThe document may also be malformed\n"
		finally:
			return self.billSummaryString
	def parseSponsorsAndAuthors(self):
		try:
			self.sponsorsString=self.inputStr[self.sponsorsMatch.end():self.authorsMatch.start()]
			self.authorsString=self.inputStr[self.authorsMatch.end():self.subheaderMatch.start()]
		except:
			print "Woops! Had some problems reading sponsors and authors. Check to make sure the document isn't malformed\n"
		finally:
			self.sponsors=self.sponsorsString.splitlines()
			self.authors=self.authorsString.splitlines()
			self.sponsors=filter(None,self.sponsors)
			self.authors=filter(None,self.authors)			 
	def createXML(self):
		tree=ET.parse('base.xml')
		root=tree.getroot()
		prefix='./bill/'
		eBillNum=root.find(prefix+'billNumber')
		eBillType=root.find(prefix+'billType')
		eBillSess=root.find(prefix+'sessionNumber')
		eBillText=root.find(prefix+'billText')
		#eSummaries=root.find(prefix+'summaries')
		eBillSummary=root.find(prefix+"summaries/summary")
		eBillHistory=root.find(prefix+'summaries/history')
		eBillIntroducedDate=root.find(prefix+'introducedDate')

		eBillIntroducedDate.text=self.introducedDate
		eBillNum.text=str(self.billNumber)
		eBillType.text=self.billType
		eBillSess.text=str(self.billSession)
		eBillHistory.text=self.billHistoryString
		eBillSummary.text=self.billSummaryString
		eBillText.text=self.billText

		self.addSponsorsAndAuthorsXML(root)
		self.addActions(root)
		tree.write("{}_{}_{}.xml".format(self.billSession,self.billType,self.billNumber),encoding='utf-8',xml_declaration=True)
	def addSponsorsAndAuthorsXML(self,root):
		#TODO: titles, differentiation between sponsors and authors
		eBillSponsors=root.find('./bill/sponsors')
		currentItemElement=None
		for sponsor in self.sponsors+self.authors:
			currentItemElement=ET.SubElement(eBillSponsors,'item')
			ET.SubElement(currentItemElement,'name').text=sponsor
	def addActions(self,root):
		eBillActions=root.find('./bill/actions')
		eBillLatestAction=root.find('./bill/latestAction')
		currentItemElement=None		
		for x in self.actions:
			currentItemElement=ET.SubElement(eBillActions,'item')
			currentItemElement.text=x
		if currentItemElement is not None:		
			eBillLatestAction.text=currentItemElement.text




