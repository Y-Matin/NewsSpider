# NewsSpider
使用PYQT5 和 scrapy框架 结合readability正文提取算法，再用pyinstaller打包. 开发一个通用的爬虫系统

打包命令： pyintaller -D main.py -i spider.ico
生成的程序暂不支持移动，需要在scrapy环境中运行，与scrapy源文件存在关联，
因为日志获取是通过subprocess模块实现的。 通过命令行启动的scrapy框架，所以依赖scrappy环境

软件运行界面请看 ppt
