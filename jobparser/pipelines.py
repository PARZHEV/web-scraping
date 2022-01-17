# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacncies


    def process_item(self, item, spider):
        item['min'], item['max'], item['cur'] = self.process_salary(item['salary'])
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        if type(salary) is list:
            if len(salary) < 6:
                if salary[0] == 'от ':
                    min_zp = salary[1]
                    num = ""
                    for c in min_zp:
                        if c.isdigit():
                            num = num + c
                    min_zp = num
                    max_zp = ''
                    cur_zp = salary[3]
                else:
                    max_zp = salary[1]
                    num = ""
                    for c in max_zp:
                        if c.isdigit():
                            num = num + c
                    max_zp = num
                    min_zp = ''
                    cur_zp = salary[3]
            else:

                min_zp = salary[1]
                num = ""
                for c in min_zp:
                    if c.isdigit():
                        num = num + c
                min_zp = num

                max_zp = salary[3]
                num = ""
                for c in max_zp:
                    if c.isdigit():
                        num = num + c
                max_zp = num
                cur_zp = salary[5]

        else:
            if salary[-4:] == 'руб.':
                num = ''
                for c in salary:
                    if c.isdigit():
                        num = num + c
                min_zp = num
                cur_zp = salary[-4:]
                max_zp = ''
            else:
                min_zp = salary
                cur_zp = ''
                max_zp = ''

        return min_zp, max_zp, cur_zp