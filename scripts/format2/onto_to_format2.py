import sys
import json
from scripts.format1 import format1_to_clusters, onto_to_format1
import os

def flatten_list_of_lists(lst):
    return [elem for sublst in lst for elem in sublst]

def convert_file(file_name):
    result = []
    with open(file_name,'r') as f:
        words, raw_target = [], []
        tmp_name = '../../tmp_file'
        onto_to_format1.write_results(file_name, tmp_name)
        format1_to_cluster = format1_to_clusters.convert_file(tmp_name)
        os.remove(tmp_name)
        for i, doc in enumerate(format1_to_cluster):
            json = {}
            to_write_doc = ''
            for cluster in doc['clusters']:
                for x,y in cluster:
                    to_write_doc += str([x,y]) + ' '
                to_write_doc += 'SEP '
            json['sentences'] = doc['sentences']
            json['target'] = to_write_doc[:-5]
            result.append(json)
    return result

def write_results(to_convert, to_output):
    result = convert_file(to_convert)
    with open(to_output, "w") as outfile:
        for i in result:
            json.dump(i, outfile)
            outfile.write('\n')

if __name__ == '__main__':
    #INPUT FILE - original data file i.e., train/test/dev
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    write_results(input_file, output_file)
