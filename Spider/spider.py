import requests
import re
import urllib
import os
import random


class spider(object):
    def __init__(self,url,localPath = './images'):
        self.url = url
        self.localPath = localPath
        self.imgTagRule = '<img[^>]+>'
        self.imgUrlRule = '"https://[^"]+"'

    # 创建目录
    def mkdir(self):
        isExists=os.path.exists(self.localPath)
        # 如果不存在则创建目录
        if not isExists:
            os.makedirs(self.localPath)
            print('目录已创建')
            return True
        # 如果目录存在则不创建，并提示目录已存在
        else:
            print('目录已存在')
            return False

    #获取网页内容
    def getPage(self):
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
        return requests.get(self.url,headers = headers).text

    #获取页面中所有的img标签
    def getImgTag(self):
        page = self.getPage()
        pattern = re.compile(self.imgTagRule,re.S)
        items = re.findall(pattern,page)
        return items

    #获取img标签中的src中的图片链接
    def getImgUrl(self):
        imgTag = self.getImgTag()
        for item in imgTag:
            pattern = re.compile(self.imgUrlRule,re.S)
            imgUrlList = re.findall(pattern,item)
            # print(imgUrlList)
            if(len(imgUrlList)!=0):
                yield imgUrlList[0][1:-1]

    #下载图片
    def downloadImg(self):
        self.mkdir()
        print(self.localPath)
        for imgUrl in self.getImgUrl():
            urllib.request.urlretrieve(imgUrl,filename=self.localPath+'/'+self.randomStr()+imgUrl[-4::])
            print('downloads:'+imgUrl)
        return True

    #生成随机字符串
    def randomStr(self,randomlength = 32):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        for i in range(randomlength):
            str+=chars[random.randint(0, length)]
        return str




spiderDemo = spider('https://movie.douban.com','../demo/images')
spiderDemo.downloadImg()
