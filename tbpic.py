
from bs4 import BeautifulSoup#通过python展现xml结构信息
from urllib.request import urlopen
from selenium import webdriver#可以让浏览器自动加载页面，获取需要的数据
import os
import threading
import re#正则

def main():
    driver=webdriver.PhantomJS(executable_path='/home/shiyanlou/phantomjs/bin/phantomjs')#浏览器的地址
    driver.get("https://mm.taobao.com/search_tstar_model.htm?")#目标网页地址
    bs0bj=BeautifulSoup(driver.page_source,"lxml")#解析html语言,page_source是网页全部html源码
    fp=open('mm.txt','r+')#用于将主页信息储存
    fp.write(driver.find_element_by_id('J_GirlsList').text)#用于获取主页上姓名，所在地，身高，体重
    print("[*]OK GET MM's BOOK")
    MMsinfoUrl=bs0bj.findAll("a",{"href":re.compile("\/\/.*\.htm\?(userID=)\d*")})#解析出个人主页
    imagesUrl=bs0bj.findAll("img",{"data-ks-lazyload":re.compile(".*\.jpg")})#解析出封面图片
    items=fp.readlines()
    content1=[]
    n=0
    m=1
    while(n<14):
        content1.append([items[n].strip('\n'),items[m].strip('\n')])
        n+=3
        m+=3
    content2=[]
    for MMinfoUrl in MMsinfoUrl:
        content2.append(MMinfoUrl["href"])
    contents=[[a,b] for a,b in zip(content1,content2)]
    i=0
    while(i<5):#保护带宽
        print("[*]MM's name:"+contents[i][0][0]+" with"+contents[i][0][1])
        print("[*]saving....."+contents[i][0][0]+" in the folder")
        perMMpageUrl="http:"+contents[i][1]
        path='/home/shiyanlou/photo/'+contents[i][0][0]
        mkdir(path)
        getperMMpageImg(perMMpageUrl,path)
        i+=1
    fp.flush()
    fp.close()
    number=1
    for imageUrl in imagesUrl:#将封面图片存进文件夹
        url="https:"+str(imageUrl["data-ks-lazyload"])
        html=urlopen(url)
        data=html.read()
        fileName='/home/shiyanlou/photo/mm'+str(number)+'.jpg'
        fph=open(fileName,"wb")
        print("[+]Loading MM........"+fileName)
        fph.write(data)
        fph.flush()
        fph.close()
        number+=1
    driver.close()
def mkdir(path):
    isExists=os.path.exists(path)#判断是否存在
    if not isExists:
        print("[*]新建了"+path+"文件夹"）
        os.makedirs(path)
    else:
        print("[+]名为"+path+"已经创建了")
def getperMMpageImg(MMURL,MMPath):
    owndriver=webdriver.PhantomJS(executable_path='/home/shiyanlou/phantomjs/bin/phantomjs')
    owndriver.get(MMURL)
    print("[*]Opening....MM........")
    own0bj=BeautifulSoup(owndriver.page_source,"lxml")
    perMMimgs=own0bj.findAll("img",{"src":re.compile(".*\.jpg")})
    number=2
    for perMMimg in perMMimgs:
        ImgPath="https:"+str(perMMimg["src"])#处理成标准超文本信息
        try:
            html=urlopen(ImgPath)
            data=html.read()
            fileName=MMPath+"/"+str(number)+'.jpg'
            fp=open(fileName,'wb')
            print("[+]Loading....")
            fp.write(data)
            fp.close()
            fp.flush()
            number+=1
        except Exception:
            print("[!]Address Error!!!!!!!!!!!")
if __name__=='__main__':
    main()















              



















