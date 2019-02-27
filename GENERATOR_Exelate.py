import os
from dateutil.relativedelta import relativedelta
from datetime import date
from s3Functions import download_s3_files,merge_s3_files
from SQLFunctions import LoadToSQL
from ExelateParser import ParseExelateFile

formatted_date = date.today() - relativedelta(days=1)
my_date = formatted_date.strftime('%Y%m%d')
 
#Get all of yesterday's exelate files from s3 (24 files)
download_s3_files(my_date)

#Merge all 24 exelate files from yesterday into a single file 
merged_filename = '/home/abennett/exelate/exelate_%s_merged.txt' % (my_date)
merged_file = open(merged_filename,'w')
for n in range(1,25):
	merge_s3_files(merged_file,my_date,n)

#Parse the input file and create an output file
ParseExelateFile(formatted_date)

#Load output file into sandbox SQL table
my_context = 'sandbox'
parsed_filename = '/home/abennett/exelate/exelate_%s_parsed.txt' % (my_date)
query_filename = '/home/abennett/exelate/' + my_date + '_LoadToSQL.sql'
LoadToSQL(parsed_filename,query_filename)

#Delete yesterday's exelate files from local directory
os.remove(merged_filename)
os.remove(parsed_filename)
os.remove(query_filename)
for n in range(1,25):
	original_filename = '/home/abennett/exelate/exelate_%s_%s.tsv.gz' % (my_date,str(n))
	try:
		os.remove(original_filename) 
	except:
		continue
