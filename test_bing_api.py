import time
from bing_api import BingApi

if __name__ == "__main__" :
    sContentDefault = "LLM大模型"
    
    sTxtGet = input("请输入生成内容:\n")
    if len(sTxtGet.strip()) == 0:
        sTxtGet = sContentDefault
    sConfirm = input("您输入内容为:\n  {}\n是否确认?(y/n)".format(sTxtGet))
    
    if (sConfirm.strip().lower()) == "n":
        print("用户退出")
        exit(0) # 执行完成自由对话模式，退出。
    
    
    # 执行标准全文一键生成模式（耗时较长）
    print("执行中，请稍候...")
    start_time = time.time()
    
    bing = BingApi()
    contacts = bing.Search(search_text=sTxtGet,s_count=5)
    print("查询耗时： {} (s)".format(str(time.time()-start_time)))
    print("result count: {}".format(len(contacts)))
    print(contacts)