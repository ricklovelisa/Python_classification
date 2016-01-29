import MySQLdb
import codecs
import os
import json

conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
cur = conn.cursor()


industry_ini = open("D:/industry.ini", 'r')
industry_name = open("D:/industry_name", 'r')
indus_codename = {}
for line in industry_name:
    temp = line.split('\t')
    indus_codename[unicode(temp[0])] = unicode(temp[1].split()[0])

industry = {}
i = 1
for line in industry_ini:
    temp = line.split("=")
    temp_2 = temp[1].split()[0].split(',')
    industry[indus_codename[temp[0]]] = [unicode(x) for x in temp_2]
    print i
    i += 1

sql = "select v_code, v_name from stock_info"
cur.execute(sql)
stock_info = dict(cur)
temp = []
for line in industry.values():
    temp = temp + line
total_code = list(set(stock_info.keys() + temp))
for line in total_code:
    if stock_info.has_key(line):
        continue
    else:
        stock_info[line] = line

for k, v in industry.items():
    print k.encode()
    industry[k] = v + [stock_info[x] for x in industry[k]]

industry_words = codecs.open("D:/industry_words", 'a+', "utf8")
industry_keywords = codecs.open("D:/indus_keywords", "r", "utf8")
result_temp = {}
for line in industry_keywords:
    key = line.split()[0]
    value = line.split()[1].split(",")
    result_temp[key] = value

## 行业关键词
for k,v in industry.items():
    if result_temp.has_key(k):
        value = v + result_temp[k]
        industry_words.write("%s\t%s\n" % (k, ",".join(value)))
    else:
        industry_words.write("%s\t%s\n" % (k, ",".join(v)))

## 股票关键词
stock_words = open("D:/stock_words", "a+")
for k,v in stock_info.items():
    stock_words.write("%s\t%s\n" % (k, k+","+v))


gn_dict = {}
file_list = os.listdir("D:/WorkSpace/Python_WorkSpace/ScrapyDocments 2/gn/")
for line in file_list[2:]:
    dir = "D:/WorkSpace/Python_WorkSpace/ScrapyDocments 2/gn/" + line
    with codecs.open(dir, 'r','utf8') as temp:
        json_temp = temp.readlines()
    dic = json.loads(json_temp[0])
    gn_dict[dic['Vocation']] = dic['Code']

gn = {}
for k, v in gn_dict.items():
    print k.encode()
    gn[k] = v + [stock_info[x] for x in gn_dict[k]] + [k]

## 版块关键词
gn_open = open("D:/Section_words","a+")
for k, v in gn.items():
    gn_open.write("%s\t%s\n" % (k, ",".join(v)))