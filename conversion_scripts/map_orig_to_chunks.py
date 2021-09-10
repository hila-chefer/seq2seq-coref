import itertools
from conversion_scripts.onto_to_format1 import convert_file as convert_to_format1
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
            lines[i] = lines[i].strip()
            if lines[i].startswith("#end"):
                curr_sentences_combs = create_chunks(curr_sentences, 768)
                # with open('../tmp_{}'.format(counter),'a+') as g:
                with open(out_file,'a+') as g:
                    for x, modified_doc in enumerate(curr_sentences_combs):
                        # print(modified_doc)
                        g.write("#begin document ({}); part {}{}\n".format(doc_name,part_name, str(x).zfill(3) ))
                        # print("##begin document ({}); part {}{}\n".format(doc_name,part_name, str(x).zfill(3) ))
                        for sent in modified_doc:
                            for wordline in sent:
                                g.write(wordline+'\n')
                            g.write('\n')
                        g.write("#end document\n")

                # convert_func('../tmp_{}'.format(counter), out_file)
                # os.remove('../tmp_{}'.format(counter))
                counter += 1
                curr_sentences = []
            elif lines[i].startswith("#"):
                #print(lines[i])
                doc_name =  lines[i].split()[2][1:-2]
                part_name = lines[i].split()[-1]
            elif lines[i] == '':
                curr_sentences.append(curr_line)
                curr_line = []
            else:
                curr_line.append(lines[i])


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    # format_num = sys.argv[3]
    augment_format(in_file, out_file, 1)



