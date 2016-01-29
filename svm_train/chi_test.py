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


import jieba
import re
import codecs
import cPickle
import numpy as np
from svmutil import *
from gensim import corpora, models
from sklearn.metrics import precision_recall_fscore_support

# 加载数据对象
with open('svm_train/pkl/indus_code_list_train.pkl', 'a+') as f:
    indus_code_list_train = cPickle.load(f)

with open('svm_train/pkl/corpus_tfidf_train.pkl', 'a+') as f:
    corpus_tfidf_train = cPickle.load(f)

with open('svm_train/pkl/dictionary_train.pkl', 'a+') as f:
    dictionary_train = cPickle.load(f)

with open('svm_train/pkl/tf_idf_train.pkl', 'a+') as f:
    tf_idf_train = cPickle.load(f)


# 计算卡方值
# 卡方值需要先计算4个值，df(t,c), df(T,c), df(t,C), df(T,C)
# 含义分别是， df(t,c)：c类文档中，包含t词的文档数量，
#              df(T,c)：c类文档中，不包含t词的文档数量
#              df(t,C)：非c类文档中，包含t词的文档数量
#              df(T,C)：非c类文档中，不包含t词的文档数量
# df(t,c) + df(T,c) = df(c)
# df(t,C) + df(T,C) = df(C) = total_df - df(c)
#
# df(t,c) + df(t,C) = df(t)
# df(T,c) + df(T,C) = df(T) = total_df - df(t)


def df_term_cate(word_id, tar_label, label_list, corpus):
    """
    word_id: 需要计算卡方检验的word_id
    tar_label:需要计算卡方检验的目标类别
    label_list:和corpus一一对应的label list
    corpus:语料库
    """

    count = {"df_tc": 0, "df_Tc": 0, "df_tC": 0, "df_TC": 0}
    for index, text in enumerate(corpus):
        if word_id in dict(text).keys() and tar_label == label_list[index]:
            count["df_tc"] += 1
        elif word_id in dict(text).keys() and tar_label != label_list[index]:
            count["df_tC"] += 1
        elif word_id not in dict(text).keys() and tar_label == label_list[index]:
            count["df_Tc"] += 1
        elif word_id not in dict(text).keys() and tar_label != label_list[index]:
            count["df_TC"] += 1
    return count


tar_label_list = list(set(indus_code_list_train))
words_counts = {}
for word_id in dictionary_train.keys():
    words_counts[word_id] = {}
    for tar_label in tar_label_list:
        temp = df_term_cate(word_id, tar_label, indus_code_list_train, corpus_tfidf_train)
        words_counts[tar_label] = temp
        print tar_label
    print word_id


def chi_test(label, corpus, dictionary):
    for text in corpus:
        text
