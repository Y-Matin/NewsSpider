import configparser
import  re
import os
from bs4 import BeautifulSoup as bs4

from NewsSpider.readability.readability import Document



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
    from main import settingsScreen
    config = configparser.ConfigParser()
    config.read(settingsScreen.configFile, encoding="utf-8-sig")

    folderName = config.get(settingsScreen.file, settingsScreen.fileP)
    path = ''
    if not os.path.isabs(folderName):
        # 代表 该目录为初始目录，在该项目下
        curdir = os.getcwd()
        path = curdir + os.path.sep + folderName
    else:
        # 代表该目录已被修改过。
        path = folderName
    # folderName = '新闻正文'

    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+os.path.sep+title+'.txt','wb') as f:
        f.write(content.encode('utf-8'))
        f.close()
    print('\nsave'+title+'成功！')
    return path+os.path.sep+title+'.txt'

def parseLocalFile(filepath):
    file = open(filepath,'r',encoding='utf-8')
    text = file.read()
    doc = Document(text)
    title = doc.title()
    summary = doc.summary()
    text = removeTags(summary)
    saveToText(title,text)
