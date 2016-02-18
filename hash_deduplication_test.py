#!/usr/bin/python
# coding: utf-8
#
# hash_deduplication_test
# $Id: hash_deduplication_test.py  2015-12-14 Qiu $
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


print hash("我的中国梦")
title1 = u"中国留美学生绑架案宣判 3人分别被判6-13年"
title2 = u"三名中国留学生因绑架并凌虐同胞在美国获刑"

n = 3
title_hash = []


def cus_hash(title, n):

    title_hash = []
    for i in range(len(title) - n + 1):
        temp = []
        for j in range(i, (i + n)):
            temp.append(title[j])
        title_hash.append(hash("".join(temp)))
    return title_hash
list1 = cus_hash(title1, n)
list2 = cus_hash(title2, n)


p = len([l for l in list1 if l in list2])*1.0/max(len(list1), len(list2))


