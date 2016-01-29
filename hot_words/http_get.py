#!/usr/bin/python
# coding: utf-8
#
# http get
# $Id: http get.py  2015-12-14 Qiu $
#
# history:
# 2016-01-07 Qiu   created

# qiuqiu@kunyand-inc.com
# http://www.kunyandata.com
#
# --------------------------------------------------------------------
#
# Copyright (c)  by ShangHai KunYan Data Service Co. Ltd..  All rights reserved.
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# ShangHai KunYan Data Service Co. Ltd. or the author
# not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# ----------------

import json
import urllib2
import re
import MySQLdb
import time


conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')


def return_index(item, list):
    i = 1
    for k,v in list:
        if item == k:
            return i
        i += 1


def get_words_tf(conn, induscode, datetime):

    cur = conn.cursor()
    sql = "SELECT hot_words FROM hot_words_history WHERE indus_code = '%s'" \
          " AND date_time = '%s'" % (induscode, datetime)
    try:
        cur.execute(sql)
    except Exception, e:
        print e
    result = cur.fetchall()
    return result


def get_indus_list():

    sql = 'SELECT indus_code, indus_name FROM indus_info'
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception, e:
        print e
    result = {}
    for k, v in cur:
        result[k] = v
    cur.close()
    return result

indus_list = get_indus_list()
diff_total = {}
for indus_code in indus_list.keys():
    tf_history = json.loads(get_words_tf(conn, indus_code, '20151224')[0][0])
    tf_history_sorted = sorted(tf_history.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    tf_now = json.loads(get_words_tf(conn, indus_code, '20151225')[0][0])
    tf_now_sorted = sorted(tf_now.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    dic_temp = list(set(tf_now.keys()))
    diff = {}
    for line in dic_temp:
        now_exsit = tf_now.has_key(line)
        history_exsit = tf_history.has_key(line)
        if now_exsit and history_exsit:
            index_now = return_index(line, tf_now_sorted)
            index_history = return_index(line, tf_history_sorted)
            diff[line] = index_now - index_history
        elif now_exsit and (not history_exsit):
            index_now = return_index(line, tf_now_sorted)
            diff[line] = index_now - len(tf_history.keys()) - 1
    diff_total[indus_code] = diff

i = 1
hot_keys_result = open('D:/hot_key_result', 'a+')
for indus_code in diff_total.keys():
    # hot_keys_result.write('%s\t%s\t%s\n' % ('#'*5, indus_list[indus_code], '#'*5))
    if diff_total[indus_code]:
        diff_total_sorted = sorted(diff_total[indus_code].items(),
                                   lambda x, y: cmp(x[1], y[1]))
        diff_result = []
        for k, v in diff_total_sorted:
            regex = re.search(ur"[^\u4e00-\u9f5a]", k)
            if v > -1 or regex:
                break
            diff_result.append(k)
        indus_name = indus_list[indus_code]
        hot_keys_result.write('%s\t%s\n' % (indus_name, r",".join(diff_result[0:10])))
        # url = r"http://120.55.189.211/cgi-bin/northsea/prsim/subscribe/1/hot_words_notice.fcgi"
        # hot_words = r"*".join(diff_result[0:20])
        # print hot_words + '\t' + indus_name + '\t' + str(i)
        i += 1
        # time.sleep(3)
        # if len(hot_words) > 0:
        #     req = urllib2.Request(url + '?hot_words=' + hot_words
        #                           + '&industry=' + indus_name)
        #     req_reponse = urllib2.urlopen(req)
        #     res = json.loads(req_reponse.read())
        #     if res['status'] == 1:
        #         print indus_name + 'send successed'
        #     else:
        #         print indus_name + 'send failed'
    # hot_keys_result.write('\n%s\n\n' % ('#'*21))
hot_keys_result.close()