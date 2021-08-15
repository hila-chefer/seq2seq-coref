import itertools
from conversion_scripts.onto_to_format1 import convert_file as convert_to_format1
from conversion_scripts.onto_to_format2 import convert_file as convert_to_format2
import os
import sys

def create_combinations(sentences):
    xs = [sentences[i:j] for i, j in itertools.combinations(range(len(sentences)+1), 2)]
    return xs

def augment_format(in_file, out_file, format_num):
    convert_func = convert_to_format1 if format_num == 1 else convert_to_format2
    with open(in_file,'r') as f:
        counter = 0
        lines = f.readlines()
        curr_sentences = []
        curr_line = []
        for i in range(len(lines)):
            print("{}/{}".format(i, len(lines)))
            lines[i] = lines[i].strip()
            if lines[i].startswith("#end"):
                curr_sentences_combs = create_combinations(curr_sentences)
                with open('tmp_{}'.format(counter),'w') as g:
                    for modified_doc in curr_sentences_combs:
                        for sent in modified_doc:
                            for wordline in sent:
                                g.write(wordline+'\n')
                        g.write("#end document\n")
                convert_func('tmp_{}'.format(counter), out_file)
                os.remove('tmp_{}'.format(counter))
                counter += 1
                curr_sentences = []
            elif lines[i].startswith("#"):
                continue
            elif lines[i] == '':
                curr_sentences.append(curr_line)
                curr_line = []
            else:
                curr_line.append(lines[i])


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    format_num = sys.argv[3]
    augment_format(in_file, out_file, format_num)



