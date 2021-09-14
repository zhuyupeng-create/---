# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 21:07:01 2021

@author: zhuyupeng
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"}
aa = {
      "channelid": "233424",
      "searchword": "粮食",
      "page": "3"
      }

#获取文章的真实URL
def get_long_url():
    short_url = 'http://www.moa.gov.cn/was5/web/search?'
    real_url=[]
    #构建参数，并发送get请求
    r = requests.get(url = short_url, params=aa,headers=headers)
    #print(r)
    #用BS4方法进行解析
    soup = BeautifulSoup(r.content,"html.parser")
    #print(soup)
    #寻找当前页面所有连接
    bb = soup.find_all("a",attrs= {"class":"dcotitlename"})
    #print(bb)
    time.sleep(0.5)#睡一会，防止被封
    #得到每一个url并封装到列表中
    for link in bb:
        href = link.get("href")
        real_url.append(href)  
        #print(real_url)
    return real_url
    

#获取目标html并保存文本，用lxml方法        
def get_subject_id(really_url):
    #枚举
    for href in really_url:
        #print(href)
        chid_page = requests.get(href, headers=headers)
        #print(chid_page)
        #decode() 进行解码
        html_str = chid_page.content.decode('UTF-8')
        #print(html_str)
        #将字符串传入 etree.HTML() 构建了一个 lxml.etree._Element 对象。
        html = etree.HTML(html_str)    
        try:
            #中央发放的通知和地方项目召开的结构不一致，需要分类进行提取，需要手动更改
            #biaoti = html.xpath('//h2[@class="xxgk_title"]//text()') 
            #result_1 = html.xpath('//div[@class="gsj_htmlcon_bot"]//text()')
            #获取文章的标题
            biaoti = html.xpath('//h1[@class="bjjMTitle"]//text()')
            #标题改换成字符串格式
            biaoti = "".join(biaoti)
            #获取文本
            result_1 = html.xpath('//div[@class="arc_body mg_auto w_855 pd_b_35"]//text()')
            result_1  = "".join(result_1)                
            #result_1 = result_1.replace(',', '').replace("\xa0", '').replace("\r\n", "").replace("\u3000\u3000", "")
            #检查
            print(biaoti)
            print(result_1) 
            
            #if not os.path.exists(biaoti) :
                #os.mkdir(biaoti)
            #对目标文件进行保存
            with open (biaoti, "w",encoding="utf-8") as f:		#保存小说
                f.write(result_1)
            
        #  本语句会根据程序进行从而进行报错             
        except Exception as e:
            print("原因:", e)
        time.sleep(0.5)
         
def main():
    really_url = get_long_url()
    time.sleep(0.5)
    #print(really_url)
    get_subject_id(really_url)
    
    

if __name__ == '__main__':
    main()

