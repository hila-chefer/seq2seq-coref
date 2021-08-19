import ast
import re
import json
import sys

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
            offset_to_add = max_indices[doc_name+'-{}'.format(int(chunk_num)-1)]
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
            with open('{}_processed'.format(file_path), 'a+') as g:
                json.dump(dic_line, g)
                g.write('\n')

if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)




