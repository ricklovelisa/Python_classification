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
from scipy.stats import chi2_contingency
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
# 加载数据对象
with open('svm_train/pkl/indus_code_list_train.pkl', 'a+') as f:
    indus_code_list_train = cPickle.load(f)

with open('svm_train/pkl/corpus_tfidf_train_dict.pkl', 'a+') as f:
    corpus_tfidf_train_dict = cPickle.load(f)

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

def bilized_fun(x, y):
    if x == y:
        return 1
    else:
        return 0


def include_term(x, y):
    if y in x:
        return 1
    else:
        return 0

def df_term_cate(indus_code_list_train, indus_code, corpus_tfidf_train, term):
    cate_list = map(bilized_fun, indus_code_list_train, [indus_code] * len(indus_code_list_train))
    term_list = map(include_term, corpus_tfidf_train, [term] * len(indus_code_list_train))
    conf_matrix = confusion_matrix(cate_list, term_list, labels=[1, 0])
    chi_value = chi2_contingency(conf_matrix)[0]
    return (conf_matrix, chi_value)
    # chi_value = np.long(conf_matrix[0,0]*conf_matrix[1,1]-conf_matrix[0,1]*conf_matrix[1,0])**2*1.0\
    #             /np.long(conf_matrix[0,0]+conf_matrix[0,1])/np.long(conf_matrix[1,0]+conf_matrix[1,1])


## 这个方法效率太低，弃用
# def df_term_cate(word_id, tar_label, label_list, corpus):
#     """
#     word_id: 需要计算卡方检验的word_id
#     tar_label:需要计算卡方检验的目标类别
#     label_list:和corpus一一对应的label list
#     corpus:语料库
#     """
#     count = {"df_tc": 0, "df_Tc": 0, "df_tC": 0, "df_TC": 0}
#     for index, text in enumerate(corpus):
#         if word_id in dict(text).keys() and tar_label == label_list[index]:
#             count["df_tc"] += 1
#         elif word_id in dict(text).keys() and tar_label != label_list[index]:
#             count["df_tC"] += 1
#         elif word_id not in dict(text).keys() and tar_label == label_list[index]:
#             count["df_Tc"] += 1
#         elif word_id not in dict(text).keys() and tar_label != label_list[index]:
#             count["df_TC"] += 1
#     return count


# tar_label_list = list(set(indus_code_list_train))
# words_counts = {}
# for word_id in dictionary_train.keys():
#     words_counts[word_id] = {}
#     for tar_label in tar_label_list:
#         temp = df_term_cate(indus_code_list_train, tar_label, corpus_tfidf_train, word_id)
#         words_counts[word_id][tar_label] = temp
#         print tar_label
#     print word_id

# corpus_tfidf_train_dict = []
# i = 0
# for line in corpus_tfidf_train:
#     corpus_tfidf_train_dict.append(dict(line).keys())
#     i += 1
#     print i

words_counts = {}
tar_label_list = list(set(indus_code_list_train))
tar_label_list = tar_label_list[0]
for tar_label in [tar_label_list]:
    words_counts[tar_label] = {}
    for word_id in dictionary_train.keys():
        temp = df_term_cate(indus_code_list_train, tar_label, corpus_tfidf_train_dict, word_id)
        words_counts[tar_label][word_id] = temp
        print word_id
    print tar_label


for line in tar_label_list:
    print line+", "+indus_code_list_train.count(line)+"\n"