import time

from scipy import spatial

from txt2vector import TxtVector
from txt2vector import TxtVector

class VectorUtils() :
    
    def CosineSimilarity(self,vector1,vector2):
        """计算并返回2个向量的余弦相似度（越接近1越相似）
        Args:
            vector1 (_type_): 向量1
            vector2 (_type_): 向量2

        Returns:
            _type_: 2向量余弦相似度值
        """
        SimilarilyValue = 0
        start_time = time.time()
        SimilarilyValue = 1-spatial.distance.cosine(vector1,vector2)
        
        run_time = time.time()-start_time
        # print("run time:{}".format(run_time))
        return SimilarilyValue