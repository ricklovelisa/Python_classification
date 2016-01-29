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
# --------------------------------------------------------------------

import re
import MySQLdb
import urllib2
from bs4 import BeautifulSoup
from input_output import InputOutput


class CrawlIndusStock(object):

    def __init__(self):

        self.from_encoding = 'GBK'
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root',
                                    passwd='root', db='stock',
                                    charset='utf8')
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.input_output = InputOutput(self.conn, self.cursor)

    def _get_html(self, url):

        try:
            req = urllib2.Request(url)
            con = urllib2.urlopen(req)
            doc = con.read()
            con.close()
            print url
            return doc
        except Exception, e:
            print e
            print url
            return

    def _get_page_nums(self, soup):

        page_num = soup.find_all('div', attrs={'class':'list_pager'})
        if page_num[0].find_all('a', attrs={'class':'end'}):
            max_page = page_num[0].find_all('a', attrs={'class':'end'})[0]['href']
            max = max_page.split('_')[1].split('.')[0]
        else:
            max = 1
        return int(max)

if __name__ == '__main__':
    crawl_industry_text = CrawlIndusStock()
    crawl_industry_text.main()
