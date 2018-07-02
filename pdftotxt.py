#!/usr/bin/python

import os
import sys

f=open("31pdfs.txt",'r')
for line in f:
	os.system("pdftotext "+line)

f.close()

os.system("ls *.txt > 31txtfiles.txt")
