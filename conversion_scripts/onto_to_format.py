import re
import sys

WORD_COL_NUM = 3
TARGET_COL_NUM = -1

def remap_target(raw_target):
    mapping = {}
    counter = 0
    result = []
    for i in range(len(raw_target)):
        if i ==122:
            print('')
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
                else:
                    res_str += '|' + target[:span[0]] + str(mapping[group])

        if res_str == '':
                result.append(raw_target[i])
        else:
            result.append(res_str)
    return result

def convert_file(file_name):
    result = []
    with open(file_name,'r') as f:
        words, raw_target = [], []
        for line in f.readlines():
            if not line.startswith('#') and line.strip() != '':
                columns = line.split()
                words.append(columns[WORD_COL_NUM])
                raw_target.append(columns[TARGET_COL_NUM])
            if line.startswith('#end'):
                remapped = remap_target(raw_target)
                text = " ".join(words)
                target = " ".join(remapped)
                words, raw_target = [], []
                result.append((text, target))
    return result

def write_results(to_convert, to_output):
    result = convert_file(to_convert)
    with open('{}'.format(to_output), 'w+') as f:
        for elem in result:
            to_write = elem[0]+'\t'+elem[1]+'\n'
            to_write = to_write.replace('|',' | ')
            f.write(to_write)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    write_results(input_file, output_file)


