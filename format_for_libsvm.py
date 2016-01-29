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
import numpy as np
from svmutil import *
from gensim import corpora, models
from sklearn.metrics import precision_recall_fscore_support


conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
cursor = conn.cursor()
jieba.load_userdict('D:/WorkSpace/Python_WorkSpace/'
                    'python_classification/dicts/user_dic')
stop_words = set(line.rstrip() for line in codecs.open('D:/WorkSpace/Python_WorkSpace/'
                                              'python_classification/'
                                              'dicts/stop_words_CN', encoding='utf8'))


# 获取与文章对应的行业列表
sql = 'select indus_code from indus_text_with_label order by id'
cursor.execute(sql)
indus_code_list = []
for indus_code in cursor:
    indus_code_list.append(int(indus_code[0]))
indus_code_list = np.array(indus_code_list)

# 去除Unicode下的空白字符
def etl(s):
    regex = re.compile(ur"[^\u4e00-\u9f5a]")
    s = regex.sub('', s)
    return s

# 生成语料库
def format_text(args, stop_words):

    for line in args:
        temp = map(etl, jieba.lcut(line[2].lower()))
        yield filter(lambda word: (len(word)) > 0 and
                                  (word not in stop_words), temp)
    cursor.close()

sql = "SELECT indus_code, title, content FROM indus_text_with_label ORDER BY id"
cursor = conn.cursor()
cursor.execute(sql)
text_format = format_text(cursor, stop_words)
dictionary = corpora.Dictionary(text_format)
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < 3]
dictionary.filter_tokens(bad_ids=once_ids)
text_format.close()
text_format = format_text(conn, stop_words)
corpus = [dictionary.doc2bow(text) for text in text_format]
tf_idf = models.TfidfModel(corpus)
corpus_tfidf_temp = tf_idf[corpus]

corpus_tfidf = []
for line in corpus_tfidf_temp:
    corpus_tfidf.append(dict(line))
corpus_tfidf = np.array(corpus_tfidf)

# 随机抽样训练集
test_index = np.random.choice(range(len(corpus_tfidf)), 25000, False)
train_index = range(len(corpus_tfidf))
for i in test_index:
    train_index.remove(i)
train_index = np.array(train_index)

with open('pkl/indus_code_list_train.pkl','a+') as f:
    pick_1 = cPickle.dump(list(indus_code_list[train_index]), f)

with open('pkl/corpus_train.pkl','a+') as f:
    pick_2 = cPickle.dump(list(corpus_tfidf[train_index]), f)

with open('pkl/corpus_test.pkl','a+') as f:
    pick_3 = cPickle.dump(list(corpus_tfidf[test_index]), f)

with open('pkl/indus_code_list_test.pkl','a+') as f:
    pick_4 = cPickle.dump(list(indus_code_list[test_index]), f)

with open('pkl/dictionary.pkl','a+') as f:
    pick_5 = cPickle.dump(dictionary, f)


###############
## test part ##
###############

import cPickle
from svmutil import *
from gensim import corpora, models
from sklearn.metrics import precision_recall_fscore_support

## readdata
with open('pkl/indus_code_list_train.pkl','a+') as f:
    indus_code_list_train = cPickle.load(f)

with open('pkl/corpus_train.pkl','a+') as f:
    corpus_train = cPickle.load(f)

with open('pkl/corpus_test.pkl','a+') as f:
    corpus_test = cPickle.load(f)

with open('pkl/indus_code_list_test.pkl','a+') as f:
    indus_code_list_test = cPickle.load(f)

with open('pkl/dictionary.pkl','a+') as f:
    dictionary = cPickle.load(f)

def reverse_corpus(corpus):
    result = []
    for line in corpus:
        result.append(line.items())
    return result

print 'data loaded'

dictionary_test = corpora.Dictionary.from_corpus(reverse_corpus(corpus_test),id2word=dictionary)

## 训练svm模型，参数 SVC，RBF核函数，惩罚函数为10
svmmodel = svm_train(indus_code_list_train, corpus_train, '-s 0 -t 0 -c 1')
predict = svm_predict(indus_code_list_test, corpus_test, svmmodel)
prf = precision_recall_fscore_support([int(x) for x in predict[0]], indus_code_list_test)


# svm_save_model("svm_RBF", svmmodel)
# svmmodel = svm_load_model(r'D:\WorkSpace\Python_WorkSpace\python_classification\svm_model\svm_RBF')
