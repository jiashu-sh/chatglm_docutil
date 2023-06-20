#_*_coding:utf-8_*_
import sys
import time
import datetime
import uuid

from bing_api import BingApi
from link_content import LinkDetail
from dbhelper_pg import DbConnection
from glm_api import GlmApi

from txt2vector import TxtVector
from vector_util import VectorUtils
# from dbhelper_milvus import MilvusConnection # Milvus操作不稳定，暂时不用


class Utils():
    
    # 保存日志文件
    def SaveLog(self,log_content,log_filename="log",file_suffix=".txt",filename_config="%Y%m%d-%H%M"):
        """保存日志文件
        Args:
            log_content (_type_): 日志记录详细内容
            log_filename (str, optional): 文件名. Defaults to "log".
            file_suffix (str, optional): 文件后缀. Defaults to ".txt".
            filename_config (str, optional): 默认的文件名日期格式. Defaults to "%Y%m%d-%H%M". %Y%m%d-%H%M%S
        """
        bReturn = False
        try:
            docs_folder = "./logs/"
            file_prefix = "main."
            full_filename = file_prefix + log_filename
            if len(filename_config.strip()) > 0 :
                full_filename += str(time.strftime(filename_config))
            full_filename += file_suffix
            f = open(docs_folder+full_filename,"w",encoding="utf-8") # 防止win默认gbk编码写入文件报错
            f.write(log_content)
            f.close()
        except Exception as e:
            print("Write log failed:", e)
        return bReturn
    
    # 获取分割大段文本List,按段落分
    def SplitParagraphs(self,sContent,iMaxContentLength = 800) :
        """
        获取分割大段文本List,按段落分。默认小于800字为一个单位
        若iMaxContentLength=0,表示按照每个自然段一个list项
        """
        splited_content = []
        if iMaxContentLength > 0: # 指定的解析段落长度大于0
            text_link_content = sContent
            if len(text_link_content) <= iMaxContentLength :
                splited_content.append(text_link_content)
            else :
                sTempSplit = text_link_content.split("\n")
                print(len(sTempSplit))
                if (len(sTempSplit) > 1):
                    sTemp = ""
                    for i in range(len(sTempSplit)):
                        if (len(sTemp) + len(sTempSplit[i])) <=iMaxContentLength :
                            sTemp += "\n" + sTempSplit[i]
                        else :
                            splited_content.append(sTemp.strip())
                            sTemp = sTempSplit[i]
                            
                    if (len(sTemp) > 0):
                        splited_content.append(sTemp.strip())
        else :# 指定的解析段落长度 <= 0 ,表示只需要按照自然段拆分即可
            sTempSplit = sContent.split("\n")
            for i in range(len(sTempSplit)):
                splited_content.append(sTempSplit[i])
                
        return splited_content
    
    # 分割获取搜索关键字
    def GetKeywords(self,sContent):
        """分割获取搜索关键字
        Args:
            sContent (_type_): _description_

        Returns:
            _type_: _description_
        """
        keywords = []
        sTxt = sContent
        
        split_chars = ["、","：",":","，",","," "] #顿号，冒号，逗号 空格
        rep_words = ["关键词：","关键词:","关键词","keywords"]
        for index in range(len(rep_words)):
            sTxt = sTxt.replace(rep_words[index],"")
        #先用英文逗号分隔，不行再用中文逗号和顿号分割
        for index in range(len(split_chars)):
            if (sTxt.find(split_chars[index])) > 0 :
                keywords = sTxt.split(split_chars[index])
                if len(keywords) > 0 :
                    break
        return keywords
    
    # 去除正文内容前的标号等无意义字符
    def TrimContent(self,sContent):
        """去除正文内容前的标号，并去除无意义的段落；同时判断若字符数小于5，也返回空
        Args:
            sContent (_type_): 正文内容

        Returns:
            _type_: 去掉标号的内容
        """
        iMinParagraphLength = 5
        iMinParagraphLength2 = 7
        
        sTxt = sContent.strip().strip('\r').strip('\n').strip('\t').strip().strip('-').strip()
        
        # 找到段最后是冒号，并且长度小于7字符的字符串，这类字符串没有扩展的意义
        list_str = [":","："]
        if len(sTxt) < iMinParagraphLength2 :
            for index in range(len(list_str)):
                if sTxt.endswith(list_str[index]):
                    print("del: {}".format(sTxt))
                    return ""
                
        # 去掉前面的序号 + “.”
        label_numbers = ["0","1","2","3","4","5","6","7","8","9",".","、","：",":","，","一","二","三","四","五","六","七","八","九","十","*"]
        if (sTxt.find(',') < 3) or (sTxt.find('.') < 3) or (sTxt.find('，') < 3) or (sTxt.find('、') < 3) :
            for index in range(len(label_numbers)):
                sTxt = sTxt.strip(label_numbers[index])
        
        # 删除单行为 特殊文字的段落，例如： 概述： 提纲：这类
        sTxt = sContent.strip().strip(':').strip('：')
        meaningless_paragraphs = ["概述","提纲"]
        for index in range(len(meaningless_paragraphs)):
            sTxt = sTxt.strip(meaningless_paragraphs[index])
        
        # 删除过短的段落，没有扩展意义
        if len(sTxt) <= iMinParagraphLength:
            print("del: {}".format(sTxt))
            sTxt = ""

        return sTxt
    
    # 初始化查询返回项
    def InitSearchContents(self) :
        """初始化查询返回项

        Returns:
            _type_: [("", "", "","")]
        """
        contacts=[]
        contacts.append(("", "", "",""))
        return contacts
    
    # 搜索BingApi获取数据
    def SearchBingApi(self,sContent="",bIsSave=False) :
        """
        搜索BingApi获取数据
        """
        if len(sContent.strip()) == 0 :
            contacts_init=[]
            contacts_init.append(("", "", "",""))
            return contacts_init
        
        # sContent = "LLM大模型"
        bing = BingApi()
        contacts = bing.Search(search_text=sContent,s_count=5)
        if bIsSave:
            for i, search_result in enumerate(contacts):
                # print(search_result)
                cnt_id = search_result[3]
                cnt_text = ""
                cnt_title = search_result[0]
                cnt_summary = search_result[1]
                cnt_link = search_result[2]
                # 获取链接明细全文------------------------------------------
                hyperlink = LinkDetail()
                sContent = hyperlink.GetContent(cnt_link)
                cnt_text = sContent.strip().strip('\n').strip('\t')
                # 数据库操作：记录对话内容-------------------------------------------------------------
                dbconn = DbConnection()
                bInsert = dbconn.InsertLlmContent(cnt_id=cnt_id,cnt_text=cnt_text,cnt_title=cnt_title,cnt_summary=cnt_summary,cnt_link=cnt_link) #
                # -----------------------------------------------------------------------------------
        return contacts
    
    def InsertTextContent(self,cnt_id,cnt_text,cnt_title,cnt_summary="",cnt_link=""):
        bInsertResult = False
        if (len(cnt_id) == 0) or (len(cnt_text) == 0) :
            return bInsertResult
        # 数据库操作：记录对话内容-------------------------------------------------------------
        dbconn = DbConnection()
        bInsertResult = dbconn.InsertLlmContent(cnt_id=cnt_id,cnt_text=cnt_text,cnt_title=cnt_title,cnt_summary=cnt_summary,cnt_link=cnt_link) #
        return bInsertResult
    
    # 获取链接明细全文（爬网页正文）
    def GetLinkContent(self,slink="") :
        """
        获取链接明细全文
        """
        cnt_text = ""
        if len(slink.strip()) == 0:
            return cnt_text
        # 获取链接明细全文------------------------------------------
        hyperlink = LinkDetail()
        sContent = hyperlink.GetContent(slink)
        cnt_text = sContent.strip().strip('\r').strip('\n').strip('\t').strip()
        return cnt_text
    
    # 获取GLM对话结果
    def LlmConversation(self,sContent="你好",his=[],cnt_id="", sToken="",iTemplateType=0,bSaveDbLog=False) :
        """_summary_
        获取GLM对话结果
        Args:
            sContent (str, optional): 主体扩写内容. Defaults to "你好".
            his (list, optional): _description_. Defaults to [].
            cnt_id (str, optional): _description_. Defaults to "".
            sToken (str, optional): _description_. Defaults to "".
            iTemplateType (int, optional): _description_. Defaults to 0.
        """
        sTxt = ""
        # 使用Glm获取对话内容------------------------------
        glmapi = GlmApi() #使用GlmApi
        sTxt = glmapi.LlmConversation(sContent=sContent,his=his,cnt_id=cnt_id, sToken=sToken,iTemplateType=iTemplateType,bSaveDbLog=bSaveDbLog) #,iTemplateType=1 详细描述内容
        return sTxt
    
    # 获取GLM对话结果
    def LlmConversationV2(self,sAdjective,sContent,his=[],cnt_id="", sToken="",iTemplateType=0) :
        """_summary_
        获取GLM对话结果
        Args:
            sAdjective (str, optional): 建议参考内容. Defaults to "".
            sContent (str, optional): 主体扩写内容. Defaults to "".
            his (list, optional): _description_. Defaults to [].
            cnt_id (str, optional): _description_. Defaults to "".
            sToken (str, optional): _description_. Defaults to "".
            iTemplateType (int, optional): _description_. Defaults to 0.
        """
        sTxt = ""
        # 使用Glm获取对话内容------------------------------
        glmapi = GlmApi() #使用GlmApi
        sTxt = glmapi.LlmConversationV2(sAdjective=sAdjective,sContent=sContent,his=his,cnt_id=cnt_id, sToken=sToken,iTemplateType=iTemplateType) #,iTemplateType=1 详细描述内容
        return sTxt
        
    # 插入并获取文档id（int）
    def GetCreateContentDocId(self,content_id) :
        """创建一个新的文档ID（根据搜索的文章资料的正文uuid）
        Args:
            content_id (_type_): 文章资料的正文uuid

        Returns:
            _type_: int 文档id
        """
        document_id = 0
        dbconn = DbConnection()
        # 插入一个content_id 并获取新生成的文档id doc_id
        cnt_id = dbconn.InsertContentDocId(cnt_id=content_id)
        if len(cnt_id) > 0 :
            document_id = dbconn.GetContentDocId(cnt_id) 
        return document_id
    
    # 文本转向量
    def Txt2Vector(self,sTitle,sContent,bSaveLog=False,logNameIndex=0) :
        out_vec = None
        t2v = TxtVector()
        out_vec = t2v.Content2Vec(sTitle,sContent,bSaveLog,logNameIndex)
        return out_vec
    
    # 计算向量余弦相似度
    def VectorCosineSimilarity(self,vector1,vector2):
        vector_util = VectorUtils()
        return vector_util.CosineSimilarity(vector1,vector2)
    
    '''
    # Milvus操作不稳定，暂时不用
    def InitMilvus(self,):
        milvusConn=MilvusConnection()
        milvusConn.CreateCollection()
    
    def InsertMilvus(self,iDocumentId,vector,bInsertMilvus = False):
        milvusConn=MilvusConnection()
        bInsert = milvusConn.InsertContentVector(iDocumentId,vector,bInsertMilvus)
        return bInsert
    '''