import csv
import datetime
import re
"""
extracts from the CSV only the "important" columns and
puts it in the outfile csv
"""

keystrings = [
	"transaction_Status",
	"dollarsobligated",
	"baseandexercisedoptionsValue",
	"baseandalloptionsvalue",
	"signeddate",
	"effectivedate",
	"currentcompletiondate",
	"ultimatecompletiondate",
	"contractactiontype",
	"typeofcontractpricing",
	"Lettercontract",
	"performancebasedservicecontract",
	"VendorName",
	"extentcompeted",
	"numberofemployees",
	"annualrevenue",
]

"""
Properly changes discrete string fields to numeric fields
"""

def modify(fieldname, row):
	if fieldname == "transaction_Status":
		if row["transaction_Status"] == "Active":
			row["transaction_Status"] = 1
		else:
			row["transaction_Status"] = 0	
	elif fieldname == "contractactiontype":					
		if row["contractactiontype"] == "DO Delivery Order":
			row["contractactiontype"] = 0
		elif row["contractactiontype"] == "DCA Definitive Contract":
			row["contractactiontype"] = 1
		else:
			row["contractactiontype"] = 2
	elif fieldname == "typeofcontractpricing":
		if re.search('J: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 0
		elif re.search('V: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 1
		elif re.search('U: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 2
		elif re.search('B: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 3
		elif re.search('R: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 4
		elif re.search('Y: ', row["typeofcontractpricing"]) != None:
			row["typeofcontractpricing"] = 5
	elif fieldname == "Lettercontract":
		if re.search('X', row["Lettercontract"]) != None:
			row["Lettercontract"] = 1
		else:
			row["Lettercontract"] = 0
	elif fieldname == "performancebasedservicecontract":
		if re.search('N: ', row["performancebasedservicecontract"]) != None:
			row["performancebasedservicecontract"] = 0
		elif re.search('Y: ', row["performancebasedservicecontract"]) != None:
			row["performancebasedservicecontract"] = 1
		elif re.search('X: ', row["performancebasedservicecontract"]) != None:
			row["performancebasedservicecontract"] = 2
	elif fieldname == "extentcompeted":
		if re.search('C: ', row["extentcompeted"]) != None:
			row["extentcompeted"] = 0
		elif re.search('G: ', row["extentcompeted"]) != None:
			row["extentcompeted"] = 1
		elif re.search('D: ', row["extentcompeted"]) != None:
			row["extentcompeted"] = 2
		else:
			row["extentcompeted"] = 3
	else:
		row[fieldname] = row[fieldname]

"""
takes the input USA Spending data, modifies it, and puts it
in the output csvfile named by outfile
"""

def modify_CSV(infile, outfile, company_name):
	with open(infile, 'r') as csvinfile, open(outfile, 'w+') as csvoutfile:
		csvinfile_reader = csv.DictReader(csvinfile)
		csvoutfile_writer = csv.DictWriter(csvoutfile, fieldnames=keystrings, lineterminator='\n')
		csvoutfile_writer.writeheader()
		for row in csvinfile_reader:

			if re.search(company_name, row["VendorName"]) == None:
				continue

			for fieldname in keystrings:
				modify(fieldname, row)

			inrow_data = {key: row[key] for key in keystrings}
			csvoutfile_writer.writerow(inrow_data)
			# inrow_data = {
			# 	"active" : row["active"],
			# 	"dollarsobligated" : row["dollarsobligated"],
			# 	"baseandexercisedoptionsValue" : row["baseandexercisedoptionsValue"],
			# 	"baseandalloptionsvalue" : row["baseandalloptionsvalue"],
			# 	"signeddate" : row["signeddate"],
			# 	"effectivedate" : row["effectivedate"],
			# 	"currentcompletiondate" : row["currentcompletiondate"],
			# 	"ultimatecompletiondate" : row["ultimatecompletiondate"],
			# 	"contractactiontype" : row["contractactiontype"],
			# 	"typeofcontractpricing" : row["typeofcontractpricing"],
			# 	"Lettercontract" : row["Lettercontract"],
			# 	"performancebasedservicecontract" : row["performancebasedservicecontract"],
			# 	"DescriptionOfContractRequirement" : row["DescriptionOfContractRequirement"],
			# 	"VendorName" : row["VendorName"], 
			# 	"extentcompeted" : row["extentcompeted"],
			# 	"numberofemployees" : row["numberofemployees"],
			# 	"annualrevenue" : row["annualrevenue"],	
			# }