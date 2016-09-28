# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 10:55:53 2016

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

#get current Directory
path = os.getcwd()
file_idandsecret = os.path.join(path,os.path.normpath('dataset/idAndSecrets_zheng.csv'))
file_useids = os.path.join(path,os.path.normpath('dataset/ua_user_list.txt'))
file_output = os.path.join(path,os.path.normpath('dataset/user_tips_0616_pred.csv'))
file_output2 = os.path.join(path,os.path.normpath('dataset/user_list_exct.csv'))


def getWebClient(client_id, client_secret):
    callback = 'https://foursquare.com/oauth2/default'
    client = foursquare.Foursquare(client_id, client_secret, redirect_uri=callback)
    auth_uri = client.oauth.auth_url()
    
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    acceptEncoding = 'gzip, deflate'
    acceptLanguage = 'zh-CN,zh;q=0.8'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    cookie = 'bbhive="HJISFB2NDH423JPP3ZLNP54T0XC45V%3A%3A1522215324"; PixelDensity=1; disableFacebookAutologin=1; XSESSIONID=fsag198083~1a9qmcbueahpgc0nj3fqy7eik; oauth_token=VKYWV2VWZ0I0YKLONHA3VJ5CGJO0T1BELNESAYPA3QXFEVEV-0; __utmt=1; __utma=51454142.1357868271.1459143326.1459503779.1459503873.3; __utmb=51454142.52.10.1459503873; __utmc=51454142; __utmz=51454142.1459503873.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
    headers = {'Accept': accept, 'Accept-Encoding': acceptEncoding, 'Accept-Language': acceptLanguage, 'Connection': 'keep-alive', 'Host': 'foursquare.com','User-Agent': userAgent, 'Cookie': cookie, 'Upgrade-Insecure-Requests': '1'}
    s = requests.Session()
    s.headers.update(headers)
    r = s.post(auth_uri, {'fs-request-signature': '5acd013e9a401d99730afe2670ca6cd2ef963467:1459845793264', 'shouldAuthorize': 'true'})
    url = r.url
    code = url[-52:-4]
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    return client
    
def getInfos(client, user_id):
    pageNum = getPages(client, user_id)
    if pageNum==0:
        pass
    page = 0
    while page < pageNum:
        use_tips = client.users.tips(user_id, params={'limit': '500', 'offset': page})
        items = use_tips['tips']['items']
        infos = set()
        for item in items:
            ven_id = item['venue']['id']
            text = item['text'].strip().replace('\n',' ').replace('\r\n',' ').replace('\r',' ').replace('|',' ')           
            createdAt = item['createdAt']
            
            info_str = str(user_id) +'|'+ str(ven_id) +'|'+ str(text) +'|'+ str(createdAt)       
              
            infos.add(info_str) 
        saveInfos(infos,file_output)
        page = page + 1

        
def getPages(client, user_id):
    use_tips = client.users.tips(user_id, params={'limit': '500'})
    count = use_tips['tips']['count']
    if count==0:
        saveInfos_2(user_id,file_output2)
    print('count of items: ', count)    
    pageNum = int(count / 500) + 1  
    print('number of item pages(500 per page): ', pageNum)
    return pageNum

def getIdAndSecret(df, index):
    client_id = df.ix[index]['client_id']
    client_secret = df.ix[index]['client_secret']
    return client_id,client_secret

def saveInfos(data,file_output):
    with open(file_output,'a',encoding='utf-8') as g:
        for st in data:
            #print(st)
            g.write(st+'\n')
        g.close()
def saveInfos_2(data,file_output):
    with open(file_output,'a',encoding='utf-8') as g:
        g.write(str(data)+'\n')
       

def run():
    df_clients = pd.read_csv(file_idandsecret)   
    df_ids = pd.read_csv(file_useids, names=['use_id'])
    key = 0    
    client_id,client_secret = getIdAndSecret(df_clients,key)
    print('current client_id:{0},client_secret:{1}'.format(client_id,client_secret))
    client = getWebClient(client_id, client_secret)

    for venueid in df_ids['use_id']:
        print('use_id: ', venueid)
        try:
            getInfos(client,venueid)
        except RateLimitExceeded as e:
            print(sys.stderr, 'Encountered API Exception:', e)
            if key < df_clients.index.size - 1:
                key += 1
            else:
                key = 0
                time.sleep(1800)
            client_id, client_secret = getIdAndSecret(df_clients, key)
            print('current client_id:{0}, client_secret:{1}'.format(client_id, client_secret))
            client = getWebClient(client_id, client_secret)
        except FoursquareException as e:
            print(sys.stderr, 'Response format invalid(invalid venueid):', e)
            pass
        except Exception as e:
            pass

if __name__ == '__main__':
    run()     
