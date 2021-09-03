import numpy as np
import ast
doc_ids = ['nw/wsj/23/wsj_2358/000-2',
'pt/nt/47/nt_4709/000-2',
'bc/phoenix/00/phoenix_0003/003-4',
'nw/wsj/23/wsj_2350/000-0',
'bc/cctv/00/cctv_0005/006-2',
'pt/nt/40/nt_4009/001-3',
'bc/cnn/00/cnn_0008/002-1',
'bc/msnbc/00/msnbc_0007/006-8',
'bn/cnn/01/cnn_0119/000-0',
'pt/nt/44/nt_4409/001-2',
'nw/wsj/23/wsj_2361/000-0',
'tc/ch/00/ch_0039/002-0',
'bc/cnn/00/cnn_0008/011-10',
'pt/nt/58/nt_5809/000-10',
'bn/cnn/00/cnn_0029/000-0',
'bn/cnn/03/cnn_0359/000-2',
'nw/wsj/23/wsj_2361/000-3',
'tc/ch/00/ch_0009/003-0',
'nw/wsj/23/wsj_2375/000-1',
'bc/phoenix/00/phoenix_0003/003-4']

bart = {}
t5 = {}
with open('bart_test_results_beam_7_processed_processed','r') as g:
    lines = g.readlines()
    for line in lines:
        dic = ast.literal_eval(line)
        if dic['doc_id'] in doc_ids:
            bart[dic['doc_id']] = dic['clusters'].replace(' | ', '|').split()

with open('t5_test_results_beam_7_processed_processed','r') as g:
    lines = g.readlines()
    for line in lines:
        dic = ast.literal_eval(line)
        if dic['doc_id'] in doc_ids:
            t5[dic['doc_id']] = dic['clusters'].replace(' | ', '|').split()
#

#
with open('test_chunks_7', 'r') as f:
    lines = f.readlines()
    for line in lines:
        all_line = ""
        t5str = ""
        bartstr = ""
        dic = ast.literal_eval(line)
        dic['target'] = " ".join(dic['target']).replace(' | ','|').split()
        if dic['doc_id'] in doc_ids:
            for k in range(len(dic['target'])):
                all_line += dic['sentences'][k] + ' ' + dic['target'][k] + ' '
                t5str += dic['sentences'][k] + ' ' + t5[dic['doc_id']][k] + ' '
                bartstr += dic['sentences'][k] + ' ' + bart[dic['doc_id']][k] + ' '
            print()
            print("Ground Truth")
            print(all_line)
            print()
            print("T5")
            print(t5str)
            print()
            print("BART")
            print(bartstr)