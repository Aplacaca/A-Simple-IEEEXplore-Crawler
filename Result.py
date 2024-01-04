import requests
import json
import pandas as pd
import urllib3
import re
import pdb
from utils import get_title,get_abstract,get_published,get_date,get_kwd

class Result(object):
    def __init__(self,config_dir=r'./search.json'):
        self.search = None
        self.totalPages = 0
        self.totalRecords = 0
        self.Data = pd.DataFrame()
        self.header = {
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '147',
            'Content-Type': 'application/json',
            'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                        'Safari/537.36 Edg/108.0.1462.46',
        }
        self.url = 'https://ieeexplore.ieee.org/rest/search'
        self.from_json(open_dir=config_dir)
        self.Data["article_id"] = self.get_article_list()
        self.get_article_info()


    def from_json(self, open_dir=r'./search.json'):
        with open(open_dir, 'r') as f:
            data = json.load(f)
        self.search = data

    def get_page(self, pagenum=1):
        search = self.search
        search["pageNumber"] = str(pagenum)
        res = requests.post(url=self.url, data=json.dumps(search), headers=self.header, verify=False)
        page_dict = res.json()
        # pdb.set_trace()
        return page_dict
    
    def get_article_list(self,):
        firstpage = self.get_page(pagenum=1)
        self.totalPages = int(firstpage["totalPages"])
        self.totalRecords = int(firstpage["totalRecords"])
        id_list = []  
        for i in range(1, self.totalPages + 1):
            page_dict = self.get_page(i)
            for an_item in page_dict["records"]:
                id_list.append(an_item["articleNumber"])
        return id_list

    def get_article_info(self,):
        title_list = []
        date_list = []
        keywords_list = []
        published_title_list = []
        for art in self.Data["article_id"].tolist():
            #
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                            'Safari/537.36 Edg/108.0.1462.46 '
            }
            url = 'https://ieeexplore.ieee.org/document/' + str(art)
            params = {}
            res = requests.get(url=url, params=params, headers=headers)
            print(res.status_code)
            page_text = res.text
            #
            title_list.append(get_title(page_text))
            date_list.append(get_date(page_text))
            keywords_list.append(get_kwd(page_text))
            published_title_list.append(get_published(page_text))
            
        self.Data["title"] = title_list
        self.Data["date"] = date_list
        self.Data["keywords"] = keywords_list
        self.Data["published_title"] = published_title_list

