import  re
import os
from bs4 import BeautifulSoup as bs4

def removeTags(html):
    bs = bs4(html,'lxml')
    # 格式化html代码
    html = bs.prettify()
    # 去掉标签 tags
    dr = re.compile(r'<[^>]+>',re.S)
    text = dr.sub('',html)
    # 去掉多余的空行
    text=re.sub('\s+', '\n', text)
    # dc = re.compile(r'\s+', re.S)
    # text = dc.sub('\n', text)
    return text

def saveToText(title,content):
    curdir = os.getcwd()
    folderName = '新闻正文'
    path = curdir+os.path.sep+folderName
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+os.path.sep+title+'.txt','wb') as f:
        f.write(content.encode('utf-8'))
        f.close()
    print('save'+title+'成功！')
    return path+os.path.sep+title+'.txt'