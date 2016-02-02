import redis

rc_6390 = redis.StrictRedis("222.73.34.96",6390,8,"7ifW4i@M")
rc_6379 = redis.StrictRedis("222.73.34.96",6379,8,"7ifW4i@M")
rcp_6379 = rc_6379.pipeline()
text = rc_6390.hgetall("News_20160130")
stock = rc_6390.hgetall("Stock_20160130")
indus = rc_6390.hgetall("Industry_20160130")
sect = rc_6390.hgetall("Section_20160130")
for index in text.keys():
    rcp_6379.hset("News_20160130", index, text[index])

for line in stock.keys():
    temp_6379 = rc_6379.hget("Stock_20160130", line)
    rcp_6379.hset("Stock_20160130", line, str(temp_6379)+stock[line])

for line in indus.keys():
    temp_6379 = rc_6379.hget("Industry_20160130", line)
    rcp_6379.hset("Industry_20160130", line, str(temp_6379)+indus[line])

for line in sect.keys():
    temp_6379 = rc_6379.hget("Section_20160130", line)
    rcp_6379.hset("Section_20160130", line, str(temp_6379)+sect[line])

rcp_6379.execute()


