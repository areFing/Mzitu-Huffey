#coding:utf-8
import requests
from bs4 import BeautifulSoup
import random
import urllib2
import urllib
import os.path
def getPage():
    return ['xinggan','japan','taiwan','mm']

def getSoup(url):
    my_headers = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36']
    header = {"User-Agent":my_headers}
    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup

def get_links(url):
    #获取单个妹子图共有多少张照片
    soup=getSoup(url)
    all_=soup.find_all('a')
    nums=-1
    for i in all_:
        span=i.find_all('span')
        if span:
            nums.append(span[0].text)
    return nums

def savePhoto(url,catogryname,filename):
    if not os.path.exists('MeiZiTu'):
        os.mkdir('MeiZiTu')
    dirName=os.path.join('MeiZiTu',catogryname)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    savePath=os.path.join(dirName,filename+'.jpg')
    urllib.urlretrieve(url, savePath)

def getEachPageItemNumbers(url):
    soup=getSoup(url)
    pages=soup.find('div',class_='pagenavi').find_all('a')
    return int(pages[-2].text)

def downPhoto(url,fileName):
    urllib.urlretrieve(url, fileName)


def getPageCount(url):
    #获取每个分类的页数
    soup=getSoup(url)
    pages=soup.find_all('a',class_='page-numbers')
    maxPage=int(pages[-2].text)
    return maxPage
def getPicInfo(urllist):
    for url in urllist:
        if not os.path.exists('MeiZiTu'):
            os.mkdir('MeiZiTu')
        catogryPath=os.path.join('MeiZiTu',url)
        if not os.path.exists(catogryPath):
            os.mkdir(catogryPath)
        #url=url+'page/2' 由于妹子图url比较有规律,可以简单粗暴循环拼接
        #为了严谨本例还是先找有多少页
        catogry=url
        catogryUrl='http://www.mzitu.com/'+url+'/'
        pages=getPageCount(catogryUrl)
        for i in range(1,pages+1):
            itemUrl=catogryUrl+'page/'+str(i) #当前页每一个item
            html=getSoup(itemUrl)
            itemList=html.find('ul',id='pins').find_all('li')
            for t in itemList:
                time=t.find('span',class_='time').text
                view=t.find('span',class_='view').text
                name=t.find('a',target='_blank').find('img',class_='lazy')['alt']
                dirName=os.path.join(catogryPath,name)
                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                else:
                    break
                finalurl=t.find('a',target='_blank')['href']
                finalCount=getEachPageItemNumbers(finalurl)
                count=1
                for f in range(1,finalCount+1):
                    lastUrl=finalurl+'/'+str(f)
                    html=getSoup(lastUrl)
                    picUrl=html.find('div',class_='main-image').find('img')['src']
                    savePath = os.path.join(dirName, str(count) + '.jpg')
                    try:
                        downPhoto(picUrl,savePath)
                        count+=1
                    except urllib.ContentTooShortError:
                        print 'Network conditions is not good.Reloading.'
                        downPhoto(picUrl, savePath)
                        count+=1
def getZiPai():
    countCount=1
    url='http://www.mzitu.com/zipai/'
    soup=getSoup(url)
    pages=soup.find_all('a',class_='page-numbers')
    maxPage=int(pages[-1].text)
    for j in range(1,maxPage+1):
        url='http://www.mzitu.com/zipai/comment-page-'+str(j)
        currentPage=getSoup(url)
        picList=currentPage.find('div',id='comments').find_all('img')
        print '当前是第'+str(j)+'页'
        for a in picList:
            savePhoto(a['src'],'ZiPai','ZiPai'+str(countCount))
            countCount+=1
    print '所有自拍图片已经下载完毕'
if __name__=='__main__':
    #妹子自拍分类需要特殊处理,需要的自己取消注释即可下载
    #getZiPai()
    getPicInfo(getPage())
    print '程序执行完成!!!'
