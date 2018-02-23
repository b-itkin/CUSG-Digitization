#!/usr/bin/python
import sys
import re
import os
import xml.etree.ElementTree as ET
import io
import string
from xml.sax.saxutils import escape

#Things TODO for Bill class:
#Create a working way to parse "Actions" and votes -- Focus is shifting to a manual way to do data entry gracefully, as OCR for sessions <83 does not lend a graceful way to process this. 
#Separate names from positions
#Get "Authors" to stop glitching -- Focus is also shifting to a manual way to do data entry gracefully here as well.
#Sessions that were working out of box (minus introducedDate): 83-86 -- now we should verify that recent changes in the past month and a half haven't broken compatibility. New driver should be written regardless

class Sponsor:
	name=""
	title=""
	def __init__(self,sponsorName,sponsorTitle):
		self.name=sponsorName
		self.title=sponsorTitle
	def createElement():
		root=ET.Element("item")
		eName=ET.SubElement(root,"name")
		eName.text=self.name
		eTitle=ET.SubElement(root,"title")
		eTitle.text=self.title
		return root

class Bill:
	rawinputstr="" #Non ASCIIFied
	inputStr="" #ASCIIFied -- nobody got time for weird unicode errors
	sponsorsString=""
	infile=""
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
	tree=None
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
	BEGINBILLMATCHRE="WHEREAS."
	BEGINBILLMATCHALTRE="(BE IT ENACTED|SECTION 1)"
	ENDBILLMATCHRE="Vote Count:*\s*[0-9]+\/[0-9]+\/[0-9]+" 
	AUTHORSMATCHRE="Author.*:.*"
	SPONSORSMATCHRE="Sponsor.*:.*"
	SUBHEADERMATCHRE="(Legislative Council|A Resolution|A Bill)"
	ACTIONSMATCHRE="^(\s\S)+(-)+(\s)*(PASSES|FAILS|POSTPONED|.*REFER.*|.*RATIF.*)(\s)*(-)+(\s)*(EXECUTIVE|LEGISLATIVE)(\s)*(COUNCIL)(\s\S)+$" #This needs some srs ironing out, may be better to do this crowdsourced or some type of fuzzy string matching
	def __init__(self,infile,xmlcreated=False):
		self.infile=infile
		if (xmlcreated):
			self.parseXML(infile)
			#We trust the XML more than the filenames in this case. There should be some intermediary in between this call and validating the XML
			#Which, speaking of, #TODO create an XML schema in DTD or XSD.
		else:		
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
		self.rawinputStr=escape(self.rawinputStr) #Is this all the safest way possible? Acrobat OCR is weird, maybe tesseract will lend itself to a better solution at the OCR level.
		tempArray=bytearray(self.rawinputStr,"utf-8")
		for x in tempArray:
			if (x>31 and x<128) or x==10:
				self.inputStr+=chr(x)
		#self.inputStr=self.rawinputStr.decode("utf-8","replace")
		#for x in self.rawinputStr:
		#	if ord(x)<128:
		#		self.inputStr+=x
	def parseFile(self):
		#TODO: actions
		self.historyMatch=re.search(self.HISTORYMATCHRE,self.inputStr, flags=re.I) #NOTE: early resolutions do not have these, case insensitive
		self.summaryMatch=re.search(self.SUMMARYMATCHRE,self.inputStr, flags=re.I) #NOTE: early resolutions do not have these, case insensitive
		self.beginbillMatch=re.search(self.BEGINBILLMATCHRE,self.inputStr,flags=re.I) #good type of lazy
		if (self.beginbillMatch is None):
			self.beginbillMatch=re.search(self.BEGINBILLMATCHALTRE,self.inputStr,flags=re.I) # It will still have this phrase if it doesn't have preambulatories. Usually applies to early bills
		endbillMatch=re.search(self.ENDBILLMATCHRE,self.inputStr, flags=re.I)
		if (self.endbillMatch is None):
			self.preAudit=True #vote counts and details of action didn't happen necessarily happen pre-audit for legislation after the millenium

		self.authorsMatch=re.search(self.AUTHORSMATCHRE,self.inputStr) #bad type of lazy -- considering getting rid of this in newbill and shifting to session drivers.
		self.sponsorsMatch=re.search(self.SPONSORSMATCHRE,self.inputStr) #bad type of lazy -- considering getting rid of this in newbill and shifting to session drivers.
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
			print "newbill.py WARNING:"+self.infile+":"
			print "Woops! Probably need to rework the code pertaining to 'historyMatch' and 'summaryMatch' in the Bill class\nThe document may also be malformed\n"
		finally:		
			return self.billHistoryString
	def parseBillSummary(self):
		try:
			self.billSummaryString=self.inputStr[self.summaryMatch.end():self.beginbillMatch.start()]
		except:
			print "newbill.py WARNING:"+self.infile+":"
			print "Woops! Probably need to rework the code pertaining to 'summaryMatch' and 'beginbillMatch' in the Bill class\nThe document may also be malformed\n"
		finally:
			return self.billSummaryString
	def parseSponsorsAndAuthors(self):
		try:
			self.sponsorsString=self.inputStr[self.sponsorsMatch.end():self.authorsMatch.start()]
			self.authorsString=self.inputStr[self.authorsMatch.end():self.subheaderMatch.start()]
		except:
			print "newbill.py WARNING:"+self.infile+":"
			print "Woops! Had some problems reading sponsors and authors. Check to make sure the document isn't malformed\n"
		finally:
			self.sponsors=self.sponsorsString.splitlines()
			self.authors=self.authorsString.splitlines()
			self.sponsors=filter(None,self.sponsors)
			self.authors=filter(None,self.authors)
	def parseXML(self,infile):
		self.tree=ET.parse(infile)
		root=self.tree.getroot()
		prefix="./bill/"
		eBillNum=root.find(prefix+'billNumber')
		eBillType=root.find(prefix+'billType')
		eBillSess=root.find(prefix+'sessionNumber')
		eBillText=root.find(prefix+'billText')
		#eSummaries=root.find(prefix+'summaries')
		eBillSummary=root.find(prefix+"summaries/summary")
		eBillHistory=root.find(prefix+'summaries/history')
		eBillIntroducedDate=root.find(prefix+'introducedDate')
		
		self.introducedDate=eBillIntroducedDate.text
		self.billNumber=int(eBillNum.text)
		self.billType=eBillType.text
		self.billSession=int(eBillSess.text)
		self.billHistoryString=eBillHistory.text
		self.billSummaryString=eBillSummary.text
		self.billText=eBillText.text
		#TODO: parse sponsors, authors, and actions.	 
	def createXML(self):
		self.tree=ET.parse('base.xml')
		root=self.tree.getroot()
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
		self.tree.write("{}_{}_{}.xml".format(self.billSession,self.billType,self.billNumber),encoding='utf-8',xml_declaration=True)
	def addSponsorsAndAuthorsXML(self,root):
		#TODO: titles, differentiation between sponsors and authors
		#eBillSponsors=root.find('./bill/sponsors')
		#currentItemElement=None
		#for sponsor in self.sponsors+self.authors:
		#	currentItemElement=ET.SubElement(eBillSponsors,'item')
		#	ET.SubElement(currentItemElement,'name').text=sponsor
		pass
	def addActions(self,root):
		#TODO		
		#eBillActions=root.find('./bill/actions')
		#eBillLatestAction=root.find('./bill/latestAction')
		#currentItemElement=None		
		#for x in self.actions:
		#	currentItemElement=ET.SubElement(eBillActions,'item')
		#	currentItemElement.text=x
		#if currentItemElement is not None:		
		#	eBillLatestAction.text=currentItemElement.text
		pass
		


