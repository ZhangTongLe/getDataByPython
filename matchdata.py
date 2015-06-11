#coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import MySQLdb
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

#格式：xxxx-xx
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
            t=str(day[j].div).split('<br />>')
            if(len(t)>1):
                #print t[1]
                for i in range(len(t)):
                    if t[i][1]=='a':
                        y=t[i].split('\">')[0].split('href=\"')[1]
                        url='http://www.stat-nba.com/'+y[0:4]+'/'+y[4:]
                        team=t[i].split('>')[1]
                        date=day[j].div.font.string
                        getOneMatch(url,date)

def getOneMatch(url,date):
    headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
    req = urllib2.Request( url = url,headers = headers)
    html  = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)

    s=soup.find('div',attrs={"class":"title"})

    t=s.string.split('赛季')

    season=t[0].strip()

    isPlayOff='1'
    if t[1].strip()=='常规赛':
        isPlayOff='0'



    #比赛简要信息
    t1=soup.findAll('table')[0].findAll('tr')
    t2=soup.findAll('table')[1].findAll('tr')
    score1=[0 for x in range(len(t1))]
    score2=[0 for x in range(len(t2))]
    score=''
    for i in range(len(t1)):
         score1[i]=t1[i].findAll('td')[1].string
         score2[i]=t2[i].findAll('td')[0].string

    for i in range(len(t1)-1):
        score=score+score1[i]+':'+score2[i]+';'
    score=score+score1[len(t1)-1]+':'+score2[len(t1)-1]#得分总览

    team1=soup.findAll('div',attrs={"class":"teamDiv"})[0].div.a.string+'队'
    team2=soup.findAll('div',attrs={"class":"teamDiv"})[1].div.a.string+'队'

    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='nba',charset='utf8')
    cur = conn.cursor()

    """
    if team1=="夏洛特山猫队":
        team1='夏洛特黄蜂队'
    if team2=="夏洛特山猫队":
        team2='夏洛特黄蜂队'

    if team1=="新奥尔良黄蜂队":
        team1='新奥尔良鹈鹕队'
    if team2=="新奥尔良黄蜂队":
        team2='新奥尔良鹈鹕队'
    """

    cur.execute("select * from teaminfo where fullname = '%s'" %(team1))
    team1ID = cur.fetchall()[0][0]
    cur.execute("select * from teaminfo where fullname = '%s'" %(team2))
    team2ID = cur.fetchall()[0][0]

    conn.commit()
    cur.close()
    conn.close()

    t=date.split('-')
    matchid=t[0]+t[1]+t[2]+team1ID+team2ID+isPlayOff

    T=[(matchid,season,team1,team2,score)]
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='nba',charset='utf8')
    cur = conn.cursor()

    cur.execute("select * from matchinfo where matchid = '%s'" %(matchid))
    temp = cur.fetchall()
    if(not len(temp)):
        stmt = "INSERT INTO matchinfo VALUES (%s,%s,%s,%s,%s)"
        cur.executemany(stmt, T)

    conn.commit()
    cur.close()
    conn.close()

    #比赛详细信息（球员数据）
    t1=soup.findAll('table')[2].tbody.findAll('tr')
    t2=soup.findAll('table')[3].tbody.findAll('tr')
    num1=len(t1)-2
    num2=len(t2)-2


    pl1=[['' for x in range(22)] for y in range(num1)]
    pl2=[['' for x in range(22)] for y in range(num2)]
    for i in range(0,num1):
        p=t1[i].findAll('td')
        pl1[i][0]=p[1].a.string
        for j in range(2,23):
            if p[j].string==' ':
                pl1[i][j-1]='/'
            else:
                pl1[i][j-1]=p[j].string

    for i in range(0,num2):
        p=t2[i].findAll('td')
        pl2[i][0]=p[1].a.string
        for j in range(2,23):
            if p[j].string==' ':
                pl2[i][j-1]='/'
            else:
                pl2[i][j-1]=p[j].string

    print date
    print team1+'VS'+team2

    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='nba',charset='utf8')
    cur = conn.cursor()

    for i in range(0,num1):
        T=[(matchid,pl1[i][0],team1,pl1[i][1],pl1[i][2],pl1[i][3],pl1[i][4]+'-'+pl1[i][5],pl1[i][6],pl1[i][7]+'-'+pl1[i][8],\
            pl1[i][9],pl1[i][10]+'-'+pl1[i][11],pl1[i][12],pl1[i][13],pl1[i][14],pl1[i][15],pl1[i][16],pl1[i][17],pl1[i][18],pl1[i][19],\
             pl1[i][20],pl1[i][21])]
        cur.execute("select * from playermatchdata where matchid = '%s'and playername='%s'" %(matchid,pl1[i][0]))
        temp = cur.fetchall()
        if(not len(temp)):
            stmt = "INSERT INTO playermatchdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\
            ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(stmt, T)

    for i in range(0,num2):
        T=[(matchid,pl2[i][0],team2,pl2[i][1],pl2[i][2],pl2[i][3],pl2[i][4]+'-'+pl2[i][5],pl2[i][6],pl2[i][7]+'-'+pl2[i][8],\
            pl2[i][9],pl2[i][10]+'-'+pl2[i][11],pl2[i][12],pl2[i][13],pl2[i][14],pl2[i][15],pl2[i][16],pl2[i][17],pl2[i][18],pl2[i][19],\
             pl2[i][20],pl2[i][21])]
        cur.execute("select * from playermatchdata where matchid = '%s'and playername='%s'" %(matchid,pl2[i][0]))
        temp = cur.fetchall()
        if(not len(temp)):
            stmt = "INSERT INTO playermatchdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\
            ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(stmt, T)

    conn.commit()
    cur.close()
    conn.close()




if __name__=="__main__":

    #getOneMatch('http://www.stat-nba.com/game/37419.html','2015-05-04')
    #14-15赛季
    """getmonth('2014-10')
    getmonth('2014-11')
    getmonth('2014-12')
    getmonth('2015-01')
    getmonth('2015-02')
    getmonth('2015-03')
    getmonth('2015-04')
    getmonth('2015-05')
    getmonth('2015-06')

    #13-14赛季
    getmonth('2013-10')
    getmonth('2013-11')
    getmonth('2013-12')
    getmonth('2014-01')
    getmonth('2014-02')
    getmonth('2014-03')
    getmonth('2014-04')
    getmonth('2014-05')
    getmonth('2014-06')"""

    #12-13赛季
    """getmonth('2012-10')
    getmonth('2012-11')
    getmonth('2012-12')
    getmonth('2013-01')
    getmonth('2013-02')
    getmonth('2013-03')
    getmonth('2013-04')
    getmonth('2013-05')
    getmonth('2013-06')

    #11-12赛季

    getmonth('2011-10')
    getmonth('2011-11')
    getmonth('2011-12')
    getmonth('2012-01')
    getmonth('2012-02')
    getmonth('2012-03')
    getmonth('2012-04')
    getmonth('2012-05')
    getmonth('2012-06')

    #10-11赛季
    getmonth('2010-10')
    getmonth('2010-11')
    getmonth('2010-12')
    getmonth('2011-01')
    getmonth('2011-02')
    getmonth('2011-03')
    getmonth('2011-04')
    getmonth('2011-05')
    getmonth('2011-06')"""

    #getOneMatch('http://www.stat-nba.com/game/27147.html','2010-11-19')

    #09-10赛季
    #getmonth('2009-10')
    getmonth('2009-11')
    getmonth('2009-12')
    getmonth('2010-01')
    getmonth('2010-02')
    getmonth('2010-03')
    getmonth('2010-04')
    getmonth('2010-05')
    getmonth('2010-06')

    #08-09赛季
    getmonth('2008-10')
    getmonth('2008-11')
    getmonth('2008-12')
    getmonth('2009-01')
    getmonth('2009-02')
    getmonth('2009-03')
    getmonth('2009-04')
    getmonth('2009-05')
    getmonth('2009-06')


    print 'Done!'

