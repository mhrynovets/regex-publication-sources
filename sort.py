#!/usr/bin/python3
import re
import sys
import json

filepath = 'fin.txt'


lines = []
with open(filepath) as fp:
    lines = fp.readlines()

data = {}
for cnt, line in enumerate(lines):
    start = re.search(r'\D(?P<year>201[4-9])\D', line)
    if start:
        # print("Line {}: {}".format(cnt, start.groupdict()['year']))
        data[cnt] = {}
        data[cnt]['year'] = start.groupdict()['year']
        data[cnt]['line'] = line

    # else:
    #     print("Line {}: --{}".format(cnt, line))

used_sort = dict(sorted(data.items(), key=lambda x: x[1]['year']))

for key, value in used_sort.items():
    print(value['line'].strip())

with open('list2.tsv', 'w', encoding='utf8') as tsv_file:
    for key, value in used_sort.items():
        tsv_file.write(value['line'])
