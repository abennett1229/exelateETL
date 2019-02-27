import boto
import boto.s3.connection
import gzip

#Get all of yesterday's exelate files from s3 (24 files)
def download_s3_files(my_date):
        access_key = 'xxxxxxxxxxxxxxxxxxx'
        secret_key = 'xxxxxxxxxxxxxxxxxxx'
        conn = boto.connect_s3(access_key,secret_key)
        bucket = conn.get_bucket('exelatepoc', validate=False)
	file_count = 0
	for file_key in bucket.list():
        	if file_key.name.startswith('exelate_%s' % (my_date)):
                	file_count = file_count + 1
                	file_key.get_contents_to_filename('/home/abennett/exelate/exelate_%s_%s.tsv.gz' % (my_date,str(file_count)))

#Merge all 24 exelate files from yesterday into a single file 
def merge_s3_files(merged_file,my_date,n):
        filename = '/home/abennett/exelate/exelate_%s_%s.tsv.gz' % (my_date,str(n))
        try:
		file = gzip.open(filename, 'rb')
        	content = file.read()
        	merged_file.write(content)
	except:
		error_log_filename = my_date + '_exelate_s3_error_log.txt'
        	error_log_file = open(error_log_filename,'a')
		error_log_file.write('hour ' + str(n-1) + ' missing from s3' + '\n')
