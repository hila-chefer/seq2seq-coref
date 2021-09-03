import itertools
from conversion_scripts.onto_to_format1_no_remap import convert_file as convert_to_format1
#from conversion_scripts.onto_to_format2 import convert_file as convert_to_format2
import os
import sys

def create_chunks(lines, chunk_size):
    # print(lines)
    chunks = []
    counter = 0
    curr_chunk = []
    busted = False
    for line in lines:
        if line == '':
            continue
        else:
            curr_chunk.append(line)
            counter += 1
        if counter == 7:
            busted = True
            chunks.append(curr_chunk)
            curr_chunk = []
            counter = 0
    if curr_chunk:
        chunks.append(curr_chunk)
    return chunks

def augment_format(in_file, out_file, format_num):
    convert_func = convert_to_format1
    with open(in_file,'r') as f:
        counter = 0
        lines = f.readlines()
        curr_sentences = []
        curr_line = []
        for i in range(len(lines)):
            # print("{}/{}".format(i, len(lines)))
            lines[i] = lines[i].strip()
            if lines[i].startswith("#end"):
                curr_sentences_combs = create_chunks(curr_sentences, 768)
                with open('../tmp_{}'.format(counter),'w') as g:
                    for x, modified_doc in enumerate(curr_sentences_combs):
                        g.write("#{}-{}\n".format(doc_name,x ))
                        for sent in modified_doc:
                            for wordline in sent:
                                g.write(wordline+'\n')
                        g.write("#end document\n")

                convert_func('../tmp_{}'.format(counter), out_file)
                os.remove('../tmp_{}'.format(counter))
                counter += 1
                curr_sentences = []
            elif lines[i].startswith("#"):
                #print(lines[i])
                doc_name =  lines[i].split()[2][1:-2]+'/'+lines[i].split()[-1]
            elif lines[i] == '':
                curr_sentences.append(curr_line)
                curr_line = []
            else:
                curr_line.append(lines[i])


import ast
import re
import json

def reset(input_file, output_file):
    processed = []
    mapping = {}
    counter = 0

    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            dic_line = ast.literal_eval(line)
            doc_name = dic_line['doc_id'].split('-')[0]
            if doc_name not in processed:
                mapping = {}
                counter = 0
                processed.append(doc_name)
            target = dic_line['target']
            for j, token in enumerate(target):
                single_token_reg = re.match('\((\d+)\)', token)
                open_span_reg = re.match('\((\d+)', token)
                close_span_reg = re.match('(\d+)\)', token)
                regs = [single_token_reg, open_span_reg, close_span_reg]
                contains_num = [i for i in range(len(regs)) if regs[i]]
                if  len(contains_num) > 0:
                    num = regs[contains_num[0]].groups()[0]
                    if num not in mapping:
                        mapping[num] = counter
                        counter+=1
                    target[j] = target[j].replace(num, str(mapping[num]))
            dic_line['target'] = target
            with open(output_file,'a+') as g:
                json.dump(dic_line, g)
                g.write('\n')


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    augment_format(in_file, 'tmp', 1)
    reset('tmp', out_file)
    os.remove('tmp')



