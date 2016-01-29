#!/usr/bin/python
# coding: utf-8
#
# text explore
# $Id: text explore.py  2015-12-14 Qiu $
#
# history:
# 2015-12-14 Qiu   created

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
# import numpy as np
# from svm import *
import jieba
import re
import math
import codecs
# from textblob import TextBlob as tb
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# from tfidf import TfIdf
from gensim import corpora, models
#
# def tf(word, text):
#     return text.words.count(word) / float(len(text.words))
#
#
# def n_containing(word, corpus):
#     return sum(1 for text in corpus if word in text['content'])
#
#
# def idf(word, corpus):
#     return math.log(len(corpus) / float(1 + n_containing(word, corpus)))
#
#
# def tfidf(word, text, corpus):
#     return tf(word, text) * idf(word, corpus)

## 以文章为基本容器，生成和计算每个类别下每篇文章下每个词的词频和tfidf
# def corp(conn, indus_code, date, stop_words):
#
#     if isinstance(indus_code, unicode):
#         sql = "SELECT indus_code, content FROM indus_text_with_label " \
#               "WHERE indus_code = '%s' AND url LIKE '%s'" % (indus_code, date)
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         for line in cursor:
#         # for line in args:
#             temp = jieba.lcut(line[1])
#             yield filter(lambda word: word not in stop_words, temp)
#         cursor.close()
#     elif isinstance(indus_code, list):
#         sql = "SELECT indus_code, content FROM indus_text_with_label " \
#               "WHERE indus_code = '%s' AND url LIKE '%s'" % (indus_code, date)
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         for line in cursor:
#         # for line in args:
#             temp = jieba.lcut(line[1])
#             yield filter(lambda word: word not in stop_words, temp)
#         cursor.close()
#     else:
#         print 'no indus input'


## 以行业为基本容器，计算每个行业下每个词的词频和tfidf
# def corp_indus(conn, indus_code, stop_words):
#
#     for code in indus_code:
#         sql = "SELECT indus_code, content FROM indus_text_with_label " \
#               "WHERE indus_code = '%s'" % (code)
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         result = []
#         for line in cursor:
#             temp = jieba.lcut(line[1])
#             result_temp = filter(lambda word: word not in stop_words, temp)
#             result = result +  result_temp
#         yield result
#     cursor.close()

conn = MySQLdb.connect(host='127.0.0.1', user='root',
                       passwd='root', db='stock',
                       charset='utf8')
# cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cursor = conn.cursor()
# vectorizer = CountVectorizer()
# transformer = TfidfTransformer()
# tfidf_compute = TfIdf()
jieba.load_userdict('D:/WorkSpace/Python_WorkSpace/'
                    'python_classification/dicts/user_dic')
stop_words = set(line.rstrip() for line in codecs.open('D:/WorkSpace/Python_WorkSpace/'
                                              'python_classification/'
                                              'dicts/stop_words_CN', encoding='utf8'))

# sql = 'SELECT indus_code FROM indus_text_with_label GROUP BY indus_code'
# cursor.execute(sql)
# indus_list = []
# for indus in cursor:
#     indus_list.append(indus[0])
sql = 'select id from indus_text_with_label order by id'
cursor.execute(sql)
id_list = []
for id in cursor:
    id_list.append(id[0])


# text = cursor.fetchall()


############################
## 根据行业分别创建语料库 ##
############################
# dictionary_total = {}
# corpus_total = {}
# corpus_tfidf_total = {}
# for line in indus_list:
#     corpus_temp = corp(conn, line, stop_words)
#     dictionary_total[line] = corpora.Dictionary(corpus_temp)
#     corpus_temp.close()
#     corpus_temp = corp(conn, line, stop_words)
#     corpus_total[line] = [dictionary_total[line].doc2bow(text) for text in corpus_temp]
#     # tf_idf = models.TfidfModel(corpus_total[line])
#     # corpus_tfidf_total[line] = tf_idf[corpus_total[line]]
#     print line

## 计算行业词汇的tfidf
# def compute_tf_in_indus(corpus, dictionary):
#
#     result = {}
#     ## 初始化结果集
#     for term in dictionary.keys():
#         result[term] = 0
#     for line in corpus:
#         for word_num in line:
#             result[word_num[0]] = result[word_num[0]] + word_num[1]
#     return result
#
# tfidf_indus = {}
# for index, value in dictionary_total.items():
#     tf_total_temp = compute_tf_in_indus(corpus_total[index], value)
#     tfidf_indus[index] = {}
#     for word_index, df in value.dfs.items():
#         tf_temp = (1.0 * tf_total_temp[word_index]) / len(value)
#         idf_temp = math.log((1.0 * value.num_docs + 1) / (1 + df))
#         tfidf_indus[index][word_index] = tf_temp * idf_temp
#     print index
# sorted(tfidf_indus['881101'].items(), lambda x, y: cmp(x[1], y[1]), reverse=True)




############################
##        热词统计        ##
############################

### 根据排名变化确定热词 ###
## 获取某个时间段内的文本，并根据行业建立语料库
# dictionary_total = {}
# corpus_total = {}
# for line in indus_list:
#     corpus_temp = corp(conn, line, stop_words, '2015/12/24')
#     dictionary_total[line] = corpora.Dictionary(corpus_temp)
#     corpus_temp.close()
#     corpus_temp = corp(conn, line, stop_words, '2015/12/24')
#     corpus_total[line] = [dictionary_total[line].doc2bow(text) for text in corpus_temp]
#     # tf_idf = models.TfidfModel(corpus_total[line])
#     # corpus_tfidf_total[line] = tf_idf[corpus_total[line]]
#     print line

# corp = []
# for line in cursor:
# #     corp.append(jieba.lcut(line['content']))
# corps = corp(conn, stop_words)
#
# ## 生成行业dict数据对象，用于存储
# dictionary_total = {}
# for code in indus_list:
#     dictionary_total[code] = []
#
# ## 将文本根据indus分离
# i = 1
# for line in corps:
#     for code in indus_list:
#         if code == line['indus_code']:
#             dictionary_total[code].append(line['content'])
#     i += 1
#     print i


def etl(s):
    regex = re.compile(ur"[^\u4e00-\u9f5a]")
    s = regex.sub('', s)
    return s

def corp(conn, stop_words):

    sql = "SELECT indus_code, title, content FROM indus_text_with_label ORDER BY id"
    cursor = conn.cursor()
    cursor.execute(sql)
    for line in cursor:
        temp = map(etl, jieba.lcut(line[2].lower()))
        yield filter(lambda word: (len(word)) > 0 and
                                  (word not in stop_words), temp)
    cursor.close()

corps = corp(conn, stop_words)
dictionary = corpora.Dictionary(corps)
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < 3]
dictionary.filter_tokens(bad_ids=once_ids)
dictionary.compactify()
corps.close()
corps = corp(conn, stop_words)
corpus = [dictionary.doc2bow(text) for text in corps]
tf_idf = models.TfidfModel(corpus)
corpus_tfidf = tf_idf[corpus]

tfidf_result = open('D:/tfidf_result_2', 'a+')
i = 0
for words in corpus_tfidf:
    sorted_words = sorted(words, lambda x, y: cmp(x[1], y[1]), reverse=True)
    for word in sorted_words:
        tfidf_result.write('%s\t%s\t%s\n' %
                           (id_list[i], dictionary[word[0]], str(word[1])))
    tfidf_result.write('\n\n')
    i += 1
    print i
tfidf_result.close()

idf_result = open('D:/idf_result_2', 'a+')
for k, v in sorted(tf_idf.idfs.items(),
                   lambda x, y: cmp(x[1], y[1]), reverse=True):
    idf_result.write(dictionary[k] + '\t' + str(v) + '\n')
    i += 1
    print i
idf_result.close()





# corpus = []
# doc_seg = []
# i = 1
# for line in cursor:
#     temp = jieba.cut(line['content'])
#     for word in temp:
#         if word not in stop_words:
#             doc_seg.append(word)
#     corpus.append(" ".join(doc_seg))
#     i += 1
#     print i
# i = 1
# for line in cursor:
#     temp = jieba.cut(corpus)
#     # corpus.append({'id': line['id'], 'content': tb(' '.join(
#     #         filter(lambda word: word not in stop_words, temp)))})
#     corpus.append(tb(' '.join(filter(lambda word: word not in stop_words, temp))))
#     i += 1
#     print i

# dtm = vectorizer.fit_transform(corpus)
# tfidf = transformer.fit_transform(dtm)
# words = vectorizer.get_feature_names()
# weights = tfidf.toarray()
# result = open('D:/result', 'a+')
# for i in range(len(weights)):
#     print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
#     for j in range(len(words)):
#         print words[j], weights[i][j]
#         result.write(words[j], weights[i][j])

# tb_corpus = []
# for line in corpus:
#     tb_corpus.append(tb(line))


# result = open('D:/result_1', 'a+')
# for line in corpus:
#     scores = {word: tfidf(word, line['content'], corpus) for word in line['content'].words}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     result.write(u'第%s篇文章\n' % (line['id']))
#     print line['id']
#     for k, v in sorted_words:
#         result.write('%s\t%s\n' % (k, round(v, 5)))


cur_test = conn.cursor()
sql_test = 'select indus_text_with_label.id, indus_text_with_label.indus_code, ' \
           'indus_info.indus_name from indus_text_with_label, indus_info ' \
           'where indus_text_with_label.indus_code = indus_info.indus_code order by id'
cur_test.execute(sql_test)
id_indus = open('D:/id_indus', "a+")
for line in cur_test:
    id_indus.write('%s\t%s\t%s\n' % (line[0], line[1], line[2]))
id_indus.close()



# documents = ["Human machine interface for lab abc computer applications",
# "A survey of user opinion of computer system response time",
# "The EPS user interface management system",
# "System and human system engineering testing of EPS",
# "Relation of user perceived response time to error measurement",
# "The generation of random binary unordered trees",
# "The intersection graph of paths in trees",
# "Graph minors IV Widths of trees and well quasi ordering",
# "Graph minors A survey"]
# stoplist = set('for a of the and to in'.split())
# texts = [[word for word in document.lower().split() if word not in stoplist]
#          for document in documents]
# from collections import defaultdict
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1
# texts = [[token for token in text if frequency[token] > 1]
#          for text in texts]
