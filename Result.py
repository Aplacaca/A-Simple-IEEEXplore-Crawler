import requests
import json
import pandas as pd
import pdb

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
        return page_dict
    
    def get_article_info(self,):
        firstpage = self.get_page(pagenum=1)
        self.totalPages = int(firstpage["totalPages"])
        self.totalRecords = int(firstpage["totalRecords"])
        id_list = []  
        title_list = []
        date_list = []
        published_title_list = []
        for i in range(1, self.totalPages + 1):
            page_dict = self.get_page(i)
            for an_item in page_dict["records"]:
                id_list.append(an_item["articleNumber"])
                title_list.append(an_item["articleTitle"])
                date_list.append(an_item["publicationDate"])
                published_title_list.append(an_item["publicationTitle"])
        self.Data["article_id"] = id_list
        self.Data["title"] = title_list
        self.Data["date"] = date_list
        self.Data["published_title"] = published_title_list
        return id_list,title_list,date_list,published_title_list


