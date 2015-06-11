#coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import MySQLdb
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

def getPlayer(url):
    #html = urllib2.urlopen(url).read()
    headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }  
    req = urllib2.Request( url = url,headers = headers)
    html  = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    
    list=soup.find('div',attrs={"class":"playerList"}).findAll('div',attrs={"class":"name"})
    num=len(list)
    player=[0 for x in range(num)]
    href=[0 for x in range(num)]
    
    for i in range(0,num):
        player[i]=list[i].a.span.string.strip()
        href[i]=list[i].a['href']
        t=href[i].split('/')[2]
        url='http://www.stat-nba.com/player/'+t
        getOnePlayer(url,player[i])
    
    
def getOnePlayer(url,name):
    headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }  
    req = urllib2.Request( url = url,headers = headers)
    html  = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    
    
    
    a=soup.find('div',attrs={"class":"detail"}).findAll('div',attrs={"class":"row"})
    colom=['全　　名:','位　　置:','身　　高:','体　　重:','出生日期:','出生城市:','高　　中:','大　　学:','球衣号码:','选秀情况:','当前薪金:']
    v=['' for x in range(11)]
    for i in range(len(a)):
        if(a[i].div):
            for j in range(len(colom)):
                if(a[i].div.string.strip()==colom[j] and colom[j]=='选秀情况:'):
                    v[j]=a[i].div.nextSibling.strip().split('被')[0]
                elif(a[i].div.string.strip()==colom[j]):
                    v[j]=a[i].div.nextSibling.strip()
    
    for i in range(len(a)):
        if(a[i].div==None):
            continue
        if(a[i].div.string.strip()=='球衣号码:' and a[i].a!=None and a[i].a.string!='详情'):
            v[8]=v[8]+a[i].a.string+'退役'
    
    #for i in range(11):
     #   print colom[i],v[i]
         
            
    #print '=============='
    cname=''
    ename=''
    t=name.split('/')
    if(len(t)==1):
        cname=ename=t[0]
    else:
        cname=t[0]
        ename=t[1]
        
    print cname
        
    image=soup.find('div',attrs={"class":"image"}).img['src']
    imageurl='http://www.stat-nba.com'+image
    save_file('F:/player',ename+'.jpg',get_file(imageurl))
    
    
    T=[(cname,ename,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10])]
    conn = MySQLdb.connect(host='localhost', user='root', passwd='941016', db='nba',charset='utf8')
    cur = conn.cursor()
    
    if(cname.find('\'')!=-1):
        d=cname.find('\'')
        cname=cname[0:d]+'\\'+cname[d:]
    cur.execute("select * from playerinfo where cname = '%s'" %(cname))
    temp=cur.fetchall()
    if(not len(temp)):   
        stmt = "INSERT INTO playerinfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(stmt, T)
    conn.commit()
    cur.close()
    conn.close()
    
def mkdir(path):
    # 去除左右两边的空格
    path=path.strip()
    # 去除尾部 \符号
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path) 
    return path    

def save_file(path, file_name, data):
    if data == None:
        return
    
    mkdir(path)
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
    
def get_file(url):
    try:
        headers = { 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }  
        req = urllib2.Request( url = url,headers = headers)
        data = urllib2.urlopen(req).read()
        return data
    except BaseException, e:
        print e
        return None
    
if __name__=="__main__":  
    c=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    #for i in range(22):
    #getPlayer('http://www.stat-nba.com/playerList.php?il=q&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=r&lil=0')
    
    #getPlayer('http://www.stat-nba.com/playerList.php?il=s&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=t&lil=0')
    
    #getPlayer('http://www.stat-nba.com/playerList.php?il=u&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=v&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=w&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=x&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=y&lil=0')
    #getPlayer('http://www.stat-nba.com/playerList.php?il=z&lil=0')

    
    #getOnePlayer('http://www.stat-nba.com/player/2451.html','杰克-马克罗斯基/Jack McCloskey')
    
    
    
    
    