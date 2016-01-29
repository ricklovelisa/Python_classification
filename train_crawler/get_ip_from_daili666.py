# -*- coding:utf-8 -*-
'''
doc
'''
import urllib2

class GetIPFromDaili666(object):
    '''
    从API中获取ip
    '''
    all_ip_list = []
    api_url = ''
    def __init__(self):
        '''
        '''
        self.api_url = 'http://vxer.daili666api.com/ip/?tid=558465838696598' \
                       '&num=50&delay=3&foreign=none&ports=80,8080'

    def start_request(self):
        '''
        从api接口中json中获得IP、port、type
        '''
        self.all_ip_list = []
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; \
    rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        proxy_support = urllib2.ProxyHandler(None)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        i_headers = {'User_Agent': user_agent}
        req = urllib2.Request(self.api_url, headers=i_headers)
        try:
                data = urllib2.urlopen(req).read()
                ip_port__list = data.split('\r\n')
                for ip_port in ip_port__list:
#                     one_dic = {'type':1, 'ip':ip_port, 'refuse':0, 'time_out':0, 'used':1}
                    #将json中的IP信息存入all_IP_list
                    self.all_ip_list.append(ip_port)
        except:
            print 'error'
