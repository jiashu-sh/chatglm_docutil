#_*_coding:utf-8_*_
import numpy as np
import os
import re
import jieba
import torch
import pandas as pd
import uuid

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
model = AutoModel.from_pretrained("bert-base-chinese")

class TxtVector() :
    
    def SaveT2vLog(self,log_filename,log_content):
        docs_folder = "./logs/"
        f = open(docs_folder + log_filename,"w",encoding="utf-8")
        f.write(log_content)
        f.close()
    
    def Content2Vec(self,sTitle,sContent,bSaveLog=False,logNameIndex=0):
        out_vec = None

        f_name = str(uuid.uuid1())
        # 对文本进行清洗处理
        content = re.sub(r"\s+", " ", sContent)
        title = sTitle
        # 分词
        words = jieba.lcut(content)
        print("总字数:{},jieba 分词数:{}".format(len(content),len(words)))
        # 将分词后的文本重新拼接成字符串
        text = " ".join(words)
        if bSaveLog :
            self.SaveT2vLog("log_"+str(logNameIndex) + "_" + f_name+".txt",content)
        
        input_ids = tokenizer(text, padding=True, truncation=True, return_tensors="pt")["input_ids"]
        with torch.no_grad():
            output = model(input_ids)[0][:, 0, :].numpy()
        out_vec = output.tolist()[0]
        if bSaveLog :
            self.SaveT2vLog("vec_"+f_name+".txt",str(out_vec))
        
        return out_vec
    
