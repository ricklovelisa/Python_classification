import MySQLdb
import redis123
import time
import json
import numpy

conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
r = redis123.StrictRedis(host='222.73.34.96', port=6379, db=6, password='7ifW4i@M')
# pr = r.pipeline()
cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
sql = "select id, title, content, url from indus_text_with_label"
cur.execute(sql)
date_time = time.localtime(time.time())
date = time.strftime('%Y-%m-%d',date_time)
time = time.strftime('%H',date_time)
sample = numpy.array(range(80111))
# sample = list(numpy.random.choice(sample, 20000, replace=False))
i = -1
for line in cur:

    i += 1
    print i+1
    # if i not in sample:
    #     continue
    hash_name = 'News' + '_' + date
    hash_key = str(line['id']) + '_' + time
    line['id'] = hash_key
    line['up'] = numpy.random.random_integers(200,size=1)[0]
    line['down'] = numpy.random.random_integers(200,size=1)[0]
    hash_value = json.dumps(line, ensure_ascii=False)
    r.hset(hash_name, hash_key, hash_value)


# pr.execute()


sql = "select indus_text_with_label.id, indus_info.indus_name " \
      "from indus_info, indus_text_with_label " \
      "where indus_info.indus_code = indus_text_with_label.indus_code " \
      "order by indus_text_with_label.id"
cur.execute(sql)
result = {}

for line in cur:
    if result.has_key(line['indus_name']):
        result[line['indus_name']].append(line['id'])
    else:
        result[line['indus_name']] = []

for k,v in result.items():
    hash_name = "Industry"
    hash_key = k
    hash_value = ",".join([(str(x) + "_" + time )for x in v])
    r.hset(hash_name, hash_key, hash_value)

# pr.execute()





