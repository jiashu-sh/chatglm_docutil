import sys
import time
import datetime
import uuid

from llm_controller import Controller
controller = Controller()

if __name__ == "__main__" :
    # python main_cli.py free-test:true
    # python main_cli.py internet-search:false
    bModeFreeTest = False # 自由对话模式
    bInternetSearch = True # 默认搜索Internet
    
    if (len(sys.argv) > 1) :
        # cmdPara1 = str(sys.argv[1])
        for idxPara in range(len(sys.argv)) :
            sPara = sys.argv[idxPara]
            print(sPara)
            if sPara == "free-test:true" :
                bModeFreeTest=True
            if sPara == "internet-search:true" :
                bInternetSearch=True
            if sPara == "internet-search:false" :
                bInternetSearch=False
    
    if bModeFreeTest :
        sLlmConversation = input("请输入Glm对话内容:\n")
        sReturn = controller.LlmConversation(sLlmConversation)
        print(sReturn)
        exit(0)        
    
    sTxtGet = input("请输入生成内容:\n")
    sConfirm = input("您输入内容为:\n  {}\n是否确认?(y/n)".format(sTxtGet))
    if (sConfirm.strip().lower()) == "n":
        print("用户退出")
        exit(0) # 执行完成自由对话模式，退出。
    
    
    # 执行标准全文一键生成模式（耗时较长）
    print("执行中，请稍候...")
    start_time = time.time()
    sTxt = controller.GenerateContent(sTxtGet,bInternetSearch)
    
    print("最终生成内容(耗时{}s)：".format(str(time.time()-start_time)))
    print(sTxt)
    # print(time.time()-start_time)
    exit(0)