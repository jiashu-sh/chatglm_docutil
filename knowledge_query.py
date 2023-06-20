# 用户提问匹配知识库

import torch
# from document_preprocess import get_vector 
from pymilvus_orm import *
from pymilvus_orm.schema import *
from pymilvus_orm.types import DataType
from transformers import AutoTokenizer, AutoModel

connections.connect(alias="default",host='10.19.1.251',port='19530')# 定义集合名称和维度
collection_name = "document"
dimension = 768

collection = Collection(name=collection_name, data=None)
# 将collection加载到内存
collection.load()

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"# 定义查询函数

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
model = AutoModel.from_pretrained("bert-base-chinese")

# 获取文本的向量
def get_vector(text):
    input_ids = tokenizer(text, padding=True, truncation=True, return_tensors="pt")["input_ids"]
    with torch.no_grad():
        output = model(input_ids)[0][:, 0, :].numpy()
    return output.tolist()[0]

def search_similar_text(input_text):
    # 将输入文本转换为向量
    input_vector = get_vector(input_text)
    # print(input_vector)
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}} #{"metric_type": "IP", "params": {"nprobe": 10}, "offset": 0}
    # 查询前三个最匹配的向量ID
    similarity = collection.search(
        data=[input_vector],
        anns_field="vector",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=3,
        expr=None,
        consistency_level="Strong"
        )
    ids = similarity[0].ids
    print(similarity[0])
    print(ids)
    # # 向量搜索
    # result = collection.search(data=np.random.random([5, 8]).tolist(),
    #                            anns_field=field_name, param=search_params, limit=10,
    #                            partition_names=[partition_name] if partition_name else None)
    # print(result[0].ids)
    # print(result[0].distances)
    
    res= []
    # 通过ID查询出对应的知识库文档
    res = collection.query(
        expr=f"id in {ids}",
        # limit=3, #offset=0,limit=3,
        output_fields=["id", "document_id"] #, # output_fields=["id", "document_id", "title"]
        # consistency_level="Strong"
        )
    print(res)
    return res

if __name__ == "__main__":
    question = input('Please enter your question: ')
    search_similar_text(question)