#_*_coding:utf-8_*_
import numpy as np
import os
import re
import jieba
import torch
import pandas as pd
# r2.0.0 rc4
from pymilvus_orm import *
from pymilvus_orm.schema import *
from pymilvus_orm.types import DataType


# from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# model = AutoModel.from_pretrained("bert-base-chinese")

connections.connect(host='10.19.1.251',port='19530')# 定义集合名称和维度 alias="default",
collection_name = "document"
dimension = 768
# _partition_name = "default"

class MilvusConnection():
    # 可参考 ： https://www.jianshu.com/p/d7f0e11e7336
    # https://www.dandelioncloud.cn/article/details/1568237349421412353
    # https://zhuanlan.zhihu.com/p/617972545
    
    # def __init__(self,
    #              host='10.19.1.251',
    #              port='19530',
    #              alias="default",
    #              collection_name="document",
    #              dimension = 768) :
    #     self.host = host
    #     self.port = port
    #     self.alias = alias
    #     self.collection_name = "document"
    #     self.dimension = 76
    #     self.connections.connect(alias=alias,host=host,port=port)# 定义集合名称和维度
    #     # connections.connect(alias="default",host='10.19.1.251',port='19530')# 定义集合名称和维度
    #     self.collection_name = collection_name # "document"
    #     self.dimension = dimension # 768
        
    def CreateCollection(self):
        iReturnVal = 0
        # 定义集合字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True, description="primary id"), # 主键
            FieldSchema(name="document_id", dtype=DataType.INT64),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            ]
        # 定义集合模式
        schema = CollectionSchema(fields=fields, description="collection_schema")
        
        # 创建集合
        if not utility.has_collection(collection_name):
            # 如果你想继续添加新的文档可以直接 return。但你想要重新创建collection，就可以执行下面的代码
            # return # 因为已经创建过 collection ，所以直接 return # 这里修改下：条件里加一个not，即没有这个collection时创建，否则就赋值即可
            # utility.drop_collection(collection_name)
            collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2) #
            # 创建索引
            default_index = {"metric_type": "L2","index_type": "IVF_FLAT", "params": {"nlist": 2048}} #, "metric_type": "IP"
            collection.create_index(field_name="vector", index_params=default_index)
            print(f"Collection {collection_name} created successfully")
            iReturnVal = 1
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
        return iReturnVal
    
    def DropCollection(self): #collection: Collection
        collection = Collection(name=collection_name, data=None)
        # 删除collection
        collection.drop()
        # 删除索引
        # collection.drop_index()
        # # 删除分区
        # collection.drop_partition("partition_name")
        
    def SearchContentVector(self,vector):
        doc_ids = []
        try:
            collection = Collection(collection_name)
            print(len(vector))
            if len(vector)==dimension:
                # =========================================================================
                # 将collection加载到内存，必须先加载到内存，然后才能检索
                # partition_name = "default"
                collection.load()
                print("milvus load ok")
                search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
                # 向量搜索
                result = collection.search(data=[vector],
                                        anns_field="vector", param=search_params, limit=3
                                        ) #partition_names= None
                print("search fin.")
                searched_ids = []
                for res in result:
                    print(res.ids)  # 查询出来id后，根据id找到对应的text
                    
                    for index in range(len(res.ids)):
                        searched_ids.append(res.ids[index])
                    # print(res)
                    for hit in res:
                        print(hit.entity)
                        
                expr = f'id in {searched_ids}' #再次根据ids查询出document_id字段
                print(expr)
                q_result = collection.query(expr=expr, output_fields=["id", "document_id"])
                print(f"query before delete by expr=`{expr}` -> result: \n-{result[0]}\n-{result[1]}\n")
                for index in range(len(q_result)):
                    doc_ids.append(result[index])
                print(doc_ids)
                #===========================================================================
            else :
                print("Vector length error : {}".format(len(vector)))
        except Exception as e:
            print("Insert milvus failed:", e)
        
        return doc_ids
        
 
    def InsertContentVector(self,iDocumentId,vector,bInsertMilvus = False):
        bInsertResult = False
        if (iDocumentId<=0):
            return bInsertResult
        # try:
        #     self.CreateCollection()
        # except Exception as e:
        #     print("Create milvus failed:", e)
        
        try:
            collection = Collection(collection_name)
            # collection = Collection(name=collection_name, data=None)
            # print(collection.name)
            if bInsertMilvus:
                data=[
                    [iDocumentId], # document_id ,另：id字段自增
                    [vector]  # 向量 np.random.random([1, 768]).tolist()
                    ]
                mr = collection.insert(data)
                print(mr.primary_keys)
                #region 参考
                # =========================================================================
                # 仅参考：
                # partition_name = "_default" # "Default partition" #"_default"
                # partition = Partition(collection,partition_name)
                # partition.insert(data)
                # print("iDocumentId = {}".format(iDocumentId))
                # # print(collection.num_entities)
                # print("Documents inserted successfully")
                
                # get_connection().flush([collection.name]) # utility.get_connection().flush([collection.name]) 使用这个就等待状态
                
                # # 从内存中释放collection
                # if collection:
                #     collection.release()
                # # 断开与服务器的连接，释放资源
                # connections.disconnect("default")
                #===========================================================================
                #endregion
                bInsertResult = True
                
                '''
                # =========================================================================
                # 将collection加载到内存，必须先加载到内存，然后才能检索
                # partition_name = "default"
                doc_ids = []
                collection.load()
                print("load fin.")
                search_params = {"metric_type": "L2", "params": {"nprobe": 10}} # IP
                print(search_params)
                # 向量搜索
                result = collection.search(data=[vector],
                                        anns_field="vector", param=search_params, limit=2,
                                        partition_names= None)
                print("search fin.")
                searched_ids = []
                for res in result:
                    print(res.ids)  # 查询出来id后，根据id找到对应的text
                    
                    for index in range(len(res.ids)):
                        searched_ids.append(res.ids[index])
                    # print(res)
                    for hit in res:
                        print(hit.entity)
                        
                expr = f'id in {searched_ids}' #再次根据ids查询出document_id字段
                print(expr)
                q_result = collection.query(expr=expr, output_fields=["id", "document_id"])
                print(f"query before delete by expr=`{expr}` -> result: \n-{result[0]}\n-{result[1]}\n")
                # for index in range(len(q_result)):
                #     doc_ids.append(result[index])
                # print(doc_ids)
                #===========================================================================
                '''
                
        except Exception as e:
            print("Insert milvus failed:", e)
        
        return bInsertResult