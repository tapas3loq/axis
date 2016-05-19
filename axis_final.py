import re
import enchant 
from enum import Enum

f = open("/home/tapas/txn_desc_complete.txt","r")

wf = open("/home/tapas/txn_desc_cat.csv","w+")

prefix = ['BRN-BY CASH ','BRN-CLG-CHQ ','BRN-TO CASH ','NEFT']

exception_list = ['cash','by','.','ram','begum','pasha','paid','to','return']
Individual_list = ['ram','begum','pasha']
org_list = ['lic']
self_list = ['yourself','ourselves','self']



d1 = enchant.Dict("en_US")
d2 = enchant.Dict("en_UK")


category = ''

cat = Enum('cat','Self Organisation Individual Unknown')

#SELF
for line in f:
	for exp in prefix:
		#print "checking for " + exp + "\n"
		regex = re.escape(exp) + r".*?"
		match = re.match(regex,line)
		if match:
			#print "line before " + line +"\n"	
			line1 = re.sub(regex,'',line)
			#print "line after " + line1 +"\n"	

			line2 = line1.rstrip('\n')
			line3 = re.split('/|\s|-',line2)
			#print str(line3)

			flag = cat.Unknown
			for word in line3:
				#print "word is " + str(word.lower()) + "\n"
				word1 = word.lower()
				if len(word1)>1 and word1.isalpha():
					#print "word is "  + word1 + "\n"

					if word1 in self_list:
						#print "word is "  + word1 + "\n"
						flag = cat.Self
						break

					elif (d1.check(word1) or d2.check(word1) or word1 in org_list) and word1 not in exception_list :
						#print "category word is " + word1
						flag = cat.Organisation
						break
					elif (d1.check(word1) == False and d2.check(word1) == False) or word1 in Individual_list:
						#print str(line3) +" " + word1
						flag = cat.Individual
					else:
						flag = cat.Unknown 

			#print '\n'
			category = flag.name	
		
			wf.write(exp+line2+","+category+"\n")	
			category_flag = 0
	
	
	