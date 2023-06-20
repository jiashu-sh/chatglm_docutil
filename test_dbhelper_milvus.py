from txt2vector import TxtVector
from dbhelper_milvus import MilvusConnection

from txt2vector import TxtVector

if __name__ == "__main__" :
    sTitle="""
    Milvus 开源向量数据库
    """
    
    sContent = """
上图是 Milvus 2.0 的一个整体架构图，从最左边 SDK 作为入口，通过 load balancer 把请求发到 proxy 这一层。接着 proxy 会和最上面的 coordinator service（包括 root coord 、 root query、data 和 index）通过和他们进行交互，然后把 DDL 和 DML 写到我们的 message storage 里。
在下方的 Worker nodes：包括 query node、data node 和 index node， 会从 message storage 去消费这些请求数据。query node 负责查询，data node 负责写入和持久化，index node 负责建索引和加速查询。
最下面这一层是数据存储层 （object storage），使用的对象存储主要是 MinIO、S3 和 Azure Blob，用来储存 log、delta 和 index file。 
    """
    
    
    t2v = TxtVector()
    out_vec = t2v.Content2Vec(sTitle,sContent,bSaveLog=True)
    
    
    
    iDocumentId = 10613001
    milvusConn=MilvusConnection()
    # milvusConn.DropCollection()
    # iReturn = milvusConn.CreateCollection()
    # # print("CreateCollection:{}".format(iReturn))
    bInsert = milvusConn.InsertContentVector(iDocumentId,vector=out_vec,bInsertMilvus = True)
    milvusConn.SearchContentVector(vector=out_vec)
    