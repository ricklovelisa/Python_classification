#!/usr/bin/python
# coding: utf-8
#
# format for libsvm
# $Id: format_for_libsvm.py  2015-12-14 Qiu $
#
# history:
# 2016-01-09 Qiu   created

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

import MySQLdb
import jieba
import re
import codecs
import cPickle
import pynlpir
import numpy as np
from svmutil import *
from gensim import corpora, models


def etl(s):

    # 去除Unicode下的空白字符

    regex = re.compile(ur"[^\u4e00-\u9f5a]")
    s = regex.sub('', s)
    return s

def format_text(args, index_range, stop_words):

    # 从数据库中提取文本，并将其格式化，以备后面创建字典和语料库

    i = -1
    for line in args:
        i += 1
        if i not in index_range:    # 训练集
            continue
        temp = map(etl, jieba.lcut(line[2].lower()))
        yield filter(lambda word: (len(word)) > 0 and
                                  (word not in stop_words), temp)

# 初始化
conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
cursor = conn.cursor()
jieba.load_userdict('D:/WorkSpace/Python_WorkSpace/'
                    'python_classification/dicts/user_dic')
stop_words = set(line.rstrip() for line in codecs.open('D:/WorkSpace/Python_WorkSpace/'
                                              'python_classification/'
                                              'dicts/stop_words_CN', encoding='utf8'))

# 随机抽取训练集和测试集
test_index = np.random.choice(range(80111), 25000, False) # 需要本地固化
train_index = range(80111)
for i in test_index:
    train_index.remove(i)
train_index = np.array(train_index) # 需要本地固化

# 获取与文章对应的行业列表
sql = 'select indus_code from indus_text_with_label order by id'
cursor.execute(sql)
indus_code_list = []
for indus_code in cursor:
    indus_code_list.append(int(indus_code[0]))
indus_code_list = np.array(indus_code_list)

# 保顿训练集和测试集的label
with open('svm_train/pkl/indus_code_list_train.pkl','a+') as f:
    pick_1 = cPickle.dump(list(indus_code_list[train_index]), f)

with open('svm_train/pkl/indus_code_list_test.pkl','a+') as f:
    pick_2 = cPickle.dump(list(indus_code_list[test_index]), f)

# 生成语料库
sql = "SELECT indus_code, title, content FROM indus_text_with_label ORDER BY id"
cursor.execute(sql)

text_train = format_text(cursor, train_index, stop_words)    # 创建格式化文本
dictionary_train = corpora.Dictionary(text_train)     # 创建词典，需要本地固化。
once_ids = [tokenid for tokenid, docfreq in dictionary_train.dfs.iteritems() if docfreq < 3]  # 去除文档频数低于2的词
dictionary_train.filter_tokens(bad_ids=once_ids)
dictionary_train.compactify()
cursor.scroll(0)
text_train = format_text(cursor, train_index, stop_words)
corpus_train = [dictionary_train.doc2bow(text) for text in text_train]   # 生成语料库
tf_idf_train = models.TfidfModel(corpus_train)     # 生成的tfidf模型需要固化
corpus_tfidf_train = tf_idf_train[corpus_train]

# 固化字典，语料库和tfidf模型
with open('svm_train/pkl/dictionary_train.pkl','a+') as f:
    pick_3 = cPickle.dump(dictionary_train, f)

with open('svm_train/pkl/tf_idf_train.pkl','a+') as f:
    pick_4 = cPickle.dump(tf_idf_train, f)

with open('svm_train/pkl/corpus_tfidf_train.pkl','a+') as f:
    pick_5 = cPickle.dump(corpus_tfidf_train, f)

# 特征选择
