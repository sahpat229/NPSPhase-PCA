import csv
import datetime
import re
import random

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


def breachRoll():
	x = random.uniform(0, 3)
	if 0 <= x <= 1:
		return 0
	elif 1 < x <= 2:
		return 1
	else:
		return 2

mapper = {
	
	'MUOS': {

		2008 : {

			1 : 1,
			2 : 1,
			3 : 0,
			4 : 0,
			5 : 0,
			6 : 0,
			7 : 0,
			8 : 0,
			9 : 0,
			10 : 0,
			11 : 0,
			12 : 0,
		},

		2009 : {

			1 : 1,
			2 : 0,
			3 : 0,
			4 : 0,
			5 : 0,
			6 : 0,
			7 : 0,
			8 : 0,
			9 : 0,
			10 : 0,
			11 : 0,
			12 : 0
		},

		2010 : {},
		2011 : {},
		2012 : {},
		2013 : {},
		2014 : {},
		2015 : {},
		2016 : {},
	}
}

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
months = range(1, 13)

for year in years:
	for month in months:
		mapper['MUOS'][year][month] = breachRoll()


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

class YearException(Exception):
	def __init__(self, value):
		self.value = value

def get_range_of_dates(start_month, start_year, end_month, end_year):


	if end_year > start_year:
		range_of_months = (zip(range(start_month, 13), [start_year] * \
			len(range(start_month, 13))))
		curr_year = start_year + 1
		while (curr_year < end_year):
			range_of_months + (zip(range(1, 13), [curr_year] * 12))
			curr_year += 1
		range_of_months + (zip(range(1, end_month + 1), [end_year] * 12))
		return range_of_months

	elif start_year == end_year :
		if end_month < start_month:
			raise YearException('N/A')
		else:
			range_of_months = zip(range(start_month, end_month + 1), [start_year] * \
				len(range(start_month, end_month + 1)))
			return range_of_months

	elif end_year < start_year:
		raise YearException('N/A')

def modify_CSV(infile, outfile, company_name):
	with open(infile, 'r') as csvinfile, open(outfile, 'w+') as csvoutfile:
		csvinfile_reader = csv.DictReader(csvinfile)
		added_names = keystrings + ["Breach"]
		csvoutfile_writer = csv.DictWriter(csvoutfile, fieldnames=added_names, lineterminator='\n')
		csvoutfile_writer.writeheader()
		for row in csvinfile_reader:

			if re.search(company_name, row["VendorName"]) == None:
				continue

			[start_month, start_day, start_year] = map(int, re.split('/', row['effectivedate']))
			print "start: ", [start_month, start_day, start_year]
			[end_month, end_day, end_year] = map(int, re.split('/', row['currentcompletiondate']))
			print "end: ", [end_month, end_day, end_year]
			avg_breach = 0.0;
			try:
				range_of_months = get_range_of_dates(start_month, start_year, end_month, end_year)
				print "RANGE OF MONTHS: ", range_of_months
				total_breach = 0.0
				for tup in range_of_months:
					print "tup", tup
					total_breach += mapper['MUOS'][tup[1]][tup[0]]
				avg_breach = total_breach/(len(range_of_months))

			except YearException as err:

				for fieldname in keystrings:
					modify(fieldname, row)

				inrow_data = {key: row[key] for key in keystrings}
				inrow_data['Breach'] = err.value
				csvoutfile_writer.writerow(inrow_data)

			else:
				for fieldname in keystrings:
					modify(fieldname, row)

				inrow_data = {key: row[key] for key in keystrings}
				inrow_data['Breach'] = avg_breach
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