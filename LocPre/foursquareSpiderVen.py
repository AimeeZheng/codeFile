# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:26:38 2016

@author: zhengyaolin
"""

import foursquare
import requests
import sys
import pandas as pd
import os
import time
from foursquare import FoursquareException
from foursquare import RateLimitExceeded
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#get current Directory
path=os.getcwd()
file_idandsecret=os.path.join(path,os.path.normpath('../dataset/idAndSecrets.csv'))
file_venueids=os.path.join(path,os.path.normpath('../dataset/venue_NY_CA_list.txt'))
file_output=os.path.join(path,os.path.normpath('../dataset/venue_NY_CA_20160516.csv'))
#pattern=r'[0-9a-zA-Z\|\-\. ]'
#regex=re.compile(pattern,re.IGNORECASE)

def getWebClient(client_id, client_secret):
    callback = 'https://foursquare.com/oauth2/default'
    client = foursquare.Foursquare(client_id, client_secret, redirect_uri=callback)
    auth_uri = client.oauth.auth_url()
    
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    acceptEncoding = 'gzip, deflate'
    acceptLanguage = 'zh-CN,zh;q=0.8'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    cookie = 'oauth_token=E3JPIMKYBLHC2UIYJ2GVZQQ4ESF4GU5PAOWW0Y2LPGFWKJSV-0; bbhive=Z3SPVVNE5XVVQEF5HCNBUV3PIDMF5C%3A%3A1522227514; XSESSIONID=fsae18086~5zro8b169d42n9zpemutl2af; PixelDensity=1; __utmt=1; __utma=51454142.401138352.1459155347.1459306484.1459313031.3; __utmb=51454142.7.10.1459313031; __utmc=51454142; __utmz=51454142.1459313031.3.3.utmcsr=developer.foursquare.com|utmccn=(referral)|utmcmd=referral|utmcct=/overview/auth'
    headers = {'Accept': accept, 'Accept-Encoding': acceptEncoding, 'Accept-Language': acceptLanguage, 'Connection': 'keep-alive', 'Host': 'foursquare.com','User-Agent': userAgent, 'Cookie': cookie, 'Upgrade-Insecure-Requests': '1'}
    s = requests.Session()
    s.headers.update(headers)
    r = s.post(auth_uri)
    url = r.url
    code = url[-52:-4]
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    return client
    
#根据venueid取得相关信息(id,location,tips,tags,name,categories)
def getInfos(client,venue_id):
    ven_info = client.venues(venue_id)
    if len(ven_info)!=0:        
        #get name        
        
        name = ven_info['venue']['name'].replace('|',',') #名字
        
        latitude = ven_info['venue']['location']['lat'] #纬度 
        longitude = ven_info['venue']['location']['lng'] #经度 
            
        #get country
        country=''
        if 'cc' in ven_info['venue']['location'].keys():
            country=ven_info['venue']['location']['cc']#国家
            
        #get city
        citys=''
        if 'state' in ven_info['venue']['location'].keys():
            citys=ven_info['venue']['location']['state'] 
        #get tips counts
        tips_count=''
        if 'tipCount' in ven_info['venue']['stats'].keys():
            tips_count=ven_info['venue']['stats']['tipCount']#number of tips here
        #get checkins counts
        checkins_count=''
        if 'checkinsCount' in ven_info['venue']['stats'].keys():
            checkins_count=ven_info['venue']['stats']['checkinsCount']#total checkins ever here
        #get users count
        users_Count=''
        if 'usersCount' in ven_info['venue']['stats'].keys():
            users_Count=ven_info['venue']['stats']['usersCount']#total users who have ever checked in here
        #get visits_count
        visits_Count=''
        if 'visitsCount' in ven_info['venue']['stats'].keys():
            visits_Count=ven_info['venue']['stats']['visitsCount']#total users who have ever visit in here
                    
        #get liked user count
        likes_count=''
        if 'likes' in ven_info['venue'].keys():
            likes_count=ven_info['venue']['likes']['count']#The count of users who have liked this venue
            
        #get venue descript
        venue_descript=''
        if 'description' in ven_info['venue'].keys():
            venue_descript=ven_info['venue']['description'].strip().replace('\n',' ').replace('\r\n',' ').replace('\r',' ').replace('|',' ')#Description of the venue provided by venue owner.
        #process data
        #s=regex.findall(venue_descript)
        #st=[item for item in s if len(item)>0]
        #venue_descript=''.join(st)
        
        #print(repr(venue_descript))
        #get venue rating
        rating='' 
        if 'rating' in ven_info['venue'].keys():
            rating=ven_info['venue']['rating']#Numerical rating of the venue (0 through 10).
                         
        #get tags
        tags = ven_info['venue']['tags'] #标签
        tag_str = ''            
        if len(tags) != 0:                
            for tag in tags:
                tag_str = tag_str + tag.replace('|',',') +','
           
        #get categories
        categorys=ven_info['venue']['categories']
        cate_str=''
        if len(categorys)!=0:
            for dc in categorys:
                cate_str=cate_str+dc['name'].replace('|',',')+','
            
        infos=set()           
        info_str=str(venue_id)+'|'+str(name)+'|'+str(latitude) +'|'+str(longitude)+'|'+str(cate_str)+'|'+str(country)+'|'+str(citys)+'|'+str(venue_descript)+'|'+str(tag_str)+'|'+str(rating)+'|'+str(likes_count) +'|'+str(tips_count)+'|'+str(checkins_count)+'|'+str(users_Count) +'|'+str(visits_Count)                    
        #info_str=str(venue_id)+'|'+str(cate_str)        
        infos.add(info_str) 
        saveInfos(infos)   

def saveInfos(data):
    with open(file_output,'a') as g:
        for st in data:
            #print(st)
            g.write(st+'\n')
        g.close()
    #infos.to_csv('data/venue_info.csv', index = None, mode = 'a')
    
def getIdAndSecret(df,index):
    client_id = df.ix[index]['client_id']
    client_secret = df.ix[index]['client_secret']
    return client_id,client_secret
 
def run():  

    df_clients = pd.read_csv(file_idandsecret)   
    df_ids = pd.read_csv(file_venueids,names=['venue_id'])
    key = 0    
    client_id,client_secret = getIdAndSecret(df_clients,key)
    print('current client_id:{0},client_secret:{1}'.format(client_id,client_secret))
    client = getWebClient(client_id, client_secret)
    
    for venueid in df_ids['venue_id']:
        print('venueid:', venueid)
        #print('client_id:', client_id)
        try:
            getInfos(client,venueid)
        except RateLimitExceeded as e:
            print(sys.stderr, 'Encountered API Exception:', e)
            #time.sleep(300)
            if key<df_clients.index.size-1:
                key+=1
            else:
                key=0
                time.sleep(1800)
            client_id,client_secret = getIdAndSecret(df_clients,key)
            print('current client_id:{0},client_secret:{1}'.format(client_id,client_secret))
            client = getWebClient(client_id, client_secret)
        except FoursquareException as e:
            print(sys.stderr, 'Response format invalid(invalid venueid): ', e)
            pass  

if __name__ == '__main__':
    run()    
    
