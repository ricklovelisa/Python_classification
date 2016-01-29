#!/usr/bin/python
# coding: utf-8
#
# hot words
# $Id: hot_words.py  2016-01-07 Qiu $
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

import codecs
import MySQLdb
import jieba
import json
import re
from gensim import corpora

conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
stop_words_path = 'D:/WorkSpace/Python_WorkSpace/'\
                  'python_classification/dicts/stop_words_CN'
stop_words = set(line.rstrip() for line in codecs.open(stop_words_path,
                                                       encoding='utf8'))
jieba.load_userdict('D:/WorkSpace/Python_WorkSpace/'
                    'python_classification/dicts/user_dic')


def corp_in_indus(conn, induscode, date, stopwords):

    cur = conn.cursor()
    sql = "SELECT indus_code, content FROM indus_text_with_label " \
          "WHERE indus_code = '%s' AND url LIKE '%s'" % (induscode, date)
    try:
        cur.execute(sql)
    except Exception, e:
        print e
    for line in cur:
        temp = jieba.lcut(line[1])
        yield filter(lambda word: word not in stopwords, temp)
    cur.close()


def get_indus_list():

    sql = 'SELECT indus_code FROM ' \
          'indus_text_with_label GROUP BY indus_code'
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception, e:
        print e
    indus_list = []
    for indus in cur:
        indus_list.append(indus[0])
    cur.close()
    return indus_list


def dict_and_corpus(conn, induscode, date, stopwords):

    # corpus_tfidf_total = {}
    corpus_temp = corp_in_indus(conn, induscode, date, stopwords)
    dictionary = corpora.Dictionary(corpus_temp)
    corpus_temp.close()
    corpus_temp = corp_in_indus(conn, induscode, date, stopwords)
    corpus = [dictionary.doc2bow(text) for text in corpus_temp]
    return dictionary, corpus


def compute_tf(corpus, dictionary):

    result = {}
    ## 初始化结果集
    for term in dictionary.keys():
        result[term] = 0
    for text in corpus:
        for word in text:
            result[word[0]] = result[word[0]] + word[1]
    return result


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

## 计算当天的词频，并写入数据库中
indus_list = get_indus_list()
for indus_code in indus_list:
    dictionary, corpus = dict_and_corpus(conn, indus_code, '%20151225%', stop_words)
    tf = compute_tf(corpus, dictionary)
    tf_word = {}
    for k, v in tf.items():
        empty = re.search(r'\s', dictionary[k])
        if v > 1 and dictionary[k] != u'\u3000' and not empty:
            tf_word[dictionary[k].decode()] = v
    json_result = json.dumps(tf_word, ensure_ascii=False)
    insert_sql = "INSERT INTO hot_words_history " \
                 "(date_time, indus_code, hot_words) " \
                 "VALUE ('%s', '%s', '%s')" % \
                 ('20151225', indus_code, json_result)
    cur = conn.cursor()
    try:
        cur.execute(insert_sql)
        conn.commit()
    except Exception, e:
        print e
    cur.close()
    print indus_code















# temp = sorted(text, lambda x, y: cmp(x[1], y[1]), reverse=True)
# heapq.nlargest()