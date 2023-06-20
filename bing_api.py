import json
import os 
from pprint import pprint
import requests
import uuid
import time
# 配置文件的包
import configparser

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''

class BingApi():
    
    # fc*****************da7
    def __init__(self,
                 subscription_key="",
                 endpoint="https://api.bing.microsoft.com/v7.0/search",
                 mkt="global",
                 search_count=7,
                 search_offset=0) :
        # 读取ini配置文件
        cf=configparser.ConfigParser()   #创建对象
        cf.read('./config.ini',encoding='UTF-8') 
        # lstCfg = cf.items("TranslatorConf")
        config_subscription_key = cf.get('BingApiConf','key')
        if len(config_subscription_key.strip()) > 0 :
            subscription_key = config_subscription_key
        config_mkt = cf.get('BingApiConf','mkt')
        if len(config_mkt.strip()) > 0 :
            mkt = config_mkt
        config_endpoint = cf.get('BingApiConf','endpoint')
        if len(config_endpoint.strip()) > 0 :
            endpoint = config_endpoint
        # Add your Bing Search V7 subscription key and endpoint to your environment variables.
        # subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
        # subscription_key ="fc*****************da7"
        self.subscription_key = subscription_key
        # endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search" 
        # endpoint = "https://api.bing.microsoft.com/v7.0/search" #  "https://api.bing.microsoft.com" + "/v7.0/search" #示例代码中多了一个 /bing/,坑爹
        self.endpoint = endpoint
        # Construct a request
        # mkt = 'global' #'zh_CN'
        self.mkt = mkt
        self.search_count = search_count
        self.search_offset = search_offset
        # 调用方式：
        # from bing_api import BingApi
        # bing = BingApi()
        # contacts = bing.Search("LLM大模型")
        
    
    def Version(self):
        sVersion = "1.0 20230530"
        sReturn = "version:{0} , host:{1}".format(sVersion,self.host)
        return sReturn

    def Search(self,search_text="本机ip",s_count=0):
        # api文档：
        # https://learn.microsoft.com/zh-cn/rest/api/cognitiveservices-bingsearch/bing-web-api-v7-reference
        # Query term(s) to search for. 
        # query = "中文语音识别、大语言模型、智能信息查询系统、中文文本语音输入、识别、查询"
        if s_count <= 0:
            s_count = self.search_count
            
        query = search_text
        # query = "bing search api 200 错误"

        params = { 'q': query, 'mkt': self.mkt, 'count': s_count, 'offset': self.search_offset}
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }

        # params = {
        #     'mkt':'en-us',
        #     'mode':'spell',
        #     'text' : search_term
        #     }

        # Call the API
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()

            # print("\nHeaders:\n")
            # print(response.headers)
            
            data = response.json()
            
            # print(type(data["webPages"])) 
            # print(data["webPages"])
            listVals = data["webPages"]["value"]
            # print(type(listVals))
            
            contacts=[]
            for dictResult in listVals:
                # print(dictResult["url"])
                # print(dictResult["name"])
                # print(dictResult["snippet"])
                doc_id = str(uuid.uuid1())
                time.sleep(0.001)
                contacts.append((dictResult["name"], dictResult["snippet"], dictResult["url"],doc_id))
                # print(type(dictResult))
            
            # print(contacts)
            return contacts
            
            # print(data["webPages"]["value"])
            
            # for item in dictVals.items():
            #     key = item[0]
            #     value = item[1]
            #     print(key)
            #     print(value)

            # print("\nJSON Response:\n")
            # print(response.json())
        except Exception as ex:
            raise ex

