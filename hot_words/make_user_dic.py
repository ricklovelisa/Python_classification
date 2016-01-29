#!/usr/bin/python
# coding: utf-8
#
# crawler_industry_text
# $Id: crawler_industry_text.py  2015-12-14 Qiu $
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

conn = MySQLdb.Connect(host='127.0.0.1', user='root',
                                    passwd='root', db='stock',
                                    charset='utf8')
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sql_stock = 'select v_code, v_name from stock_info'
sql_indus = 'select indus_name from indus_info'

cursor.execute(sql_stock)
stock = cursor.fetchall()
cursor.execute(sql_indus)
indus = cursor.fetchall()

user_dic = open('D:/user_dic', 'a+')
for line in stock:
    user_dic.write(line['v_name'] + '\t' + '100'+ '\t' + 'n' + '\n')
    user_dic.write(line['v_code'] + '\t' + '100'+ '\t' + 'n' + '\n')
for line in indus:
    user_dic.write(line['indus_name'] + '\t' + '100' + '\t' + 'n' + '\n')

user_dic.close()
cursor.close()
conn.close()
