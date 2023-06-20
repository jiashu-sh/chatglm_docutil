#_*_coding:utf-8_*_
import requests
import json
import sys
import uuid

from langchain import PromptTemplate 
from dbhelper_pg import DbConnection

if __name__ == "__main__" :
    
    # 生成一个文档uuid （每个文档一个id）
    content_id = str(uuid.uuid1()) 
    
    dbconn = DbConnection()
    cnt_id = dbconn.InsertContentDocId(cnt_id=content_id)
    iDocId = dbconn.GetContentDocId(cnt_id) 
    print("test ok : {}".format(iDocId))
    
