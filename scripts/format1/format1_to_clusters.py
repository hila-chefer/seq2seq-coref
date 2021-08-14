import re
import json
import sys
import ast
def from_dict_to_list(dic):
    result = []
    for i in dic:
        result.append(dic[i])
    return result

def convert_file(file_name):
    result = []
    with open(file_name,'r') as f:
        for line in f.readlines():
            line = ast.literal_eval(line)
            json_result = {}
            json_result['sentences'] = line['sentences']
            json_result['clusters'] = {}

            target = line['target']

            stack = []
            ambiguity = False
            char_counter = 0
            for i in target:
                single_token_reg = re.match('\((\d+)\)',i)
                open_span_reg = re.match('\((\d+)', i)
                close_span_reg = re.match('(\d+)\)', i)
                if '|' in i:
                    ambiguity = True
                    char_counter -= 1
                if single_token_reg:
                    cluster = single_token_reg.groups()[0]
                    if cluster not in json_result['clusters']:
                        json_result['clusters'][cluster] = []
                    json_result['clusters'][cluster].append([char_counter, char_counter])
                elif open_span_reg:
                    cluster = open_span_reg.groups()[0]
                    stack.append(char_counter)

                elif close_span_reg:
                    cluster = close_span_reg.groups()[0]
                    popped_char_counter = stack.pop()
                    if cluster not in json_result['clusters']:
                        json_result['clusters'][cluster] = []
                    json_result['clusters'][cluster].append([popped_char_counter, char_counter])
                if ambiguity is False:
                    char_counter += 1
                ambiguity = False
            json_result['clusters'] = from_dict_to_list(json_result['clusters'])
            result.append(json_result)
    return result

if __name__ == '__main__':
    #INPUT FILE - same format as output of onto_to_format script
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(output_file, "w+") as outfile:
        result = convert_file(input_file)
        for i in result:
            json.dump(i, outfile)
            outfile.write('\n')
