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
from dbconn_pg import DbConnection

headers = {
    "Content-Type": "application/json; charset=UTF-8"
    }
url = "http://10.19.1.250:8000"

def env_hooks(resp_uuid, *args,  **kwargs): #response,
    print("end: " + str(datetime.datetime.now()))
    # print(response.headers["Content-Type"])
    print("fin:" + resp_uuid)

if __name__ == "__main__" :
    
    token_code = str(uuid.uuid1())
    print(token_code)
    
    dbconn = DbConnection()
    # print(dbconn.Version())
    
    txt_req = "请概述基于中文语音识别技术和大语言模型的智能信息查询项目开题报告。"
    txt_req = "请详细展开说明这一点：利用中文语音识别技术和大语言模型，构建一个智能信息查询系统，能够实现中文文本的语音输入、识别和查询。"
    txt_req = "意图分析：播放歌曲《真心英雄》。"
    txt_req = "意图分析：播放我的默认歌曲列表。"
    txt_req = "意图分析：通过搜索引擎来搜索内容'目前常见中文大语言模型'"
    txt_req = "将以下内容概括为可以用于搜索引擎搜索的关键字：'利用中文语音识别技术和大语言模型，构建一个智能信息查询系统，能够实现中文文本的语音输入、识别和查询。'"
    
    txt_req = """
    请概括以下内容：
    简介:
在.NET开发中，多线程是一个常见的需求。为了确保线程安全和资源的正确使用，我们需要使用同步机制。其中一种常用的同步机制是信号量（Semaphore），它可以用于控制同时访问特定资源的线程数量。本文将介绍在.NET中如何在线程中使用信号量，以确保线程安全和 资源的合理分配。
1、什么是信号量？
信号量是一种用于同步和互斥的机制，用于控制对资源的访问。它维护一个计数器，表示可用资源的数量。线程在访问资源之前必须获取信号量的许可，如果信号量计数器大于零，则线程可以继续执行；否则，线程将被阻塞，直到有可用的许可。
2、创建和初始化信号量
在.NET中，可以使用Semaphore类来创建和管理信号量。可以通过指定初始许可数量和最大许可数量来初始化信号量。例如，以下代码创 建一个初始许可数量为3，最大许可数量为5的信号量：
3、获取和释放信号量
线程可以使用信号量的WaitOne方法获取许可。如果有可用的许可，线程将继续执行；否则，它将被阻塞，直到有可用的许可。获取许可 后，线程可以访问受信号量保护的资源。完成后，线程应使用Release方法释放许可，以便其他线程可以获取许可并访问资源。
4、信号量的应用场景
信号量在多线程环境下的应用场景非常广泛。例如，当有限数量的资源需要被多个线程共享时，可以使用信号量来限制同时访问资源的线程数量。另一个常见的应用是控制对文件、数据库连接或网络连接等外部资源的并发访问。
    """
    
    txt_req = "请写一下：在.NET中如何使用信号量来控制线程同步和资源访问，以保障多线程开发的线程安全和资源合理分配。信号量是一种常用的同步机制，可以用于限制同时访问特定资源的线程数量，避免竞争条件和数据损坏。在.NET中，可以使用Semaphore类来创建和管理信号量，通过指定初始许可数量和最大许可数量来初始化信号量，使用WaitOne方法获取许可，使用Release方法释放许可，以实现线程同步和资源控制。信号量的应用场景非常广泛，例如在多线程环境下限制同时访问资源的数量，控制对文件、数据库连接或网络连接等外部资源的并发访问。在实际应用中，需要注意适当的许可管理，以避免死锁和资源泄漏的问题。"
    txt_req = ""
    
    name_template = """
    请将以下问题详细描述一下，并给出3~5个建议搜索关键词：{question_description}
    """
    name_template = str("""
    请将以下问题详细描述一下，并给出3~5个建议搜索关键词：{question_description}
    """)
    # name_template.strip().strip('\r').strip('\n').strip('\r\n').strip('\t')
    # print(name_template)
    
    prompt_template = PromptTemplate(input_variables=["question_description"], template=name_template)
    description = "利用中文语音识别技术和大语言模型，构建一个智能信息查询系统，能够实现中文文本的语音输入、识别和查询。" # "列举spaceX星舰在2022年后的发射记录"
    txt_req = (prompt_template.format(question_description=description)).strip().strip('\n').strip('\t')
    print(prompt_template.format(question_description=description))
    print(txt_req)
    # sys.exit(0)

    
    txt_req = "请概述基于中文语音识别技术结合大语言模型的智能信息查询项目开题报告。请一步步列出步骤。"
    txt_req = "你好"
    
    pyload = {"prompt": txt_req,"history": [],"max_length":2048,"top_p":0.7,"temperature":0.95}

    print(token_code + " : " + txt_req)
    # response = requests.post(url, data=json.dumps(pyload), headers=headers,stream=True)
    response = requests.post(url, data=json.dumps(pyload), headers=headers, hooks=dict(response=env_hooks(token_code)))
    
    # for chunk in response.iter_content(chunk_size=128):
    #     print(chunk)
        
    # print(response.text)

    result = json.loads(response.text)

    print(result["response"])
    print("..........")
    print(result["history"])
    
    txt_resp = result["response"]
    txt_his = result["history"]
    
    iRows = dbconn.InsertLlmResp(txt_req,txt_resp,str(txt_his),token_code=token_code) #,token_code="",user_id=0
    
    print(iRows)
    
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
