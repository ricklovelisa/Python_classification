import redis
import hashlib
import time
import json
import happybase

hbase_conn = happybase.Connection(host="222.73.34.91",port=9090)
hbase_conn.open()
rc = redis.StrictRedis(host='222.73.34.96', port=6379,
                                   db=7, password='7ifW4i@M')
rcp = rc.pipeline()

table_names = {'3_analyzed':u"第一财经", '5_analyzed':u"21CN", '6_analyzed':u"同花顺",
               '7_analyzed':u"雪球", '8_analyzed':u"大智慧", '9_analyzed':u"东方财富"}
date_format = "%Y%m%d"
timeSting_format = "%Y%m%d%H%M%S"
time_format = "%H%M%S"
md5_id = hashlib.md5()

for t_name in table_names.keys():
    table = dict(hbase_conn.table(t_name).scan(include_timestamp=True))
    tableJson = dict(hbase_conn.table(t_name).scan())
    for rowkey in table.keys():
        time_stamp = table[rowkey]['info:industry'][1]/1000
        date_String = time.strftime(date_format, time.localtime(time_stamp))
        datetime_String = time.strftime(timeSting_format, time.localtime(time_stamp))
        time_String = time.strftime(time_format, time.localtime(time_stamp))
        key = "News_" + date_String
        md5_id.update(rowkey)
        field = md5_id.hexdigest() + "_" + time_String
        values_temp = {"indus":tableJson[rowkey]["info:industry"],
                       "sect":tableJson[rowkey]["info:section"],
                       "stock":tableJson[rowkey]["info:category"],
                       "title":tableJson[rowkey]["info:title"],
                       "url":rowkey,
                       "up":0,
                       "down":0,
                       "id":field,
                       "from":table_names[t_name],
                       "time":datetime_String}
        values = json.dumps(values_temp, ensure_ascii=False)
        rcp.hset(key, field, values)
        rcp.expire(key, 60*60*48)
        indus_key = "Industry_" + date_String
        stock_key = "Stock_" + date_String
        sect_key = "Scction" + date_String
        indus_list = values_temp['indus'].split(",")
        for indus in indus_list:
            if indus:
                id_temp = rc.hget(indus_key, indus)
                if not id_temp:
                    rcp.hset(indus_key, indus, field)
                    rcp.expire(indus_key, 60*60*48)
                else:
                    id_new = id_temp + field
                    rcp.hset(indus_key, indus, id_new)
                    rcp.expire(indus_key, 60*60*48)

        stock_list = values_temp['stock'].split(",")
        for stock in stock_list:
            if indus:
                id_temp = rc.hget(stock_key, stock)
                if not id_temp:
                    rcp.hset(stock_key, stock, field)
                    rcp.expire(stock_key, 60*60*48)
                else:
                    id_new = id_temp + field
                    rcp.hset(stock_key, stock, id_new)
                    rcp.expire(stock_key, 60*60*48)

        sect_list = values_temp['sect'].split(",")
        for sect in sect_list:
            if indus:
                id_temp = rc.hget(sect_key, sect)
                if not id_temp:
                    rcp.hset(sect_key, sect, field)
                    rcp.expire(sect_key, 60*60*48)
                else:
                    id_new = id_temp + field
                    rcp.hset(sect_key, sect, id_new)
                    rcp.expire(sect_key, 60*60*48)


rcp.execute()


