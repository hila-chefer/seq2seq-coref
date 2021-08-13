import re
import json
import sys
import ast

def text_cluster_to_list(text_clusters):
    lists = []
    formatted = [i.strip().replace(' ',',').replace(',,',',') for i in text_clusters]
    for i in range(len(formatted)):
        lst = ast.literal_eval('['+formatted[i]+']')
        lists.append(lst)
    return lists

def from_dict_to_list(dic):
    result = []
    for i in dic:
        result.append(dic[i])
    return result

def convert_file(file_name):
    result = []
    with open(file_name,'r') as f:
        for i, line in enumerate(f.readlines()):
            json_result = {}
            splitted = line.split('\t')
            sentence = splitted[0]
            format2 = splitted[1]
            format2_splitted = format2.split('SEP')
            cluster_lists = text_cluster_to_list(format2_splitted)
            json_result['sentences'] = sentence
            json_result['clusters'] = cluster_lists
            result.append(json_result)
    return result

if __name__ == '__main__':
    #INPUT FILE - same format as output of onto_to_format script
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(output_file, "w+") as outfile:
        result = convert_file(input_file)
        json.dump(result, outfile)