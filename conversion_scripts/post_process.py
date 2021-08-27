import ast
import sys
import json


def rremove(alist, x):  # reversed remove: remove last apareance of x in list
    alist.pop(len(alist) - alist[::-1].index(x) - 1)


def correctParen(cors):
    clusList = []  # to keep cluster of the incorrect coref
    indList = []  # to keep index of the incorrect coref
    i = 0
    while i in range(len(cors)):
        cor = cors[i]
        j = 0
        found = 0
        aux = []
        cor = cor.split("|")
        while j in range(len(cor)):
            c = cor[j]
            aux.append(c)
            if "(" in c and ")" not in c:  # if (1
                clusList.append(c.strip("("))
                indList.append([i, j])
            elif ")" in c and "(" not in c:  # 1)
                if c.strip(")") not in clusList:  # no (1 in list
                    found = 1
                    del aux[-1]
                else:
                    indList.pop((-clusList[::-1].index(c.strip(")"))) - 1)
                    rremove(clusList, c.strip(")"))
            if found:
                if "|" in cors[i]:
                    cors[i] = "|".join(aux)
                else:
                    cors[i] = "-"
            j += 1
        i += 1
    for i in reversed(indList):
        if isinstance(i, list):
            i, j = i[0], i[1]
            c = cors[i].split("|")
            if len(c) > 1:
                print(c)
                del c[j]
            else:
                c[j] = "-"
            cors[i] = "|".join(c)
        else:
            cors[i] = ("-")
    return cors


def postprocess(source, target):
    out = correctParen(target)
    joined_out = " ".join(out)
    out = joined_out.replace(' | ', '|').split()
    len_diff = len(source.split()) - len(out)
    if len_diff > 0:
        for j in range(len_diff):
            out.append('-')
    else:
        out = out[:len(out) + len_diff]
    return " ".join(out).replace('|', ' | ')


def main():
    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for i in lines:
            dic = ast.literal_eval(i)
            dic['clusters'] = postprocess(dic['sentences'], dic['clusters'].split())
            with open('{}_processed'.format(input_file), 'a+') as f:
                json.dump(dic, f)
                f.write('\n')


if __name__ == '__main__':
    main()
