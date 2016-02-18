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
import time
import MySQLdb
import urllib2
from bs4 import BeautifulSoup
from input_output import InputOutput


class CrawlText(object):
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
            time.sleep(60)
            return "request reject"

    def _get_page_nums(self, soup):

        page_num = soup.find_all('span', attrs={'class': 'num-container'})
        if page_num[0].find_all('a', attrs={'class': 'end'}):
            max_page = page_num[0].find_all('a', attrs={'class': 'end'})[0]['href']
            max = max_page.split('_')[1].split('.')[0]
        else:
            max = 1
        return int(max)

    def _get_indus_page_list(self, from_encoding):

        sql = "select indus_code, indus_name from indus_info"
        code_name = self.input_output.get_data(sql)
        indus_page = {}
        for line in code_name:
            temp_url = 'http://field.10jqka.com.cn/list/field/' \
                       + line['indus_code'] + '/'
            doc = self._get_html(temp_url)
            soup = BeautifulSoup(doc, 'html.parser',
                                 from_encoding=from_encoding)
            page_counts = self._get_page_nums(soup)
            page_url_list = []
            for page in range(1, page_counts + 1):
                page_url = temp_url + 'index_' + unicode(page) + '.shtml'
                page_url_list.append(page_url)
            indus_page[line['indus_code']] = page_url_list
        return indus_page

    def _get_text_url_list(self, url, from_encoding='utf8'):

        doc = self._get_html(url)
        if doc == "request reject":
            return "empty"
        soup = BeautifulSoup(doc, 'html.parser', from_encoding=from_encoding)
        text_list = soup.find_all('span', attrs={'class': 'arc-title'})
        url_list = []
        for line in text_list:
            url_list.append(line.a['href'])
        return url_list

    def _get_text_content(self, url, from_encoding):

        try:
            doc = self._get_html(url)
        except Exception, e:
            print e
            return
        soup = BeautifulSoup(doc, 'html.parser', from_encoding=from_encoding)
        if soup.find_all('div', attrs={'class': 'art_head'}):
            title_temp = soup.find_all('div', attrs={'class': 'art_head'})
            title = title_temp[0].h1.string
            content = ''
            content_temp = soup.find_all('div', attrs={'class': 'art_main'})
            content_temp_list = content_temp[0].find_all('p')
            for line in content_temp_list:
                line_temp = str(line)
                s_u_b = re.compile(r'<[^>]+>', re.S)
                content_str = s_u_b.sub('', line_temp)
                content = content + '\n' + content_str
            result = {'title': title, 'content': content}
            return result
        elif soup.find_all('div', attrs={'class': 'articleTit'}):
            title_temp = soup.find_all('div', attrs={'class': 'articleTit'})
            title = title_temp[0].string
            content = ''
            content_temp = soup.find_all('div', attrs={'class': 'art_main'})
            content_temp_list = content_temp[0].find_all('p')
            for line in content_temp_list:
                line_temp = str(line)
                s_u_b = re.compile(r'<[^>]+>', re.S)
                content_str = s_u_b.sub('', line_temp)
                content = content + '\n' + content_str
            result = {'title': title, 'content': content}
            return result
        elif soup.find_all('div', attrs={'class': 'atc-head'}):
            title_temp = soup.find_all('div', attrs={'class': 'atc-head'})
            title = title_temp[0].h1.string
            content = ''
            content_temp = soup.find_all('div', attrs={'class': 'atc-content'})
            content_temp_list = content_temp[0].find_all('p')
            for line in content_temp_list:
                line_temp = str(line)
                s_u_b = re.compile(r'<[^>]+>', re.S)
                content_str = s_u_b.sub('', line_temp)
                content = content + '\n' + content_str
            result = {'title': title, 'content': content}
            return result
        else:
            print url

    def main(self):

        page_url_list = self._get_indus_page_list(self.from_encoding)
        text_url_list = {}
        for indus_code, page_urls in page_url_list.items():
            indus_code_sql = "select indus_code from indus_text_with_label" \
                             " group by indus_code"

            # 爬虫中断后控制重复爬取的行业
            # crawled_temp = list(self.input_output.get_data(indus_code_sql))
            # # crawled_temp.remove({'indus_code':'881154'})
            # crawled_code = []
            # for crawled in crawled_temp:
            #     crawled_code.append(crawled['indus_code'])
            # if indus_code in crawled_code:
            #     continue

            text_url_list[indus_code] = []
            for page_url in page_urls:
                text_url_list_temp = self._get_text_url_list(page_url,
                                                             self.from_encoding)
                if text_url_list_temp == "empty":
                    continue
                for text_url in text_url_list_temp:
                    try:
                        text_content = self._get_text_content(text_url, self.from_encoding)
                    except Exception, e:
                        print e
                        continue
                    if text_content:
                        sql = "INSERT INTO indus_text_with_label (indus_code," \
                              " title, content, url) VALUES ('%s', '%s', '%s'" \
                              ", '%s')" % (indus_code, text_content['title'],
                                           text_content['content'], text_url)
                        e = self.input_output.insert_data(sql)

                        # 如果发现重复插入的文章，则跳出循环
                        if e:
                            if e[0] == 1062:
                                break
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    crawl_industry_text = CrawlText()
    crawl_industry_text.main()
