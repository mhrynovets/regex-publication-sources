#!/usr/bin/python3
import re
import sys
import json

# Positive Lookahead
#  (?:(?=[A-Z][^\ ]+\ [a-z])[A-Z][^\ ]+)
# https://stackoverflow.com/questions/39222950/regular-expression-with-if-condition
# https://www.regular-expressions.info/conditional.html

def process(name, pattern, unparsed_int):
    global data
    global r_author
    unparsed_old = unparsed_int
    unparsed = []
    print(f">> start {name} regex")
    for cnt, line in enumerate(unparsed_old):
        item = {}
        parsed = re.match(pattern, line)
        if parsed:
            print(cnt, "\t", parsed.groupdict()["full"].strip("\\/ "))
            for key, value in parsed.groupdict().items():
                item[key] = value.strip("\\/ ")
            
            for _, author_pattern in r_author.items():
                p2 = author_pattern+r'.*[\/]{1,2}(?P<rest>.*)'
                res = re.match(p2, item['issuer'])
                if res:
                    item['author'] = res.groupdict()['author']
                    item['issuer'] = res.groupdict()['rest']
                    # sys.exit(1)


            pages = item.get('pages',False)
            if pages:
                p3 = r'\D\.?\ ?(?:(?:(?P<num2>[\d]+)[-–](?P<num3>[\d]+))|(?P<num1>[\d]+))\.?'
                res = re.match(p3, pages)
                if res:
                    print()
                    print()
                    if res.groupdict().get('num2', False):
                        print(res.groupdict()['num2'])
                        print(res.groupdict()['num3'])
                        p1 = int(res.groupdict()['num2'])
                        p2 = int(res.groupdict()['num3'])
                        item['pages'] = str(p2 - p1 + 1)
                        # sys.exit(1)
                    else:
                        print(res.groupdict()['num1'])
                        # item['pages'] = res.groupdict()['num1']
                        item['pages'] = '1'
                p4 = r'[\D]?(?P<num1>[\d]+)\ ?\w\.?'
                res = re.match(p4, pages)
                if res:
                    print()
                    print()
                    print(res.groupdict()['num1'])
                    item['pages'] = res.groupdict()['num1']
                    # sys.exit(1)
            data[int(parsed.groupdict()['num'])] = item
        else:
            unparsed.append(line)
    print(f"<< end {name} regex")
    return unparsed

filepath = 'list.txt'
filerest = 'list_rest.txt'

check_wrong_lines = False
lines = []
with open(filepath) as fp:
    lines = fp.readlines()

for cnt, line in enumerate(lines):
    start = re.match(r'^(\d+)', line)
    if not start:
        print("Line {}: {}".format(cnt, line))
        check_wrong_lines = True

    if check_wrong_lines:
        sys.exit(1)

r_author = {}
r_author_full = r'(?P<author>(?:[A-ZА-Я][\w-]+\ ?[A-ZА-Я][\w-]+[,\.]?\ ?)+)'

r_author['pre1'] = r'(?P<author>(?:[A-ZА-ЯІ]\.[A-ZА-ЯІ]\.\ ?[A-ZА-ЯІ][\w-]+,?\ ?)+)'
r_author['pre2'] = r'(?P<author>(?:[A-ZА-ЯІ]\.\ ?[A-ZА-ЯІ][\w-]+,?\ ?)+)'
r_author['post1'] = r'(?P<author>(?:[A-ZА-ЯІ][\w-]+\ [A-ZА-ЯІ]\.[A-ZА-ЯІ]\.,?\ ?)+)'
r_author['post2'] = r'(?P<author>(?:[A-ZА-ЯІ][\w-]+\ [A-ZА-ЯІ]\.,?\ ?)+)'
r_author_old = r'(?P<author>(?:[A-ZА-ЯІ](?:\.[\w\.]{0,3}|[\w-]+)\ ?[A-ZА-ЯІ](?:\.[\w\.]{0,3}|[\w-]+),?\ ?)+)'
r_num = r'(?P<full>^(?P<num>\d+)\.\s*'
r_pages = r'(?P<pages>[СсCcPpРрSs]\..*)\.?'
r_pages_rev = r'(?P<pages>\d+[СсCcPpРрSs]\.)\.?'
r_name = r'(?P<name>.*?)'

data = {}
unparsed = lines
lines_count = len(lines)+5


#regex_patent = r'(?P<full>^(?P<num>\d+)\.\s*(?P<name>Патент .+?)(?P<author>(?:[A-ZА-ЯІ](?:\.[\w\.]{0,3}|[\w-]+)\ [A-ZА-ЯІ](?:\.[\w\.]{0,3}|[\w-]+),?\ )+)[;:] (?P<issuer>.*)$)'
regex_patent = r_num + r'(?P<name>Патент .+?)' + r_author_old + r'[;:] (?P<issuer>.*)$)'
unparsed = process("patent", regex_patent, unparsed)
# 1 page for all

# regex_electron = r_num + r_author_full + r_name + r'(?:\[Електронний ресурс\].*)(?P<issuer>http[s]?.*)$)';
# unparsed = process("electron_full", regex_electron, unparsed)
# # 1 page for all

# regex_encyclopedia = r'(?P<full>^(?P<num>\d+)\.\s*(?P<author>(\w\.\w{2,},?\ ?)+)(?P<name>.*)(?P<issuer>Encyclopedia.*)[-–][\ ]*(?P<pages>[СсCcPpРрSs]\..*)\.)';
for key, value in r_author.items():
    regex_encyclopedia = r_num + r_author[key] + r_name + r'(?P<issuer>Encyclopedia.*)[-–][\ ]*' + r_pages + ')'
    unparsed = process("encyclopedia_"+key, regex_encyclopedia, unparsed)

for key, value in r_author.items():
    regex = r_num + r_author[key] + r_name + r'(?:[\/]{1,2})(?P<issuer>(?:\w|\s).+)–[\ ]*' + r_pages + ')'
    unparsed = process("basic_"+key, regex, unparsed)

regex = r_num + r_author_full + r_name + r'(?:[\/]{1,2})(?P<issuer>(?:\w|\s).+)–[\ ]*' + r_pages + ')'
unparsed = process("basic_full", regex, unparsed)

for key, value in r_author.items():
    regex = r_num + r_author[key] + r_name + r'(?:[\/]{1,2})(?P<issuer>(?:\w|\s).+)–[\ ]*' + r_pages_rev + ')'
    unparsed = process("basic_"+key, regex, unparsed)

regex = r_num + r_author_full + r_name + r'(?:[\/]{1,2})(?P<issuer>(?:\w|\s).+)–[\ ]*' + r_pages_rev + ')'
unparsed = process("basic_full", regex, unparsed)


with open(filerest, 'w') as f:
    for item in unparsed:
        f.write("%s" % item)

print()

with open('list.json', 'w', encoding='utf8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

with open('list.tsv', 'w', encoding='utf8') as tsv_file:
    print(lines_count)
    for i in range(1, lines_count):
        row = data.get(i, {})
        
        if row:
            print(i, "+")
            pages = row.get('pages', '1')
            line = f"{row['num']}\t{row['name'].strip(' ,')}\tдрук\t{row['issuer'].strip(' ,')}\t{pages}с.\t{row['author'].strip(' ,')}"
            if 'Alma Mater.' in row['issuer']:
                continue
            if 'Народне здоров' in row['issuer']:
                continue
            tsv_file.write(line+"\n")
