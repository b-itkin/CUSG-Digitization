import newbill
import sys
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape

class TwentySixBill(newbill.Bill):
	NEWENDBILLMATCHRE="This (Bill|Resolution|Legislation) takes effect upon passage"
	TOPHEADERRE="26 EXECUTIVE COUNCIL (BILL|RESOLUTION) [0-9][0-9]*"
	INTRODUCEDDATERE="[0-9][0-2]*\/[0-9][0-9]*\/[0-9][0-9]"	
	MONTHINTRODUCEDDATERE="(SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST)\s*[0-9][0-9]*,\s*198[0-9]"

	def parseBillText(self):
		self.endbillMatch=re.search(self.NEWENDBILLMATCHRE,self.inputStr,re.I)
		self.billText=self.inputStr[self.beginbillMatch.start():self.endbillMatch.end()]
		#self.addActions
	def parseIntroducedDate(self):
		try:
			topHeaderMatch=re.search(self.TOPHEADERRE,self.inputStr,re.I)
			introducedDateMatch=re.search(self.MONTHINTRODUCEDDATERE,self.inputStr,re.I)

			self.introducedDate=self.inputStr[introducedDateMatch.start():introducedDateMatch.end()]
		except:
			print "Unable to parse Introduced Date\n"

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
		mybill=TwentySixBill(line.strip())
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
f=open('legislation_web.html','w+').write(template.render(legislation=legislations,session='26',legislationtype=mybill.billType))
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
