#coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    

def getMatchData(url,date,type):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    tables = soup.findAll("table")
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()

    #单节比分
    
    t1 = tables[6].findAll('tr')[1].findAll('td')
    t2 = tables[6].findAll('tr')[2].findAll('td')
    
    num_ofOT=len(t1)
    
    team1=soup.findAll(name="a",attrs={"class":"tlogo"})[0].string.strip()+"队"#客队
    team2=soup.findAll(name="a",attrs={"class":"tlogo"})[1].string.strip()+"队"#主队
    
    print date
    print team1+"VS"+team2
    
    if(team1=="山猫队"):
        team1="黄蜂队"
    elif(team1=="黄蜂队" and date[0:4]+date[5:7]+date[8:10]<'20140707'):
        team1="鹈鹕队"  
          
    if(team2=="山猫队"):
        team2="黄蜂队"
    elif(team2=="黄蜂队" and date[0:4]+date[5:7]+date[8:10]<'20140707'):
        team2="鹈鹕队" 

    
    #客队四节得分
    score1 = [0 for x in range(0, num_ofOT)]
    #主队四节得分
    score2 = [0 for x in range(0, num_ofOT)]

    ot =''
    for i in range(0, num_ofOT):
        score1[i] = t1[i].string
        score2[i] = t2[i].string
    if  num_ofOT>4:
        temp=[0 for x in range(0, num_ofOT-4)]
        for i in range(0,len(temp)):
            temp[i]=score1[i+4]+':'+score2[i+4]
    
        for i in range(0,len(temp)-1):
            ot=ot+temp[i]+";"
        ot=ot+temp[len(temp)-1]
            
        
    #对比数据

    c = tables[26].findAll('tr')
    #得分，快攻得分，内线得分，最大领先，投篮%，罚球%，三分%，技术犯规，恶意犯规，犯满离场，被逐出场
    c1 = [0 for x in range(0, 11)]#客队数据
    c2 = [0 for x in range(0, 11)]#主队数据

    for i in range(0, 11):
        c1[i] = c[i].findAll('td')[0].string
        c2[i] = c[i].findAll('td')[2].string
        if(c1[i]==None):
            c1[i]='0'
        if(c2[i]==None):
            c2[i]='0'    
    
    cc = [0 for x in range(0, 11)]#客队数据    
    for i in range(0,11):
        cc[i]=c1[i]+":"+c2[i]
        #print cc[i]
        
        
    #存比赛简要数据
    
    #获取客队主队ID
    cur.execute("select * from teaminfo where cname = '%s'" %(team1))
    team1ID = cur.fetchall()[0][0]
    cur.execute("select * from teaminfo where cname = '%s'" %(team2))
    team2ID = cur.fetchall()[0][0]
    
    #date[0:4]+date[5:7]+date[8:10]
    year=date[0:4]
    month=date[5:7]
    day=date[8:10]
    matchID=date[0:4]+date[5:7]+date[8:10]+team1ID+team2ID#比赛ID：日期，客队ID，主队ID
    
    score=[0 for x in range(0,4)]
    for i in range(0,4):
        score[i]=score1[i]+":"+score2[i]
    
    #T=[(matchID,type,team1,team2,score[0],score[1],score[2],score[3],ot,cc[1],cc[2],cc[3],cc[4],cc[5],cc[6])]
    
    
    #stmt = "INSERT INTO matchinfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #cur.executemany(stmt, T)
    
    conn.commit()
    cur.close()
    conn.close()
    
    #球员数据  

    p1 = tables[12].findAll('tr')
    num1 = len(p1) - 3
    p2 = tables[15].findAll('tr')
    
    num2 = len(p2) - 3

    #姓名，时间，投篮，三分，罚球，前篮板，后篮板，总篮板，助攻，抢断，盖帽，失误，犯规，得分
    player1 = [[0 for x in range(0, 14)] for y in range(num1)]#客队数据
    player2 = [[0 for x in range(0, 14)] for y in range(num2)]#主队数据

    if(url=='http://nba.sports.sina.com.cn/look_scores.php?id=2015041517'):
        #2015年4月16日，魔术VS篮网，魔术首发球员很脏= =，所以特殊处理
        for i in range(0,5):
            if(i==0):
                player1[i][0]=p1[1].findAll('td')[0].a.string.strip()
                for j in range(1,14):
                    player1[i][j]=p1[1].findAll('td')[j].string.strip()
            else:
                player1[i][0]=p1[i+2].findAll('td')[0].a.string.strip()
                for j in range(1,14):
                    player1[i][j]=p1[i+2].findAll('td')[j].string.strip()
            
        
        for i in range(5,10):
            player1[i][0]=p1[i+3].findAll('td')[0].a.string.strip()
            for j in range(1,14):
                player1[i][j]=p1[i+3].findAll('td')[j].string.strip()
                
        for i in range(10,num1-1):
            player1[i][0]=p1[i+3].findAll('td')[0].a.string.strip()
            for j in range(1,14):
                if(j == 2 or j == 3 or j == 4):   
                    player1[i][j] = '0-0'
                else:
                    player1[i][j] = '0'
               
        player1[num1-1][0]=p1[2].findAll('td')[0].a.string.strip()
        for j in range(1,14):
            player1[num1-1][j]=p1[2].findAll('td')[j].string.strip()
    else:
        for i in range(0, num1):
            if(i < 5):
                if(p1[i + 1].findAll('td')[0].a.string!=None):
                    player1[i][0] = p1[i + 1].findAll('td')[0].a.string.strip()
                else:
                    player1[i][0]='-'
                for j in range(1, 14):
                        player1[i][j] = p1[i + 1].findAll('td')[j].string
            if(i >= 5):
                if(p1[i + 2].findAll('td')[0].a.string!=None):
                    player1[i][0] = p1[i + 2].findAll('td')[0].a.string.strip()
                else:
                    player1[i][0]='-'
                    
                if(p1[i + 2].findAll('td')[1].string == "没有上场" or p1[i + 2].findAll('td')[1].string == "未被激活"):
                    for j in range(1, 14):
                        if(j == 2 or j == 3 or j == 4):   
                            player1[i][j] = '0-0'
                        else:
                            player1[i][j] = '0'
                else:
                    for j in range(1, 14):
                        player1[i][j] = p1[i + 2].findAll('td')[j].string

    for i in range(0, num2):
        if(i < 5):
            if(p2[i + 1].findAll('td')[0].a.string!=None):
                player2[i][0] = p2[i + 1].findAll('td')[0].a.string.strip()
            else:
                player2[i][0] ='-'
            for j in range(1, 14):
                player2[i][j] = p2[i + 1].findAll('td')[j].string
        if(i >= 5):
            if(p2[i + 2].findAll('td')[0].a.string!=None):
                player2[i][0] = p2[i + 2].findAll('td')[0].a.string.strip()
            else:
                player2[i][0]='-'
            if(p2[i + 2].findAll('td')[1].string == "没有上场" or p2[i + 2].findAll('td')[1].string == "未被激活"):
                for j in range(1, 14):
                    if(j == 2 or j == 3 or j == 4):
                        player2[i][j] = '0-0'
                    else:
                        player2[i][j] = '0'
            else:
                for j in range(1, 14):
                    player2[i][j] = p2[i + 2].findAll('td')[j].string
    
    player1ID=[0 for x in range(num1)]
    player2ID=[0 for x in range(num2)]
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    #获得球员id
    t=1
    for i in range(0,num1):
        name=player1[i][0]
        if(name=='蒂莫西-哈达威'):
            name='蒂姆-哈达威'
        if(name=='库兹米奇'):
            name='奥格涅-库兹米奇'
        if(name=='杰夫-潘德格拉夫'):
            name='杰夫-艾尔斯'
        if(name=='莫-哈克莱斯'):
            name='莫里斯-哈克莱斯'
        cur.execute("select * from playerinfo where cname = '%s'" %(name))
        temp=cur.fetchall()
        if(not len(temp)):
            print name
            if(i>4):
                href=p1[i+2].td.a['href']
            else:
                href=p1[i+1].td.a['href']
            newurl="http://nba.sports.sina.com.cn/"+href
            cur.execute("select max(playerid) from playerinfo" )
            newid=int(cur.fetchall()[0][0])+t
            t=t+1
            print newid,t
            addPlayer(newurl,newid)

    for i in range(0,num2):
        name=player2[i][0]
        if(name=='蒂莫西-哈达威'):
            name='蒂姆-哈达威'
        if(name=='库兹米奇'):
            name='奥格涅-库兹米奇'
        if(name=='杰夫-潘德格拉夫'):
            name='杰夫-艾尔斯'
        if(name=='莫-哈克莱斯'):
            name='莫里斯-哈克莱斯'
        cur.execute("select * from playerinfo where cname = '%s'" %(name))
        temp=cur.fetchall()
        if(not len(temp)):
            print name
            if(i>4):
                href=p2[i+2].td.a['href']
            else:
                href=p2[i+1].td.a['href']
            newurl="http://nba.sports.sina.com.cn/"+href
            cur.execute("select max(playerid) from playerinfo" )
            newid=int(cur.fetchall()[0][0])+t
            t=t+1
            print newid,t
            addPlayer(newurl,newid)
       
    conn.commit()
    cur.close()
    conn.close()   
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    #获得球员id
    for i in range(0,num1):
        name=player1[i][0]
        if(name=='蒂莫西-哈达威'):
            name='蒂姆-哈达威'
        if(name=='库兹米奇'):
            name='奥格涅-库兹米奇'
        if(name=='杰夫-潘德格拉夫'):
            name='杰夫-艾尔斯'
        if(name=='莫-哈克莱斯'):
            name='莫里斯-哈克莱斯'
        cur.execute("select * from playerinfo where cname = '%s'" %(name))
        player1ID[i] = cur.fetchall()[0][0]
        
        isfirst='0'
        if i<5:
           isfirst='1'
        #T=[(matchID,team1ID,team1,player1ID[i],player1[i][0],player1[i][1],player1[i][2],player1[i][3],player1[i][4],player1[i][5],player1[i][6],player1[i][7],player1[i][8],player1[i][9],player1[i][10],player1[i][11],player1[i][12],player1[i][13],isfirst)]
        #stmt = "INSERT INTO playerdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #cur.executemany(stmt, T)
        
    for i in range(0,num2):
        name=player2[i][0]
        if(name=='蒂莫西-哈达威'):
            name='蒂姆-哈达威'
        if(name=='库兹米奇'):
            name='奥格涅-库兹米奇'
        if(name=='杰夫-潘德格拉夫'):
            name='杰夫-艾尔斯'
        if(name=='莫-哈克莱斯'):
            name='莫里斯-哈克莱斯'
        cur.execute("select * from playerinfo where cname = '%s'" %(name))
        player2ID[i] = cur.fetchall()[0][0]
        
        isfirst='0'
        if i<5:
           isfirst='1'
        #T=[(matchID,team2ID,team2,player2ID[i],player2[i][0],player2[i][1],player2[i][2],player2[i][3],player2[i][4],player2[i][5],player2[i][6],player2[i][7],player2[i][8],player2[i][9],player2[i][10],player2[i][11],player2[i][12],player2[i][13],isfirst)]
        #stmt = "INSERT INTO playerdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #cur.executemany(stmt, T)
       
    conn.commit()
    cur.close()
    conn.close() 
    
def addPlayer(url,id):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    url=soup.meta['content'].split(';')[1].split('url=')[1]
    
    getOnePlayer(url, id)
    
        
def getMonthData(year,month):
    url="http://nba.sports.sina.com.cn/match_result.php?day=0&years="+year+"&months="+month+"&teams="
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    matchs=soup.findAll('table')[1].findAll('tr')
    if(soup.findAll('table')[1].tr==None):
        print "This month has no games"
        return
    num=len(matchs)
     
    date=""
    for i in range(0,num):
        t=matchs[i].findAll('td')
        #print t[0].string
        if(t[0].string.find("星期")!=-1):
            date=year+"年"+t[0].string.split("星期")[0]
        elif(t[0].string.find("完场")!=-1):
            if(t[1].string=="常规赛" or t[1].string=="季后赛"):
                href=t[8].a["href"]
                html="http://nba.sports.sina.com.cn/"+href
                getMatchData(html,date,t[1].string)
                
   
def getOnePlayer(url,id):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
 
    base=soup.findAll('p')[2]
    temp=base.a.nextSibling.split("|")
    
    cname=base.strong.string#中文名
    if(cname[0]=='-' and len(cname)>2):
        cname=cname[1:]
        
    ename=base.strong.nextSibling.split("(")[1].split(")")[0]#英文名
    team=base.a.string#球队
    number=temp[1].strip()#号码
    position=temp[2].strip()#位置
    
    line=soup.findAll('table')[1].findAll('tr')
    
    birth=line[0].findAll('td')[2].string#生日
    age=line[0].findAll('td')[4].string#年龄
    birth_place=line[1].findAll('td')[1].string#出生地
    school=line[1].findAll('td')[3].string#毕业学校
    height=line[2].findAll('td')[1].string#身高
    weight=line[2].findAll('td')[3].string#体重
    inNBA=line[3].findAll('td')[1].string#进入NBA
    #yearInNBA=line[3].findAll('td')[3].string#球龄
    
    #写入数据库
    Pid=str(id)
    if(len(Pid)<3):
        for j in range(0,3-len(Pid)):
           Pid='0'+Pid
    T=[(Pid,cname,ename,team,number,position,birth,age,birth_place,school,height,weight,inNBA)]
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    stmt = "INSERT INTO playerinfo(playerid,cname,ename,team,number,position,birth,age,birthplace,school,height,weight,inNBA) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(stmt, T)

    conn.commit()
    cur.close()
    conn.close()  
    
def getPlayer():
    #id=1
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    cur.execute("select max(playerid) from playerinfo" )
    idstr = cur.fetchall()
    if(not idstr[0][0]):
        id=0
    else:
        id=int('0'+idstr[0][0])
        print id
    conn.commit()
    cur.close()
    conn.close()
    
    headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }  
    req = urllib2.Request( url = "http://nba.sports.sina.com.cn/players.php?key=e",headers = headers)
    html  = urllib2.urlopen(req).read()

    #url="http://nba.sports.sina.com.cn/players.php?key=e" 
    #html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    lines=soup.findAll('table')[1].findAll('tr')
    for i in range(0,len(lines)):
        if(lines[i].td.string==None):
            for j in range(0,3):
                p=lines[i].findAll('td')[j]
                if(p.a!=None):
                    href=p.a["href"]
                    url="http://nba.sports.sina.com.cn/"+href
                    if(updateOnePlayer(url)==0):
                        id=id+1
                        getOnePlayer(url,id)

def updateOnePlayer(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    base=soup.findAll('p')[2]
    temp=base.a.nextSibling.split("|")

    cname=base.strong.string#中文名
    if(cname[0]=='-' and len(cname)>2):
        cname=cname[1:]
    ename=base.strong.nextSibling.split("(")[1].split(")")[0]#英文名
    team=base.a.string#球队
    number=temp[1].strip()#号码
    position=temp[2].strip()#位置

    line=soup.findAll('table')[1].findAll('tr')

    birth=line[0].findAll('td')[2].string#生日
    age=line[0].findAll('td')[4].string#年龄
    birth_place=line[1].findAll('td')[1].string#出生地
    school=line[1].findAll('td')[3].string#毕业学校
    height=line[2].findAll('td')[1].string#身高
    weight=line[2].findAll('td')[3].string#体重
    inNBA=line[3].findAll('td')[1].string#进入NBA

    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from playerinfo where cname = '%s' and birth='%s'" %(cname,birth))
    list = cur.fetchall()
    if len(list):
        T=[(''+list[0][0],cname,ename,team,number,position,birth,age,birth_place,school,height,weight,inNBA)]
        stmt = "replace INTO playerinfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(stmt, T)
        conn.commit()
        cur.close()
        conn.close()
        return 1
    else:
        return 0

def getOneTeam(url,ename,id):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    lines=soup.findAll('table')[1].findAll('tr')
    name=lines[0].findAll('td')[1].string#中文名
    city=lines[1].findAll('td')[1].string#城市
    t=lines[7].findAll('td')[1].string.split(' ')
    partition=t[0]#分区
    division=t[1]#赛区
    court=lines[9].findAll('td')[1].string#球场
    inNBA=lines[10].findAll('td')[1].string#进入NBA

    pos=court.find(';')
    if(pos>=0):
        court=court[0:pos]+court[(pos+1):]

    Tid=str(id)
    if(len(Tid)<2):
        for j in range(0,2-len(Tid)):
           Tid='0'+Tid

    T=[(Tid,name,ename,city,partition,division,court,inNBA)]

    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    stmt = "INSERT INTO teaminfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(stmt, T)
    conn.commit()
    cur.close()
    conn.close()

def getTeam():
    id=1
    url="http://nba.sports.sina.com.cn/teams.php?dpc=1" 
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    lines=soup.findAll('table')[1].findAll('tr')
    for i in range(2,7):
        teams=lines[i].findAll('td')
        for j in range(0,6):
            href=teams[j].a['href']
            ename=href.split('/')[4].split('.')[0]
            if(ename=='Trail%20Blazers'):
                t=ename.split('%20')
                ename=t[0]+" "+t[1]
            if(updateOneTeam(href,ename)==0):
                getOneTeam(href,ename,id)
                id=id+1


def updateOneTeam(url,ename):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    lines=soup.findAll('table')[1].findAll('tr')

    name=lines[0].findAll('td')[1].string#中文名
    city=lines[1].findAll('td')[1].string#城市
    t=lines[7].findAll('td')[1].string.split(' ')
    partition=t[0]#分区
    division=t[1]#赛区
    court=lines[9].findAll('td')[1].string#球场
    inNBA=lines[10].findAll('td')[1].string#进入NBA

    pos=court.find(';')
    if(pos>=0):
        court=court[0:pos]+court[(pos+1):]

    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='se3',charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from teaminfo where cname = '%s'" %name)
    list = cur.fetchall()
    if len(list):
        T=[(list[0][0],name,ename,city,partition,division,court,inNBA)]
        stmt = "replace INTO teaminfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(stmt, T)
        conn.commit()
        cur.close()
        conn.close()
        return 1
    else:
        return 0

    
if __name__=="__main__":  
    """print 'getPlayer' 
    getPlayer()
    print 'getTeam'
    getTeam()"""
    
    #getMatchData('http://nba.sports.sina.com.cn/look_scores.php?id=2015041517','2014年04月16日','常规赛')
    
    id=450
    url=[]
    
    #14-15赛季
    #getMonthData("2012",'10')
    getMonthData("2012",'11')
    getMonthData("2012",'12')
    getMonthData("2013",'01')
    getMonthData("2013",'02')
    getMonthData("2013",'03')
    getMonthData("2013",'04')
    getMonthData("2013",'05')
    getMonthData("2013",'06')
    
    #13-14赛季
    
        
    







