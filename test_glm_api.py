import time
import uuid

from glm_api import GlmApi

# 获取GLM对话结果
def LlmConversation(sContent="你好",his=[],cnt_id="", sToken="",iTemplateType=0) :
    """_summary_
        获取GLM对话结果
        Args:
            sContent (str, optional): _description_. Defaults to "你好".
            his (list, optional): _description_. Defaults to [].
            cnt_id (str, optional): _description_. Defaults to "".
            sToken (str, optional): _description_. Defaults to "".
            iTemplateType (int, optional): _description_. Defaults to 0.
        """
    sTxt = ""
    # 使用Glm获取对话内容------------------------------
    glmapi = GlmApi() #使用GlmApi
    sTxt = glmapi.LlmConversation(sContent=sContent,his=his,cnt_id=cnt_id, sToken=sToken,iTemplateType=iTemplateType) #,iTemplateType=1 详细描述内容
    return sTxt

if __name__ == "__main__" :
    
    sTxt = """
     随着近年来人工智能的快速发展，AI逐渐融入到各行业，产生新的行业应用场景。除了金融、城市管理、医疗等行业已经快速智慧化转型。而教育作为立国之本，重中之重，在2000年初，人工智能就被逐渐赋能到教育产业中。

在国内，AI+教育赛道备受资本关注。 2013年-2019年，AI+教育领域共发生274笔投融资事件，总融资额达145亿。从融资增速上来看，融资事件数复合增速达34%，融资总额增速达57%，资本一度狂热，其中K12与教育信息化领域的融资规模领跑其他细分赛道，期间各自总共融资78亿与20亿，分别占整体融资额的53.5%和13.6%。
    """
    cnt_id = str(uuid.uuid1())
    token_code = "test-" + cnt_id
    sGlmReply = LlmConversation(sTxt,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=4) #,iTemplateType=3 提取关键字
    
    print(sGlmReply)
    
    exit(0)
    