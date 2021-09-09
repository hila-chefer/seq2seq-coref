import re
import sys
import json


def remove_words(text):
    cls_regex = r'_|\(\d+\)|\(\d+|\d+\)|\| \(\d+|\| \d+\)|\(\d+ \||\d+\) \||\(\d+\) \||\| \(\d+\)'
    reg = r'(.+?) (' + cls_regex + '?) '
    p = re.compile(reg)

    m = re.search(p, text)
    res = ""
    while m:
        # Append classification
        res += m.group(2) + ' '
        # print(res)
        # Set to the next
        text = text[m.end(0):]
        m = re.search(p, text)
    return res


def main():
    if len(sys.argv) != 3:
        print("Usage: {} input_file output_file".format(sys.argv[0]))
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]

    with open(input_path, "r") as inp, open(output_path, "w") as out:
        for line in inp:
            example = json.loads(line)
            out.write(json.dumps({'doc_id': example['doc_id'], 'clusters': remove_words(example['clusters']),
                                  'sentences': example['sentences']}) + "\n")


if __name__ == "__main__":
    main()
