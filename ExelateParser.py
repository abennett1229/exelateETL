import os
from datetime import date
from RangeFunctions import combine_bounds
from SQLFunctions import file_to_matrix

#Define segments

scale_dict = {}
type_dict = {}
value_dict = {}
min_dict = {}
max_dict = {}
ordinal_dict = {}
used_segments_list = []

mx_taxonomy = file_to_matrix('/home/abennett/exelate/exelate_taxonomy.txt')
for row in mx_taxonomy:
    segment_code = row[0]
    segment_scale = row[1]
    segment_type = row[2]
    segment_value = row[3]
    segment_min = row[4]
    if segment_min != "NULL":
        segment_min = int(segment_min)
    segment_max = row[5]
    if segment_max != "NULL":
        segment_max = int(segment_max)
    scale_dict[segment_code] = segment_scale
    type_dict[segment_code] = segment_type
    value_dict[segment_code] = segment_value
    min_dict[segment_code] = segment_min
    max_dict[segment_code] = segment_max
    used_segments_list.append(segment_code)

mx_ordinal_dict = file_to_matrix('/home/abennett/exelate/ordinal_dict.txt')
for row in mx_ordinal_dict:
    ordinal_segment_type = row[0]
    ordinal_segment_value = row[1]
    ordinal_segment_name = row[2]
    ordinal_dict[(ordinal_segment_type,ordinal_segment_value)] = ordinal_segment_name


f_list = ["13449","13456","13454","13452","13451","13450","13453","3374","13455","13459","13458","13457","227","140","13705","13448","144",
          "1286","10320","13706","145","3373","141","1280","1281"]
m_list = ["13460","13461","13465","13463","13464","13462","13470","13467","13468","13466","13469","13471","994","542","13701","13447",
          "996","13702","13703","13704","998","3376","1000","1282","1283"]

def ParseExelateFile(formatted_date):
    my_date = formatted_date.strftime('%Y%m%d')
    input_filename = '/home/abennett/exelate/exelate_%s_merged.txt' % (my_date)
    output_filename = '/home/abennett/exelate/exelate_%s_parsed.txt' % (my_date)
    log_filename = '/home/abennett/exelate/' + my_date + "_exelate_parser_log.txt"
    log_file = open(log_filename,'a')
    try:
     	input_filesize = os.path.getsize(input_filename) 
	if input_filesize == 0:
		log_file.write(input_filename + '\t' + "input file empty" + '\n')
        	return -1
    except:
	log_file.write(input_filename + '\t' + "input file missing" + '\n')
        return -1
    mx_input = file_to_matrix(input_filename)
    output_file = open(output_filename,'w')
    for row in mx_input:
        ordinal_segment_count = 0
        ordinal_code_list = []
        ordinal_type_list = []
        binary_segment_count = 0
        binary_code_list = []
        binary_type_list = []
        continuous_segment_count = 0
        continuous_code_list = []
        continuous_type_list = []
        revised_segment_list = []
	try:
		uuid = str(row[0])
		req_id = str(row[1])
		campaign_id = str(row[2])
        	ad_id = str(row[3])
        	referrer_doc_id = str(row[4])
        	doc_id = str(row[5])
        	referrer_pub_id = str(row[6])
        	advertiser_id = str(row[7])
        	referrer_source_id = str(row[8])
        	segment_list = row[9]
        	segment_list = segment_list.split(',')
        except:
		continue
	#filter list of attributes to include only demographic attributes and simplify cleaup gender taxonomy
        for segment_code in segment_list:
            if segment_code in f_list:
                revised_segment_list.append("15")
            if segment_code in m_list:
                revised_segment_list.append("16")
            if segment_code in used_segments_list:
                revised_segment_list.append(segment_code)
        #divide attributes into separate lists based on their measurement scale (binary, ordinal, continous, nominal).Nominal attributes will just be written to output file but the rest require unique treatments to correct data inconsistencies.
        for segment_code in list(set(revised_segment_list)):
            if scale_dict[segment_code] == "Binary":
                binary_code_list.append(segment_code)
                if type_dict[segment_code] in binary_type_list:
                    binary_type_list.remove(type_dict[segment_code])
                    binary_segment_count =- 1
                else:
                    binary_type_list.append(type_dict[segment_code])
                    binary_segment_count =+ 1
            elif scale_dict[segment_code] == "Ordinal":
                ordinal_code_list.append(segment_code)
                ordinal_type_list.append(type_dict[segment_code])
                ordinal_segment_count =+ 1
            elif scale_dict[segment_code] == "Continuous":
                continuous_code_list.append(segment_code)
                continuous_type_list.append(type_dict[segment_code])
                continuous_segment_count =+ 1
            else:
                output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + type_dict[segment_code] + '\t' + value_dict[segment_code] + '\n')
        #skip conflicting binary attributes and write the rest to output file
        if binary_segment_count>0:
	    binary_type_list = list(set(binary_type_list))
            for segment_type in binary_type_list:
                for segment_code in binary_code_list:
                    if type_dict[segment_code] == segment_type:
                        output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + type_dict[segment_code] + '\t' + value_dict[segment_code] + '\n')
        #if an ordinal attribute has a single value, write it to the output file. If it has multiple values, write the value range to the output file.
        if ordinal_segment_count>0:
	    ordinal_type_list = list(set(ordinal_type_list))
            for segment_type in ordinal_type_list:
                segment_value_list = []
                for segment_code in ordinal_code_list:
                    if type_dict[segment_code] == segment_type:
                        segment_value_list.append(value_dict[segment_code])
                if len(segment_value_list) == 1:
                    output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + segment_type + '\t' + ordinal_dict[(segment_type,segment_value_list[0])] + '\n')
                else:
                    segment_range = ordinal_dict[(segment_type,min(segment_value_list))] + " to " + ordinal_dict[(segment_type,max(segment_value_list))]
                    output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + segment_type + '\t' + segment_range + '\n')
        #if a continuous attribute has a single range, write it to the output file. If it has multiple ranges, find the smallest possible intersection of the ranges and write it to the output file.
        if continuous_segment_count>0:
	    continuous_type_list = list(set(continuous_type_list))
            for segment_type in continuous_type_list:
                segment_range_list = []
                for segment_code in continuous_code_list:
                    if type_dict[segment_code] == segment_type:
                        segment_range_list.append((min_dict[segment_code],max_dict[segment_code]))
                segment_range_list = list(set(segment_range_list))
                if len(segment_range_list) == 1:
                    segment_range = str(segment_range_list[0][0]) + " to " + str(segment_range_list[0][1])
                    if segment_range_list[0][0] == -999999999 or segment_range_list[0][0] == 0:
                        segment_range = "Under " + str(segment_range_list[0][1])
                    if segment_range_list[0][1] == 999999999:
                        segment_range = str(segment_range_list[0][0]) + "+"
                    output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + segment_type + '\t' + segment_range + '\n')
                else:
                    tuple_range = combine_bounds(segment_range_list)
                    if tuple_range == "NULL":
                        continue
                    if (tuple_range[0] == 0 or tuple_range[0] == -999999999) and tuple_range[1] == 999999999:
                        continue
                    segment_range = str(tuple_range[0]) + " to " + str(tuple_range[1])
                    if tuple_range[0] == -999999999 or tuple_range[0] == 0:
                        segment_range = "Under " + str(tuple_range[1])
                    if tuple_range[1] == 999999999:
                        segment_range = str(tuple_range[0]) + "+"
                    output_file.write(str(formatted_date) + '\t' + req_id + '\t' + uuid + '\t' + doc_id + '\t' + ad_id + '\t' + campaign_id + '\t' + advertiser_id + '\t' +referrer_doc_id + '\t' + referrer_source_id + '\t' + referrer_pub_id + '\t' + segment_type + '\t' + segment_range + '\n')
    if os.path.getsize(output_filename) == 0:
        log_file.write(input_filename + '\t' + "no data written to output file" + '\n')
        return -1
    else:
        log_file.write(input_filename + '\t' + "success" + '\n')
        return 1
