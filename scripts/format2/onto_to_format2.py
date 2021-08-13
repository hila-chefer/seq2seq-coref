import sys
from scripts.format1 import format1_to_clusters, onto_to_format1

def flatten_list_of_lists(lst):
    return [elem for sublst in lst for elem in sublst]

def convert_file(file_name):
    result = []
    with open(file_name,'r') as f:
        words, raw_target = [], []
        tmp_name = '../../tmp_file'
        onto_to_format1.write_results(file_name, tmp_name)
        format1_to_cluster = format1_to_clusters.convert_file(tmp_name)
        for i, doc in enumerate(format1_to_cluster):
            to_write_doc = ''
            for cluster in doc['clusters']:
                for x,y in cluster:
                    to_write_doc += str([x,y]) + ' '
                to_write_doc += 'SEP '
            to_write_doc = to_write_doc[:-5]
            result.append((" ".join(flatten_list_of_lists(doc['sentences'])),to_write_doc))
    return result

def write_results(to_convert, to_output):
    result = convert_file(to_convert)
    with open('{}'.format(to_output), 'w+') as f:
        for elem in result:
            to_write = elem[0]+'\t'+elem[1]+'\n'
            f.write(to_write)

if __name__ == '__main__':
    #INPUT FILE - original data file i.e., train/test/dev
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    write_results(input_file, output_file)
