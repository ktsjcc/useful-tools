# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:46:08 2020
This script is used to auto-backup master branch from GitLab.
Author: Mike Zhao
"""
import time
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import datetime
import tarfile
import shutil



##初始化list
kk=[]
page=[]
file_name=[]
down_url=[]


#获取当前的日期
now=datetime.datetime.now()
current_date=now.strftime('%Y-%m-%d')
#创建文件夹
back_path='D:\\backup\\'
path_hyde='D:\\backup\\'+current_date+'\\hyde\\'
os.makedirs(path_hyde) 

path_naja='D:\\backup\\'+current_date+'\\naja\\'
os.makedirs(path_naja) 



#无窗登陆界面

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


#有窗登录界面
#driver = webdriver.Chrome()
#driver.maximize_window() 
####################

driver.get("http://git.hyde-health.com/users/sign_in#login-pane")
driver.find_element_by_id('user_login').send_keys('#######') #username
time.sleep(1)

driver.find_element_by_id('user_password').send_keys('######')   #password
time.sleep(1)


driver.find_element_by_xpath('//*[@id="new_user"]/div[5]/input').click()
s = requests.session()     #获得session

#根据不同的浏览器，配置headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Cookie": "_gitlab_session=4f57a6e786e50b473ddfe48c432d974d",
    'Connection':'keep-alive'
    }


##获取最后一页的页码
response = s.get('http://git.hyde-health.com/',headers=headers)  
soup= BeautifulSoup(response.content,'html.parser')
last_page=soup.select('li[class="page-item js-last-button"]')
patt2=re.compile(r'\d+',re.S)
last_num=patt2.findall(str(last_page))

for i in range(1,int(last_num[0])+1,1):
    url='http://git.hyde-health.com/?non_archived=true&page='+str(i)+'&sort=latest_activity_desc'
    page.append(url)

for login_url in page:
    
    response = s.get(login_url,headers=headers)
    soup= BeautifulSoup(response.content,'html.parser')
    ls=soup.select('a[class="project"]')
    patt=re.compile(r'<a.*?href="(.*?)"',re.S)
    zzr=patt.findall(str(ls))
    kk=kk+zzr  #kk中存有所有的文件名





#下载管理

for name in kk:
    down_url.append('http://git.hyde-health.com'+name+'/-/archive/master/'+kk[0].split('/')[-1]+'-master.zip')

 
for item in down_url:
    file_name=item.split('/')[3:6]
    file_name=('-').join(file_name).rstrip('-')+'.zip'

    try:
        r=s.get(item,headers=headers)
        
        time.sleep(2)
        
        if item.split('/')[3]=='hyde': 
              
            os.chdir(path_hyde)
            with  open (file_name,  "wb" ) as code:
                code.write(r.content)
        
        elif item.split('/')[3]=='naja':
            
          
            os.chdir(path_naja)
            
            with open(file_name,  "wb" ) as code:
                code.write(r.content)
    except:
        print('no files in '+item)
        
  
    else:
        print('Successfully downloaded '+file_name)



##归档打包
os.chdir(back_path)
with tarfile.open(current_date+'_backup.tar',mode="w:gz") as tar:
    tar.add(current_date)


if os.path.exists(current_date+'_backup.tar'):
    shutil.rmtree(current_date)








