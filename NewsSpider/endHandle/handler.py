import configparser
import  re
import os
from bs4 import BeautifulSoup as bs4

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

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

    # 解决windows 下 文件名不合法问题
    # 去掉\/|*字符，将 <>:?"替换为中文字符
    titleFinally = re.sub('[\\\/|*]', '', title)
    table = {ord(f): ord(t) for f, t in zip(
        u':?<>',
        u'：？《》')}
    titleFinally = titleFinally.translate(table)
    with open(path+os.path.sep+titleFinally+'.txt','wb') as f:
        f.write(content.encode('utf-8'))
        f.close()
    print('\nsave<'+titleFinally+'>成功！')
    return path+os.path.sep+titleFinally+'.txt'

def parseLocalFile(filepath):
    file = open(filepath,'r',encoding='utf-8')
    text = file.read()
    doc = Document(text)
    title = doc.title()
    summary = doc.summary()
    text = removeTags(summary)
    saveToText(title,text)

def sendEmail(text):
    my_sender = '724797522@qq.com'  # 发件人邮箱账号
    my_pass = 'fvrqcojpynkpbfbe'  # 发件人邮箱密码
    my_user = '724797522@qq.com'  # 收件人邮箱账号，我这边发送给自己
    ret = True
    try:
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["martin", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["martin", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "爬虫系统用户反馈"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.qq.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

def not_empty(s):
    return s and s.strip()

def getHeader():
    header= {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate, br',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'keep-alive'
    }
    return header
