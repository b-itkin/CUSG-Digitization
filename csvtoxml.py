#!/usr/bin/python
import newbill


filename=os.argv[1]
f=open(filename,'r')

rows=[]
splitrows=[]
sponsors=[]
authors=[]
actions=[]
for line in f:
	rows.append(line)

del rows[0]

for row in rows:
	splitrows.append(row.split(','))

if (splitrows[0][1] is 'y' and splitrows[0][2] is 'y'):
	for splitrow in splitrows:
		
