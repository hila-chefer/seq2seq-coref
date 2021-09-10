import ast
import re
import json
import sys
import os

def main(file_path):
    indices = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            dic_line = ast.literal_eval(line)
            doc_name = dic_line['doc_id']
            indices[doc_name] = []
            for token in dic_line['clusters'].split():
                single_token_reg = re.match('\((\d+)\)', token)
                open_span_reg = re.match('\((\d+)', token)
                close_span_reg = re.match('(\d+)\)', token)
                regs = [single_token_reg, open_span_reg, close_span_reg]
                contains_num = [i for i in range(len(regs)) if regs[i]]
                if len(contains_num) > 0:
                    num = regs[contains_num[0]].groups()[0]
                    indices[doc_name].append(int(num))

    max_indices = {}
    for elem in indices:
        if indices[elem]:
            max_indices[elem] = max(indices[elem])
        else:
            max_indices[elem] = 0
    #

    processed = []
    counter = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            dic_line = ast.literal_eval(line)
            doc_name, chunk_num = dic_line['doc_id'].split('-')
            if int(chunk_num) == 0:
                with open('upgraded_preds_processed','a+') as g:
                    json.dump(dic_line, g)
                    g.write('\n')
                continue
            offset_to_add = 1+max_indices[doc_name+'-{}'.format(int(chunk_num)-1)]
            target = dic_line['clusters'].split()

            for j, token in enumerate(target):
                single_token_reg = re.match('\((\d+)\)', token)
                open_span_reg = re.match('\((\d+)', token)
                close_span_reg = re.match('(\d+)\)', token)
                regs = [single_token_reg, open_span_reg, close_span_reg]
                contains_num = [i for i in range(len(regs)) if regs[i]]
                if len(contains_num) > 0:
                    num = regs[contains_num[0]].groups()[0]
                    target[j] = target[j].replace(num, str(offset_to_add + int(num)))

            dic_line['clusters'] = " ".join(target)
            with open('upgraded_preds_processed', 'a+') as g:
                json.dump(dic_line, g)
                g.write('\n')

#
def merge_by_doc(file_name, output_file):
    map = {}
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:

            dic_line = ast.literal_eval(line)
            doc_name, chunk_num = dic_line['doc_id'].split('-')
            if doc_name not in map:
                map[doc_name] = {chunk_num : (dic_line['sentences'], dic_line['clusters'])}
            else:
                map[doc_name][chunk_num] = (dic_line['sentences'], dic_line['clusters'])

    dic_doc = {}
    for doc_name in map:
        dic_doc['sentences'] = ''
        dic_doc['clusters'] = ''
        dic_doc['doc_id'] = doc_name
        for i in range(0,100):
            if str(i) not in map[doc_name]:
                break
            dic_doc['sentences'] += ' ' + map[doc_name][str(i)][0]
            dic_doc['clusters'] += ' ' + map[doc_name][str(i)][1]
        with open(output_file,'a+') as f:
            json.dump(dic_doc, f)
            f.write('\n')

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file)
    merge_by_doc('upgraded_preds_processed', output_file)
    os.remove('upgraded_preds_processed')
