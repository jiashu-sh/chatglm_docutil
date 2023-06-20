# ref ： https://blog.csdn.net/a914541185/article/details/130150101
# 文档预处理
# 1.连接 milvus 向量库
# 2.创建对应的connection
# 3.遍历读取文档
# 4.文档预处理
# 5.文档内容转向量
# 6.存入向量库
import numpy as np
import os
import re
import jieba
import torch
import pandas as pd
# from pymilvus import utility
# from pymilvus import connections, CollectionSchema, FieldSchema, Collection, DataType
# from pymilvus import (
#     connections,
#     FieldSchema, CollectionSchema, DataType,
#     Collection,
#     utility
# )
# from pymilvus_orm import connections, FieldSchema, CollectionSchema, DataType, Collection,utility , schema,types
from pymilvus_orm import *
from pymilvus_orm.schema import *
from pymilvus_orm.types import DataType

from transformers import AutoTokenizer, AutoModel

connections.connect(alias="default",host='10.19.1.251',port='19530')# 定义集合名称和维度
collection_name = "document"
dimension = 768

docs_folder = "./knowledge/"
docs_folder2 = "./logs/"
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
model = AutoModel.from_pretrained("bert-base-chinese")

def save_log(log_filename,log_content):
    f = open(docs_folder2+log_filename,"w")
    f.write(log_content)
    f.close()

# 获取文本的向量
def get_vector(text):
    input_ids = tokenizer(text, padding=True, truncation=True, return_tensors="pt")["input_ids"]
    with torch.no_grad():
        output = model(input_ids)[0][:, 0, :].numpy()
    return output.tolist()[0]

def create_collection():
    # 定义集合字段
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True, description="primary id"), # 主键
        FieldSchema(name="document_id", dtype=DataType.INT64),
        # FieldSchema(name="title", dtype=DataType.UNKNOWN, max_length=550),
        # FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=5000),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        ]
    # 定义集合模式
    schema = CollectionSchema(fields=fields, description="collection schema")
    
    # 创建集合
    if not utility.has_collection(collection_name):
        # 如果你想继续添加新的文档可以直接 return。但你想要重新创建collection，就可以执行下面的代码
        # return
        # return # 因为已经创建过 collection ，所以直接 return # 这里修改下：条件里加一个not，即没有这个collection时创建，否则就赋值即可
        # utility.drop_collection(collection_name)
        collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2)
        # 创建索引
        default_index = {"metric_type": "L2","index_type": "IVF_FLAT", "params": {"nlist": 2048}} #, "metric_type": "IP"
        collection.create_index(field_name="vector", index_params=default_index)
        print(f"Collection {collection_name} created successfully")
    else:
        collection = Collection(name=collection_name, data=None)
        print(f"\nGet collection name, schema, description and partitions...")
        print("collection name:{} , schema:{} , description:{} , partitions:{} ".format(collection.name,collection.schema,collection.description,collection.partitions))
        # 已经有了，不需要再创建索引了
        # collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2)
        # # 创建索引
        # default_index = {"index_type": "IVF_FLAT", "params": {"nlist": 2048}, "metric_type": "IP"}
        # collection.create_index(field_name="vector", index_params=default_index)
        # print(f"Collection {collection_name} created successfully")
        
    
def init_knowledge():
    bInsertMilvus = False
    collection = Collection(collection_name)
    # 遍历指定目录下的所有文件，并导入到 Milvus 集合中
    docs = []
    doc_id = 0
    for root, dirs, files in os.walk(docs_folder2): #docs_folder2 是logs文件夹
        for file in files:
            # 只处理以 .txt 结尾的文本文件
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                doc_id +=1
                # 对文本进行清洗处理
                content = re.sub(r"\s+", " ", content)
                title = os.path.splitext(file)[0]
                # 分词
                words = jieba.lcut(content)
                print("总字数:{},jieba 分词数:{}".format(len(content),len(words)))
                # 将分词后的文本重新拼接成字符串
                content = " ".join(words)
                save_log("log_"+title+".txt",content)
                
                # 获取文本向量
                vector = get_vector(title + content)
                print(title)
                print(len(vector))
                save_log("vet_"+title+".txt",str(vector))
                
                """
                # print(type(vector[1]))
                # print([doc_id,vector])
                # docs.append({"title": title, "content": content, "vector": vector})
                # collection.insert([[doc_id],vector]) # [title,content,vector]
                """
                """ 插入Milvus数据库 """
                if bInsertMilvus:
                    collection.insert([
                        [doc_id], # cat_id
                        # [title],
                        [vector]  # 向量 np.random.random([1, 768]).tolist()
                    ]) # [title,content,vector]
                
    # return       
    # 将文本内容和向量通过 DataFrame 一起导入集合中
    print(f"\nInsert data...")
    # df = pd.DataFrame(docs)
    # collection.insert(df)
    # print(docs) #到这里正常
    ''''''
    if bInsertMilvus:
        partition_name = "_default"
        partition = Partition(collection,partition_name)
        print(collection.num_entities)
    
    # partition.insert
    
    # mr = collection.Insert([
    #     docs["title"],
    #     docs["content"],
    #     docs["vector"]
    # ]
    # )
    ''''''
    
    # mr = collection.insert([
    #     # 只能是list
    #     np.random.random([10000, 8]).tolist(),  # 向量
    #     np.random.randint(0, 10, [10000]).tolist()  # cat_id
    # ], partition_name=partition_name)
    
    # 由于主键field_id设置自增，所以无需插入
    # df = pd.DataFrame(docs)
    # mr = collection.insert(docs)
    # print(mr.primary_keys)

    # 插入的数据存储在内存，需要传输到磁盘
    # utility.get_connection().flush([collection.name])
    
    
    print("Documents inserted successfully")
    
if __name__ == "__main__":
    # create_collection()
    
    init_knowledge()