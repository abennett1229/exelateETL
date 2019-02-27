import os

#Read in a file and return a two-dimensional list representation
def file_to_matrix(filename):
    #Read in the file
    result_str = ''
    f = open(filename)
    result_str = f.read()
    f.close()
    #Initialize a new matrix to store the results
    result_matrix = []
    #Split rows into a list
    for row in result_str.split('\n'):
        #Filter out any last null rows
        if (row != ''):
            new_row = []
                for entry in row.split('\t'):
                    new_row.append(entry)
                        result_matrix.append(new_row)
    return result_matrix

#Default credentials for sandbox SQL
def get_sandbox_credentials():
    mode = 'sql'
    user = 'outbrain_sandbox'
    password = 'xxxxxxxxxxxxxxxx'
    host = 'mysql-xxxxxxxxxxxxxxxxxx.outbrain.com'
    port = 'xxxx'
    return {'mode':mode,'user':user,'password':password,'host':host,'port':port}

#Load data from text file into MySQL table
def LoadToSQL(parsed_filename,query_filename):
	query_file = open(query_filename,'w')
	my_credentials = get_sandbox_credentials()
	query_template_filename = '/home/abennett/exelate/LoadToSQL.sql'
	query_template_file = open(query_template_filename)
	query_content = query_template_file.read()
	query_content = query_content.replace('filename',parsed_filename)
	query_file.write(query_content)
	query_file.close()
	query_str = "mysql --user=%s --password=%s --host=%s --port=%s < %s" % (my_credentials['user'],my_credentials['password'], my_credentials['host'], my_credentials['port'], query_filename)
	os.popen(query_str).read()
