import time

from scipy import spatial

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
    
    sContent3 = """
Milvus 是一款开源的、针对海量特征向量的相似性搜索引擎。自从 Milvus 开源以来，受到了业界朋友的广泛关注，还有一些朋友亲自体验了 Milvus 做向量检索。我们也收到了很多用户的反馈，其中相当一部分是在使用 Milvus 中踩到的坑。为了给更多的用户排雷，我们特地总结了 Milvus 使用过程中比较容易踩到的一些坑。
数据是测试的主体
从最左边 SDK 作为入口，通过 load balancer 把请求发到 proxy 这一层。接着 proxy 会和最上面的 coordinator service（包括 root coord 、 root query、data 和 index）通过和他们进行交互，然后把 DDL 和 DML 写到我们的 message storage 里。
在下方的 Worker nodes：包括 query node、data node 和 index node， 会从 message storage 去消费这些请求数据。
    """
    
    sContent3 = """
    只有当数据做过归一化，Metric_type 的 L2 和 IP 计算的向量相似度结果才会等价。
​ 细心的 Milvus 用户会发现，Milvus 的配置文件里面定义了两种计算向量相似度的方法，L2（欧氏距离）和 IP（点积）。当把数据导入 Milvus 之后，分别使用 L2 和 IP 的方法进行查询，两者查询出来的结果竟然不一致！
​ 这是操作的不对还是 Milvus 自身出了问题？都不是，是数据出了问题！可以通过数学推理证明，只有当数据做过归一化，L2 和 IP 计算的向量相似度结果才会等价，具体推理过程可以参考：数据归一化。所以，当数据没有做归一化，使用 L2 和 IP 计算的向量相似度结果不一致也就不足为奇了。推荐使用 Milvus 做向量检索时，提前对数据做归一化，这样你就可以自由地选择 L2 和 IP 这两种计算向量相似度的方法了。
    数据目录映射之前，应该提前计算需要的存储空间，保证磁盘空间充足。
​ Milvus 启动时要指定一个数据存储目录，即 db 目录。当你启动好 Milvus 的数据导入程序，出去喝完一杯咖啡，打算验收导入成果时，只见电脑屏幕上赫然显示着 no space left on device 一行小字。恍然意识到磁盘空间已经用尽，前面的工作功亏一篑。
为了避免踩进上面的坑里，建议每次在导入数据之前都提前计算一下需要占用的磁盘空间。以１亿条 512 维的单精度向量为例，如果对其建立 FLAT 或者 IVFLAT 索引，那么导入 Milvus 之后占用的存储空间大小为：
​ 4B x 512 x 100,000,000 = 200GB
如果采用 IVF_SQ8 索引，则导入 Milvus 占用的存储空间为 FLAT 或 IVFLAT 的四分之一，即 50GB。"""
    
    #query node 负责查询，data node 负责写入和持久化，index node 负责建索引和加速查询。
#最下面这一层是数据存储层 （object storage），使用的对象存储主要是 MinIO、S3 和 Azure Blob，用来储存 log、delta 和 index file。 
    
    sContent2 = """
    Milvus 是一款开源的、针对海量特征向量的相似性搜索引擎。自从 Milvus 开源以来，受到了业界朋友的广泛关注，还有一些朋友亲自体验了 Milvus 做向量检索。我们也收到了很多用户的反馈，其中相当一部分是在使用 Milvus 中踩到的坑。为了给更多的用户排雷，我们特地总结了 Milvus 使用过程中比较容易踩到的一些坑。
数据是测试的主体，数据处理得好，坑就踩得少"""
    
    start_time = time.time()
    
    t2v = TxtVector()
    out_vec = t2v.Content2Vec(sTitle,sContent,bSaveLog=True)
    print("length vec ：{}".format(len(out_vec)))
    out_vec2 = t2v.Content2Vec(sTitle,sContent2,bSaveLog=True)
    print("length vec 2 ：{}".format(len(out_vec2)))
    out_vec3 = t2v.Content2Vec(sTitle,sContent3,bSaveLog=True)
    print("length vec 3 ：{}".format(len(out_vec3)))
    
    run_time = time.time()-start_time
    print("run consuming time:{} sec".format(run_time))
    
    start_time = time.time()
    cos_sim = 1-spatial.distance.cosine(out_vec,out_vec2)
    print(time.time()-start_time)
    
    print("cosine:{}".format(cos_sim))
    
    cos_sim = 1-spatial.distance.cosine(out_vec2,out_vec3)
    
    print("cosine:{}".format(cos_sim))
    
    '''
    iDocumentId = 10613001
    milvusConn=MilvusConnection()
    # milvusConn.DropCollection()
    # iReturn = milvusConn.CreateCollection()
    # # print("CreateCollection:{}".format(iReturn))
    bInsert = milvusConn.InsertContentVector(iDocumentId,vector=out_vec,bInsertMilvus = True)
    milvusConn.SearchContentVector(vector=out_vec)
    '''
    