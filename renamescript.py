import sys

print "#!/bin/bash"
for i in range(2,60):
	#print "mv 26ecb%d_OCR.pdf 26_ecb_%d.pdf" % (i,i)
	print "pdftotext 26_ecb_%d.pdf" % i

