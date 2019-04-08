# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import configparser

import pymongo

from main import settingsScreen


class NewsspiderPipeline(object):

    @classmethod
    def from_crawler(cls,crawler):
        config = configparser.ConfigParser()
        configFile = settingsScreen.configFile
        config.read(configFile, encoding="utf-8-sig")
        return cls(
            linkMongo = config.getboolean(settingsScreen.configForDB, settingsScreen.linkDB),
            dbtype = config.get(settingsScreen.configForDB, settingsScreen.database),
            host=config.get(settingsScreen.configForDB, settingsScreen.host),
            dbName=config.get(settingsScreen.configForDB, settingsScreen.databaseName),
            userN=config.get(settingsScreen.configForDB, settingsScreen.user),
            passW = config.get(settingsScreen.configForDB, settingsScreen.passwd)
        )
    def __init__(self, linkMongo, dbtype,host,dbName,userN,passW):
        self.linkMongo = linkMongo
        self.dbtype = dbtype
        self.host = host
        self.dbName = dbName
        self.userN = userN
        self.passW = passW

        # self.mongo_url = mongo_url
        # self.mongo_db = mongo_db

    def open_spider(self,spider):
        # self.client = pymongo.MongoClient(self.mongo_url)
        # self.client = pymongo.MongoClient('mongodb://root:123456@localhost:27017/')

        # self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        # self.db = self.client['NEWS']

        if self.linkMongo:
            if 'MongoDB'.__eq__(self.dbtype):
                mongo_url = 'mongodb://'
                if  len(self.userN)!=0:
                    if  len(self.passW)!=0:
                        mongo_url = "%s%s:%s@"%(mongo_url,self.userN,self.passW)
                    else:
                        print('用户名不为空，密码为空！')
                elif len(self.passW)!=0:
                    print('用户名为空，密码不为空！')
                mongo_url = "%s%s/"%(mongo_url,self.host)
                self.client = pymongo.MongoClient(mongo_url)
                self.db = self.client[self.dbName]
            else:
                self.client = None
                self.db = None
        else:
            self.client = None
            self.db = None

    def process_item(self, item,spider):
        if  self.client:
            name = item.__class__.__name__
            self.db[name].insert(dict(item))  #
            return item

    def close_spider(self,spider):
        if  self.client:
            self.client.close()