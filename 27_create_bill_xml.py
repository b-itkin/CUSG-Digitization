import newbill
import sys
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape

#NOTA BENE: I'm testing a magic number as ALTENDBILLMATCHRE for edge cases in which NEWENDBILLMATCHRE will fail to detect the final clause of a piece of legislation.
#No fancy stuff here, just putting my birthday twice at the end of a bill when legislators feel like not abiding by typical format.

class TwentySevenBill(newbill.Bill):
	NEWENDBILLMATCHRE="This (Bill|Resolution)(, being special order,)* (shall take|takes) effect (immediately )*upon passage\.*"
	ALTENDBILLMATCHRE="0808199708081997" #We're gonna test having a magic number as a delimiter in this session in case the above doesn't catch something.
	TOPHEADERRE="26 EXECUTIVE COUNCIL (BILL|RESOLUTION) [0-9][0-9]*"
	INTRODUCEDDATERE="[0-9][0-2]*\/[0-9][0-9]*\/[0-9][0-9]"
	MONTHINTRODUCEDDATERE="(APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|JANUARY|FEBRUARY|MARCH)\s*[0-9][0-9]*,\s*19(8|9)[0-9]"

	def parseBillText(self):
		self.endbillMatch=re.search(self.NEWENDBILLMATCHRE,self.inputStr,re.I)
		if (self.endbillMatch is None):
			print "WARNING: Trying to detect end of bill. Put '0808199708081997' before the actions section in " + self.infile +" if you have not already"
			self.endbillMatch=re.search(self.ALTENDBILLMATCHRE,self.inputStr,re.I)
		try:
			self.billText=self.inputStr[self.beginbillMatch.start():self.endbillMatch.end()]
		except:
			print "ERROR:"+self.infile+":can't parseBillText"
		#self.addActions
	def parseIntroducedDate(self):
		try:
			topHeaderMatch=re.search(self.TOPHEADERRE,self.inputStr,re.I)
			introducedDateMatch=re.search(self.MONTHINTRODUCEDDATERE,self.inputStr,re.I)

			self.introducedDate=self.inputStr[introducedDateMatch.start():introducedDateMatch.end()]
		except:
			print "ERROR:" +self.infile+"Unable to parse Introduced Date"

f=open('txtfiles.txt','r')
mybill=None
legislations=[]
legislation_name=""
env=Environment(
	loader=FileSystemLoader('./'),
	autoescape=select_autoescape(['html','xml'])
)
template=env.get_template('legislation_template.html')
for line in f:
	try:
		mybill=TwentySevenBill(line.strip())
		mybill.completeParse()
		mybill.createXML()
		legislation_name=line.strip('.txt\n')+'.html'
		with open(legislation_name,'w') as hf:
			hf.write(template.render(billNum=line.strip('.txt\n')))
		legislations.append(legislation_name)
	except Exception as e:
		print "error processing " + line + "\n" + str(e)
f.close()
template=env.get_template('legislation_webpage_template.html')
f=open('legislation_web.html','w+').write(template.render(legislation=legislations))
f.close()
#print "SPONSORS"
#print "--------"
#print mybill.sponsors
#print "AUTHORS"
#print "--------"
#print mybill.authors
#print "Bill History"
#print "--------"
#print mybill.billHistoryString
#print "Bill Summary"
#print "--------"
#print mybill.billSummaryString
#print "Bill Text"
#print "--------"
#print mybill.billText
#print "Bill Introduced Date"
#print "--------"
#print mybill.introducedDate
#mybill.createXML()
