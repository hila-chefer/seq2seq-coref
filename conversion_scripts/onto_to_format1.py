import re
import sys
import json
import os

WORD_COL_NUM = 3
TARGET_COL_NUM = -1

def remap_target(raw_target):
    mapping = {}
    counter = 0
    result = []
    stack = []
    for i in range(len(raw_target)):
        targets = raw_target[i].split('|')
        res_str = ""
        for num_tar, target in enumerate(targets):
            reg_iter = re.finditer("(\d+)", target)
            for match in reg_iter:
                span, group = match.span(), match.group()
                if group not in mapping:
                    mapping[group] = counter
                    counter += 1
                if num_tar == 0:
                    res_str += target[0:span[0]] + str(mapping[group]) + target[span[1]:span[1]+1]
                    stack.append(str(mapping[group]))
                else:
                    res_str += ' | ' + target[:span[0]] + str(mapping[group]) + target[span[1]:span[1]+1]
        if res_str == '':
                result.append(raw_target[i])
        else:
            splitted_res_str = res_str.split()
            for i in splitted_res_str:
                result.append(i)
    return result

def convert_file(file_name, to_output):
    result = []
    with open(file_name,'r') as f:
        words, raw_target = [], []
        lines = f.readlines()
        for line in lines:
            if not line.startswith('#') and line.strip() != '':
                columns = line.split()
                words.append(columns[WORD_COL_NUM])
                raw_target.append(columns[TARGET_COL_NUM])
            if line.startswith('#end'):
                remapped = remap_target(raw_target)
                json_res = {'sentences' : words, 'target' : remapped}
                words, raw_target = [], []
                with open(to_output, "a+") as outfile:
                    json.dump(json_res, outfile)
                    outfile.write('\n')

if __name__ == '__main__':
    #INPUT FILE - original data file i.e., train/test/dev
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)



