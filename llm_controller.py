#_*_coding:utf-8_*_
import sys
import time
import datetime
import uuid
# import numpy as np

from llm_util import Utils
utils = Utils()

class Controller():
    
    def Version(self):
        sVersion = "1.0 20230608"
        sReturn = "version:{0} , host:{1}".format(sVersion,self.host)
        return sReturn
    
    def LlmConversation(self,sTxt,iTemplateType=-1,bSaveDbLog=True) :
        sReturn = ""
        cnt_id = str(uuid.uuid1())
        sReturn = utils.LlmConversation(sTxt,his=[],cnt_id=cnt_id, sToken=cnt_id,iTemplateType=-1,bSaveDbLog=bSaveDbLog) #,iTemplateType=-1 无指令，直接对话
        sLog = sTxt
        sLog += "\n" + "-------------------------------------------------------------------"
        sLog += "\n" + sReturn
        utils.SaveLog(sLog,log_filename="m-conversation-text-log")
        return sReturn
    
    def ExtendWriting(self,lKeywords,cnt_id_seed,token_code,qHis,sTxtSummary):
        
        # ExtendWriting(lSummaryKeywords,cnt_id_seed,token_code)
        sTxt = ""
        sLog = "" # 日志文件
        
        sSplit = "------------------------------------------------------------------------------"
        
        # 主内容转换为向量
        mainVector = utils.Txt2Vector(sTitle=qHis,sContent=sTxtSummary,bSaveLog=True,logNameIndex=0) #主内容转换为向量
        
        # setp : search summary keywords -------------------------------------------------------
        sSetpDesc = "-- 101. search summary keywords......" #用搜索关键词执行搜索
        print(sSetpDesc)
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        sKeyword = ""
        for index in range(len(lKeywords)):
            sKeyword += lKeywords[index] + " "
        contacts = utils.SearchBingApi(sKeyword,bIsSave=True) #执行搜索，并保存搜索内容
        sLog += "search fin. results : {} ".format(len(contacts)) + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        if (len(contacts)<=0) : # 如果没有搜索到内容，暂时就这样退出
            utils.SaveLog(sLog,log_filename="s")
            sLog += "search api find no result." + "\r\n"
            return [sTxt, sLog]
        
        # setp : split search results, vector cosine compute ,get max cosine val -------------------------------------------------------
        sSetpDesc = "-- 102. split search results, vector cosine compute ,get max cosine val......" # 将搜索到的结果按字数和自然段分段，并对每一段和原始内容进行余弦相似度比较，找到最相似的段落（为下一步进行扩展做准备）
        print(sSetpDesc)
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        # 定义相似度最高的余弦值和文本段（temp）
        CosineVals = [] # 余弦相似度List
        LstParas = [] # 余弦相似度，段落 list
        # 搜索完成后，从contacts中获取文档id（doc_id），然后准备存入向量数据库
        for index in range(len(contacts)):
            cnt_title = contacts[index][0]
            cnt_uuid = contacts[index][3]
            cnt_summary = contacts[index][1].strip()
            cnt_link = contacts[index][2].strip()
            if len(cnt_link) > 0 :
                doc_id = utils.GetCreateContentDocId(cnt_uuid)
                sLinkContent = utils.GetLinkContent(cnt_link)
                splitParas = utils.SplitParagraphs(sLinkContent)
                for i in range(len(splitParas)):
                    sParagraph = splitParas[i]
                    logfile_id = str(i) + "." + cnt_uuid
                    print("cnt_title:{} , cnt_uuid:{} , doc_id:{}".format(cnt_title,logfile_id,doc_id))
                    paraVector = utils.Txt2Vector(sTitle=cnt_title,sContent=sParagraph,bSaveLog=False,logNameIndex=(i+1)) # 当前段落文本的向量,bSaveLog=False 不需要记录向量值日志
                    cosineVal = utils.VectorCosineSimilarity(mainVector,paraVector) # 余弦相似度计算
                    CosineVals.append([i,int(cosineVal*10000)]) # 余弦相似度List (乘10000然后转整数，便于排序) --- 余弦相似度，段落id的数组 组成List
                    LstParas.append(sParagraph) # 段落 list 
                    # print("cosine val {}: {}".format((i+1),cosineVal)) # 不用打印出cosine val
        #region 找出一个向量余弦最大值，不再使用
                    # if cosineVal > dMaxCosineVal :
                    #     dMaxCosineVal = cosineVal
                    #     sSimilarilyParagraph = sParagraph
        # 
        # print("max cosine val : {}".format(dMaxCosineVal))
        # print("最相似内容：------------------------\n{}".format(sSimilarilyParagraph))
        # print("-----------------------------------")
        # sLog += "最相似内容：------------------------\n{}".format(sSimilarilyParagraph) + "\r\n" #记录Log .....
        # sLog += sSplit + "\r\n"
        #endregion
        
        # print("排序前：\r\n{}\r\n".format(CosineVals)) # 不用打印
        sTopXSimilarilyParagraph = ""
        if len(LstParas) >= 3:
            lstValTopX = sorted(CosineVals,key=lambda x:(-1*x[1])) # 按照CosineVals第二列 cosineVal 值降序排序
            # print("排序后： \r\n{}\r\n".format(lstValTopX)) # 不用打印
            for j in range(len(lstValTopX)):
                if (j<3): #只要前3个
                    idx = lstValTopX[j][0]
                    print(idx)
                    sEachTopXParagraph = LstParas[idx] # 找到的Top x 相似内容
                    print(sEachTopXParagraph)
                    
                    # setp : generate summary --------------------------------------------------------------
                    sSetpDesc = "-- 103. generate summary （search get paragraph）......" #总结概括相似内容
                    print(sSetpDesc) 
                    sLog += sSetpDesc + "\r\n" # 记录Log .....
                    cnt_id = "103-" + cnt_id_seed
                    sTxtSummary = utils.LlmConversation(sEachTopXParagraph,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=2) #,iTemplateType=2 概括文章
                    aHis = sTxtSummary
                    sLog += sTxtSummary + "\r\n" #记录Log .....
                    sLog += sSplit + "\r\n"
                    print(sTxtSummary)
                    
                    sTopXSimilarilyParagraph += sTxtSummary + "\r\n" # LstParas[idx] 原来是直接将搜索内容添加进参考资料，但是文本太长（超过2048）,因此改为概括后加入参考资料
                    
            
        # setp : generate summary keywords -----------------------------------------------------
        sSetpDesc = "-- 104. extended writing by reference paragraph......" # 将最接近的段落进行扩展说明
        print(sSetpDesc)
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        cnt_id = "104-" + cnt_id_seed
        # sTxtExtended = utils.LlmConversationV2(sSimilarilyParagraph,sTxtSummary, his=[[qHis,aHis]],cnt_id=cnt_id, sToken=token_code,iTemplateType=1) #,iTemplateType=4 根据参考文档进行写作
        sTxtExtended = utils.LlmConversation(sTxtSummary +"\n" + sTopXSimilarilyParagraph, his=[[qHis,sTxtSummary]],cnt_id=cnt_id, sToken=token_code,iTemplateType=4) #,iTemplateType=4 根据参考文档进行写作
        sLog += "扩展内容：------------------------\n{}".format(sTxtExtended) + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        
        sTxt = sTxtExtended
        
        return [sTxt, sLog]
    
    def GenerateContent(self,sText,bInternetSearch=True) : #,bInternetSearch=True 默认进行搜索引擎搜索扩写
        """生成正文
        Args:
            sText (_type_): 标题
        """
        sContent = ""
        
        qHis=sText.strip().strip('\r').strip('\n').strip('\t').strip()
        aHis=""
        
        if len(qHis) == 0 :
            return "无输入内容,请检查输入后重试."
        
        token_code = "token-" + str(uuid.uuid1())
        cnt_id_seed = str(uuid.uuid1())
        
        sSplit = "------------------------------------------------------------------------------"
        sLog = ""
        # setp : generate outline --------------------------------------------------------------
        sSetpDesc = "-- 1. generate outline......" #写提纲
        print(sSetpDesc) 
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        cnt_id = "01-" + cnt_id_seed
        sTxt = utils.LlmConversation(qHis,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=0) #,iTemplateType=0 概述列提纲
        sLog += sTxt + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        # aHis = sTxt
        
        # setp : generate summary --------------------------------------------------------------
        sSetpDesc = "-- 2. generate summary......" #总结提纲
        print(sSetpDesc) 
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        cnt_id = "02-" + cnt_id_seed
        sTxtSummary = utils.LlmConversation(sTxt,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=2) #,iTemplateType=2 将提纲概括一下
        aHis = sTxtSummary
        sLog += sTxtSummary + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        print(sTxtSummary)
        
        # setp : generate summary keywords -----------------------------------------------------
        sSetpDesc = "-- 3. generate summary keywords......" #概括提纲搜索关键词
        print(sSetpDesc)
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        cnt_id = "03-" + cnt_id_seed
        sTxtSummaryKewords = utils.LlmConversation(sTxtSummary,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=3) #,iTemplateType=3 提取关键字
        sLog += sTxtSummaryKewords + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        print(sTxtSummaryKewords)
        lSummaryKeywords = utils.GetKeywords(sTxtSummaryKewords)
        print(lSummaryKeywords)
        
        # setp : insert summary content to db -----------------------------------------------------
        sSetpDesc = "-- 04. insert summary content to db......" # 插入db保存提纲正文 - save
        print(sSetpDesc)
        sLog += sSetpDesc + "\r\n" # 记录Log .....
        cnt_id = "04-" + cnt_id_seed
        bInsertTextContent = utils.InsertTextContent(cnt_id=cnt_id,cnt_text=sTxt,cnt_title=qHis,cnt_summary=sTxtSummary,cnt_link="")
        main_doc_id = utils.GetCreateContentDocId(cnt_id)
        sLog += "insert : {} , doc_id: {}".format(bInsertTextContent,main_doc_id) + "\r\n" #记录Log .....
        sLog += sSplit + "\r\n"
        # 到这里出问题了，Milvus不稳定，改为直接通过向量作计算
        # utils.InitMilvus()
        # utils.InsertMilvus(iDocumentId=main_doc_id,vector=mainVector,bInsertMilvus = True)
        
        '''
        # 对整篇的扩写
        extResult = self.ExtendWriting(lSummaryKeywords,cnt_id_seed,token_code,qHis,sTxtSummary)
        sLog += extResult[1]
        sTxt += sSplit + "\r\n"
        sTxt += extResult[0]
        
        print(sTxtSummaryKewords)
        lSummaryKeywords = utils.GetKeywords(sTxtSummaryKewords)
        print(lSummaryKeywords)
        '''
        
        # utils.SaveLog(sLog)
        # return sTxt #下面暂时不用执行，节约时间
        
        # setp : -- setp by step generate ------------------------------------------------------
        sSetpDesc = "-- 10. setp by step generate ......"
        print(sSetpDesc)
        paras = utils.SplitParagraphs(sTxt,0)
        for index in range(len(paras)) :
            print("--------------------------------------")
            # print(paras[index])
            sPara = paras[index].strip().strip('\r').strip('\n').strip('\t').strip().strip('-').strip()
            sExtendPara = sPara #准备扩写内容参考
            if len(sExtendPara.strip()) == 0: # 为空则跳出，继续下一个循环
                continue
            
            if bInternetSearch : # 搜索并扩写
                sKeyword = ""
                # 段落内容太少（6个字以内，不需要再进行扩展和分析，直接作为关键词）
                iMinParagraphLength2 = 7
                if len(sPara) < iMinParagraphLength2 :
                    sKeyword = sPara + " "
                    for index in range(len(lSummaryKeywords)):
                        sKeyword += lSummaryKeywords[index] + " "
                    print("搜索关键词（s）: {}".format(sKeyword))
                else : # 段落内容大于6个字，进行扩展后，提取关键字
                    sDetalContent = utils.TrimContent(sPara)
                    if len(sDetalContent.strip()) > 3: #有一定长度的内容进行关键词分析
                        print(sDetalContent)
                        sSetpDesc = "-- generate detail keywords......"
                        sTxtDetailKewords = utils.LlmConversation(sDetalContent,his=[[qHis,aHis]],cnt_id=cnt_id, sToken=token_code,iTemplateType=3) #,iTemplateType=3 提取关键字
                        lDetailKeywords = utils.GetKeywords(sTxtDetailKewords)
                        
                        for index in range(len(lDetailKeywords)):
                            sKeyword += lDetailKeywords[index] + " "
                        for index in range(len(lSummaryKeywords)):
                            sKeyword += lSummaryKeywords[index] + " "
                        print("搜索关键词（l）: {}".format(sKeyword))
                # # 对每一段的扩写
                lstKeywords = utils.GetKeywords(sTxtSummaryKewords)
                print(lSummaryKeywords)
                extResult = self.ExtendWriting(lstKeywords,cnt_id_seed,token_code,qHis,sTxtSummary)
                sLog += sExtendPara + "\r\n"
                sLog += "......................................................................." + "\r\n"
                sLog += extResult[1]
                sTxt += sSplit + "\r\n"
                sTxt += sExtendPara + "\r\n"
                sTxt += "......................................................................." + "\r\n"
                sTxt += extResult[0]
            else : # 不用搜索，直接根据提纲扩写
                sLlmConversationResult = utils.LlmConversation(sExtendPara,his=[[qHis,aHis]],cnt_id=cnt_id, sToken=token_code,iTemplateType=5) #,iTemplateType=5 对以下内容进行扩展
                sLog += sExtendPara + "\r\n"
                sLog += "......................................................................." + "\r\n"
                sLog += sLlmConversationResult
                sTxt += sSplit + "\r\n"
                sTxt += sExtendPara + "\r\n"
                sTxt += "......................................................................." + "\r\n"
                sTxt += sLlmConversationResult
        
        utils.SaveLog(sLog)
        utils.SaveLog(sTxt,log_filename="m-return-text-log")
        sContent = sTxt
        
        return sContent