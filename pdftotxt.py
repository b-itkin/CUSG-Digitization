#!/usr/bin/python

import os
import sys

os.system("ls *.pdf > pdffiles.txt")
f=open("pdffiles.txt",'r')
for line in f:
	os.system("pdftotext "+line)

f.close()

os.system("ls *.txt > txtfiles.txt")
