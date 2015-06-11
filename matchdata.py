#coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import MySQLdb
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

#��ʽ��xxxx-xx
def getmonth(date):
    url='http://www.stat-nba.com/gameList_simple-'+date+'.html'
    headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
    req = urllib2.Request( url = url,headers = headers)
    html  = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)

    line=soup.table.tbody.findAll('tr')
    num=len(line)

    date=''

    for i in range(num):
        day=line[i].findAll('td')
        for j in range(1,len(day)):
            print day[j].div
            if day[j].div.font!=None and day[j].div.a!=None:
                print '日期',day[j].div.font.string
                print '比赛',day[j].div.a.string

    return

if __name__=="__main__":
    getmonth('2015-06')