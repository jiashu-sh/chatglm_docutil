#_*_coding:utf-8_*_
import requests
import json
import sys
import uuid
import datetime

"""调用langchain的PromptTemplate的简单示例。
Prompt模板十分有用，比如，我们想利用langchain构建专属客服助理，并且明确告诉其只回答知识库（产品介绍、购买流程等）里面的知识，
其他无关的询问，只回答“我还没有学习到相关知识”。这时，可利用Prompt模板对llm进行约束。
"""
from langchain import PromptTemplate 
from dbhelper_pg import DbConnection

_headers = {
    "Content-Type": "application/json; charset=UTF-8"
    }

class GlmApi():
    
    def __init__(self,
                 url="http://10.19.1.250:8000",
                 prompt="你好",
                 history=[],
                 max_length=2048,
                 top_p=0.7,
                 temperature=0.95) :
        # url = "http://10.19.1.250:8000"
        # pyload = {"prompt": txt_req,"history": [],"max_length":2048,"top_p":0.7,"temperature":0.95}
        self.url = url
        self.prompt = prompt
        self.history = history
        self.max_length = max_length
        self.top_p = top_p
        self.temperature = temperature
        self.headers = _headers

    # def LlmCallback(token_code):
    #     print("LlmCallback : " + token_code)
    #     return token_code

    def LlmConversation(self,sContent="你好",his=[],cnt_id="", sToken="",iTemplateType=0,bPrintText = False): #, func_llm_call_back=LlmCallback()
        # iTemplateType=0 : 表示默认prompt，详细描述 ，iTemplateType=-1、0、1、2、3、4、 9 表示 不指定命令直接 概述列提纲、详细描述、概括、提取搜索关键字、参考资料进行写作、  意图分析
        txt_resp = "."
        resp_uuid = str(uuid.uuid1()) # 每轮对话生成一个resp_uuid
        # token_code = str(uuid.uuid1())
        if len(sToken.strip()) == 0:
            sToken = str(uuid.uuid1())
        # print(token_code)
        
        def env_hooks(resp_uuid, *args,  **kwargs): #response,
            # print("end: " )
            # print(response.headers["Content-Type"])
            if bPrintText :
                print("2. env_hooks - {} ,uuid:{}".format(str(datetime.datetime.now()) ,resp_uuid))
        
        # region 设置提示词类型
        # 默认无特殊提示词
        prompt_template = """
        {question_description}
        """
        if iTemplateType == -1 :
            prompt_template = """
            {question_description}
            """
        elif iTemplateType == 0 :
            prompt_template = """
            请概述以下内容，并列出提纲：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 1 :
            prompt_template = """
            请详细描述分析以下内容：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 2 :
            prompt_template = """
            请分析并概括说明以下内容：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 3 :
            prompt_template = """
            将以下内容概括为3到5个可以用于搜索引擎搜索的关键词：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 4 :
            prompt_template = """
            请参考以下资料，进行总结并详细描述：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 5 :
            prompt_template = """
            对以下内容进行扩展：
            “
            {question_description}
            ”
            """
        elif iTemplateType == 9 :
            prompt_template = """
            意图分析：
            “
            {question_description}
            ”
            """
        prompt_template.strip().strip('\t')
        # endregion
        
        description = sContent
        prompt_template = PromptTemplate(input_variables=["question_description"], template=prompt_template)
        
        if bPrintText :
            print(prompt_template.format(question_description=description))

        txt_req = prompt_template.format(question_description=description)
        # txt_req = "请概述基于中文语音识别技术结合大语言模型的智能信息查询项目开题报告。请一步步列出步骤，并将结果以json格式表达。"
        if len(txt_req.strip()) == 0:
            txt_req = self.prompt
        txt_req = txt_req.strip().strip('\n').strip('\t')
        
        pyload = {"prompt": txt_req,"history": his,"max_length":self.max_length,"top_p":self.top_p,"temperature":self.temperature}
        print("1. start (LlmConversation) - {} ,uuid:{}".format(str(datetime.datetime.now()) ,resp_uuid))
        response = requests.post(self.url, data=json.dumps(pyload), headers=self.headers, hooks=dict(response=env_hooks(resp_uuid=resp_uuid))).text
        # print(response)

        result = json.loads(response)

        # print(result["response"])
        # print("..........")
        # print(result["history"])
        
        txt_resp = result["response"]
        txt_his = result["history"]
        
        # 数据库操作：记录对话内容-------------------------------------------------------------
        dbconn = DbConnection()
        confirm_token = dbconn.InsertLlmResp(txt_req,txt_resp,str(txt_his),cnt_id, resp_uuid, token_code=sToken) #,token_code="",user_id=0
        # -----------------------------------------------------------------------------------
        if bPrintText :
            print("3. db insert (LlmConversation) - {} ,confirm_token:{}".format(str(datetime.datetime.now()) ,confirm_token))
        
        return txt_resp
    
    def LlmConversationV2(self,sAdjective,sContent,his=[],cnt_id="", sToken="",iTemplateType=0): #, func_llm_call_back=LlmCallback()
        # iTemplateType=0 : 表示默认prompt，详细描述 ，iTemplateType=-1、0、1、2、3、4、 9 表示 不指定命令直接 概述列提纲、详细描述、概括、提取搜索关键字、参考资料进行写作、  意图分析
        txt_resp = "."
        resp_uuid = str(uuid.uuid1()) # 每轮对话生成一个resp_uuid
        # token_code = str(uuid.uuid1())
        if len(sToken.strip()) == 0:
            sToken = str(uuid.uuid1())
        # print(token_code)
        
        description = sContent
        def env_hooks(resp_uuid, *args,  **kwargs): #response,
            # print("end: " )
            # print(response.headers["Content-Type"])
            print("2. env_hooks - {} ,uuid:{}".format(str(datetime.datetime.now()) ,resp_uuid))
        
        # region 设置提示词类型
        # 默认无特殊提示词
        prompt_template = """
        {adjective}{question_description}
        """
        if iTemplateType == -1 :
            prompt_template = """
            {adjective}{question_description}
            """
        elif iTemplateType == 0 :
            prompt_template = """
            {adjective}{question_description}
            """
        elif iTemplateType == 1 :
            prompt_template = """
            请根据参考资料，详细描述分析以下内容：
            “
            {question_description} 
            ”
            参考资料：
            “
            {adjective}
            ”
            """
        
        prompt_template.strip().strip('\t')
        # endregion
        
        description = sContent
        prompt_template = PromptTemplate(input_variables=["adjective","question_description"], template=prompt_template)
        
        txt_req = prompt_template.format(adjective=sAdjective,question_description=description)
        print(txt_req)
        
        # txt_req = "请概述基于中文语音识别技术结合大语言模型的智能信息查询项目开题报告。请一步步列出步骤，并将结果以json格式表达。"
        if len(txt_req.strip()) == 0:
            txt_req = self.prompt
        txt_req = txt_req.strip().strip('\n').strip('\t')
        
        pyload = {"prompt": txt_req,"history": his,"max_length":self.max_length,"top_p":self.top_p,"temperature":self.temperature}
        print("1. start - {} ,uuid:{}".format(str(datetime.datetime.now()) ,resp_uuid))
        response = requests.post(self.url, data=json.dumps(pyload), headers=self.headers, hooks=dict(response=env_hooks(resp_uuid=resp_uuid))).text
        # print(response)

        result = json.loads(response)

        # print(result["response"])
        # print("..........")
        # print(result["history"])
        
        txt_resp = result["response"]
        txt_his = result["history"]
        
        # 数据库操作：记录对话内容-------------------------------------------------------------
        dbconn = DbConnection()
        confirm_token = dbconn.InsertLlmResp(txt_req,txt_resp,str(txt_his),cnt_id, resp_uuid, token_code=sToken) #,token_code="",user_id=0
        # -----------------------------------------------------------------------------------
        print("3. db insert - {} ,uuid:{}".format(str(datetime.datetime.now()) ,resp_uuid))
        
        return txt_resp
        
        '''
        sys.exit(0)

        pyload = {"prompt": "唐宋八大家是谁？","history": [],"max_length":2048,"top_p":0.7,"temperature":0.95}

        response = requests.post(url, data=json.dumps(pyload), headers=headers).text
        print(response)

        result = json.loads(response)

        print(result["response"])
        print("..........")
        print(result["history"])

        # print(result)
        is_continue = True
        if is_continue :
            pyload = {"prompt": "最著名的是哪位？","history": result["history"],"max_length":2048,"top_p":0.7,"temperature":0.95}
            print(pyload)
            response = requests.post(url, data=json.dumps(pyload), headers=headers).text
            result = json.loads(response)
            print(result["response"])
        '''
