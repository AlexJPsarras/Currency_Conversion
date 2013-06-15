#!/usr/bin/python
import feedparser

# Open the TXT file created in ACL
input_file = open("C:\ACL_Download\CurrencyInputValues.txt", "r")

# Read the TXT file and set the variables
lines = input_file.readlines()
ACLTable = lines[0].strip()
AmountField = lines[1].strip()
CurrencyField = lines[2].strip()
ConvertToCurrency = lines[3].strip()
my_string = lines[4].strip()
CurrencyList = my_string.split(",")

# Close input file
input_file.close()

# Open the output BAT file and start creating the ACL script
output_file = open('C:\ACL_Download\CurrencyConverter.BAT', 'w')
output_file.write("COM ** Create a computed field that converts all amounts to %s\n"% ConvertToCurrency)
output_file.write("COM ** The exchange rate used is today's rate downloaded from:\n")
output_file.write("COM ** http://themoneyconverter.com\n\n")

output_file.write("OPEN %s\n\n" % ACLTable)
output_file.write("DELETE FIELD c_Amount%s OK\n" % ConvertToCurrency)
output_file.write("DEFINE FIELD c_Amount%s COMPUTED\n\n" % ConvertToCurrency)
output_file.write('1.0000 * %s IF ALLTRIM(%s)="%s"\n' % (AmountField,CurrencyField,ConvertToCurrency))

# Parse the RSS feed for the selected currency
feed_url = "http://themoneyconverter.com/rss-feed/%s/rss.xml" % ConvertToCurrency
feed_data = feedparser.parse(feed_url)

# For each entry in the RSS feed
for entry in feed_data.entries:
 	ex_rate = entry.description.split("=")[1].split(" ")[1].strip()
	curr = entry.title.strip()[0:3]
	# if the currency isn't the selected currency, create a computed field condition
	if curr in CurrencyList:
		if curr != ConvertToCurrency:
			output_file.write('%s * %s IF ALLTRIM(%s)="%s"\n' % (ex_rate,AmountField,CurrencyField,curr))

#Finalise the computed field and close the BAT file
output_file.write("DEC(%s,4)" % AmountField)
output_file.close()