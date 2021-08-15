import sys
import json
from conversion_scripts import onto_to_format1, format1_to_clusters
import os

def flatten_list_of_lists(lst):
    return [elem for sublst in lst for elem in sublst]

def convert_file(file_name, output_file):
    with open(file_name,'r') as f:
        words, raw_target = [], []
        tmp_name = '../../tmp_file'
        onto_to_format1.convert_file(file_name, tmp_name)
        format1_to_cluster = format1_to_clusters.convert_file(tmp_name)
        os.remove(tmp_name)
        for i, doc in enumerate(format1_to_cluster):
            to_output = {}
            to_write_doc = ''
            for cluster in doc['clusters']:
                for x,y in cluster:
                    to_write_doc += str([x,y]) + ' '
                to_write_doc += 'SEP '
            to_output['sentences'] = doc['sentences']
            to_output['target'] = to_write_doc[:-5]
            with open(output_file, "a+") as outfile:
                json.dump(to_output, outfile)
                outfile.write('\n')


if __name__ == '__main__':
    #INPUT FILE - original data file i.e., train/test/dev
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)
