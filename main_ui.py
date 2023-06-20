import sys
import time
import datetime
import uuid
import tkinter
from tkinter import ttk


from llm_util import Utils
utils = Utils()

from llm_controller import Controller
controller = Controller()

_g_selected_index = -1



def showMainWindow(): # contacts
    # 获取搜索结果
    contacts = utils.InitSearchContents() # utils.SearchBingApi(sContent = "LLM大模型")
    iContactsCount = 0
    
    #region 设置主窗口
    mainwin = tkinter.Tk()
    mainwin.attributes("-alpha",1.0)
    mainwin.title("Contents")
    winWidth = 800
    winHeight = 750
    mainwin.geometry(
        f"{str(winWidth)}x{str(winHeight)}+"+
        f"{int((mainwin.winfo_screenwidth() - winWidth)/2)}+"+
        f"{int((mainwin.winfo_screenheight() - winHeight)/2)}"
    )
    #endregion
    
    #region 设置panel布局
    # 设置容器
    frame1 = tkinter.Frame(mainwin,height=120,width=200,relief=tkinter.GROOVE, bg='#FFFAF0',bd=1,borderwidth=1)
    # 设置填充和布局
    frame1.pack(fill=tkinter.BOTH,ipady=0,expand=True,side=tkinter.TOP)
    frame1.pack_propagate(False)
    
    # 设置容器
    framebtn1 = tkinter.Frame(mainwin,height=35,width=200,relief=tkinter.GROOVE, bg='#CCCCCC',bd=1,borderwidth=1)
    # 设置填充和布局
    framebtn1.pack(fill=tkinter.X,ipady=0,expand=False,side=tkinter.TOP)
    framebtn1.pack_propagate(False)
    
    # 设置容器
    frame2 = tkinter.Frame(mainwin,height=120,width=200,relief=tkinter.GROOVE, bg='#FFFAF0',bd=1,borderwidth=1)
    # 设置填充和布局
    frame2.pack(fill=tkinter.BOTH,ipady=0,expand=True,side=tkinter.TOP)
    frame2.pack_propagate(False)
    
    # 设置容器
    frame3 = tkinter.Frame(mainwin,height=60,width=200,relief=tkinter.GROOVE, bg='#FFFAF0',bd=1,borderwidth=1)
    # 设置填充和布局
    frame3.pack(fill=tkinter.BOTH,ipady=0,expand=True,side=tkinter.TOP)
    frame3.pack_propagate(False)
    
    # 设置容器
    frame4 = tkinter.Frame(mainwin,height=300,width=200,relief=tkinter.GROOVE, bg='#CCFFCC',bd=1,borderwidth=1)
    # 设置填充和布局
    frame4.pack(fill=tkinter.BOTH,ipady=0,expand=True,side=tkinter.TOP)
    frame4.pack_propagate(False)
    
    # 设置容器
    framebtn2 = tkinter.Frame(mainwin,height=35,width=200,relief=tkinter.GROOVE, bg='#CCCCCC',bd=1,borderwidth=1)
    # 设置填充和布局
    framebtn2.pack(fill=tkinter.X,ipady=0,expand=False,side=tkinter.BOTTOM)
    framebtn2.pack_propagate(False)
    #endregion
    
    #region 设置文本框，以及列表(Tree)
    txt_content = ""
    # 设置两个文本框， grid是设置页面位置
    text_content = tkinter.Text(frame1,width=50,height=100, font=("宋体", 11, "normal"),bg='#FFFAF0') #, tkinter.Entry(show='',  bg='white', highlightcolor='blue', relief='raised',width=60,textvariable=txt_content）
    text_content.pack(fill=tkinter.X,expand=False,side=tkinter.TOP,anchor=tkinter.N)
    text_content.insert("insert",txt_content)
    text_content.focus_set()
    
    text_selected = tkinter.Text(frame3,width=50,height=100, font=("宋体", 11, "normal"),bg='#FFFAF0') #, tkinter.Entry(show='',  bg='white', highlightcolor='blue', relief='raised',width=60,textvariable=txt_content）
    text_selected.pack(fill=tkinter.X,expand=False,side=tkinter.TOP,anchor=tkinter.N)
    text_selected.insert("insert",txt_content)
    # text_selected.focus_set()
    
    txt_splited_content = ""
    text_content_split = tkinter.Text(frame4,width=50,height=100, font=("宋体", 11, "normal"),bg='#CCFFCC') #, tkinter.Entry(show='',  bg='white', highlightcolor='blue', relief='raised',width=60,textvariable=txt_content）
    text_content_split.pack(fill=tkinter.X,expand=False,side=tkinter.TOP,anchor=tkinter.N)
    text_content_split.insert("insert",txt_splited_content)
    

    # 实例化控件，设置表头样式和标题文本,listview 参考文档如下：
    # https://www.jianshu.com/p/52925c3d3caf
    columns = ("name", "snippet", "url","docid")
    headers = ("标题", "片段", "url","id")
    widthes = (550, 220, 80, 0)
    tv = ttk.Treeview(frame2, height=200, show="headings", columns=columns)
    tv.pack(fill=tkinter.X,expand=False,side=tkinter.TOP,anchor=tkinter.N)

    for (column, header, width) in zip(columns, headers, widthes):
        tv.column(column, width=width, anchor="w")
        tv.heading(column, text=header, anchor="w")

    #region 定义方法
    def del_data(): # 删除一行
        items = tv.get_children()[1:2]
        tv.delete(items)
        
    def inser_data(contacts):
        """插入数据"""
        # contacts =[
        #     ('李4', '1589928xxxx', 'lisi@google.com', '谷歌'),
        #     ('王5', '1340752xxxx', 'wangwu@baidu.com', '微软'),
        #     ('郑6', '1899986xxxx', 'zhenghe@163.com', '网易'),
        # ]
        for i, search_result in enumerate(contacts):
            tv.insert(parent='', index=i,iid=i, values=search_result)
            
    def on_click(event):
        if iContactsCount<=0 :
            return
        widgetObj = event.widget                          # 取得控件
        itemselected = widgetObj.selection()[0]           # 取得选项 
        # print(widgetObj.item(itemselected,"values")[0])
        text_selected.delete("1.0","end") #删除文本 txt_entry.delete(start_index,end_index)#删除文本
        text_selected.insert("insert",widgetObj.item(itemselected,"values")[2]+ "\r\n") # 第3列：url
        text_selected.insert("insert",tv.selection()[0] + "." + widgetObj.item( itemselected,"values")[1]  ) # 第2列：片段
        global _g_selected_index 
        _g_selected_index = int(tv.selection()[0])
        # get_data(int(tv.selection()[0]))
        
    #endregion
    tv.pack()

    inser_data(contacts)
    tv.bind('<ButtonRelease-1>',on_click)
    #endregion
    
    #region 定义方法2
    def get_data(idx=0):
        # 获取选中行的链接字段并返回
        item = tv.get_children()[idx] # print(tv.item(item, "values"))
        slink = str(tv.item(item, "values")[2]) # str(tv.item(item, "values")[2]) # 第三列：url 
        # 获取链接明细全文------------------------------------------
        sContent = utils.GetLinkContent(slink)
        # ---------------------------------------------------------
        return sContent
    def get_cntid(idx=0):
        # 获取选中行的链接字段并返回
        item = tv.get_children()[idx] # print(tv.item(item, "values"))
        cnt_id = str(tv.item(item, "values")[3]) # str(tv.item(item, "values")[2]) # 第三列：url 
        return cnt_id
    
    # def LlmCallback(token_code):
    #     print("LlmCallback : " + token_code)
    #     return token_code

    def sendStr():
        txt_get = text_content.get("1.0","end")
        global _g_selected_index 
        if (_g_selected_index > -1): # 
            # 填入表格选中行内容
            text_content_split.delete("1.0","end") #删除文本
            text_content_split.insert("insert",txt_get)
            sFinal = ""
            sSummarize = ""
            cnt_id = get_cntid(_g_selected_index) # str(uuid.uuid1()) # 文档id
            token_code = "task-" + cnt_id
            # 获取选中行具体内容
            iMaxContentLength = 800
            text_link_content = get_data(_g_selected_index)
            splited_content = utils.SplitParagraphs(text_link_content,iMaxContentLength) # 按段落拆分，800以内合并
            # 打印出来
            for i in range(len(splited_content)) :
                print(splited_content[i])
                print(".................................")
                sFinal += splited_content[i]
                sFinal += "\n" + str(len(splited_content[i])) + "................................." + "\n"
                
            for i in range(len(splited_content)) :
                # 使用Glm获取对话内容（概括）------------------------------
                # glmapi = GlmApi() #使用GlmApi
                sTxt = utils.LlmConversation(splited_content[i],his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=2) #,func_llm_call_back=LlmCallback(token_code)
                print(sTxt)
                print(".................................")
                sSummarize += "({})".format(sTxt)
                sSummarize += "\n" + "................................." + "\n"
            
            text_content_split.insert("insert",sFinal + "\n" + sSummarize)
            # 
    #endregion        
            
    button2 = tkinter.Button(framebtn2,text='Continue'+'\n' + '(next step)', width=150,height=2,font=("Arial,宋体", 9, "normal"),command=sendStr)
    button2.pack(expand=True)
    
    
    def expDoc() :
        qHis="基于中文语音识别技术和大语言模型的智能信息查询项目开题报告"
        aHis="本项目旨在利用中文语音识别技术和大语言模型，构建一个智能信息查询系统，能够实现中文文本的语音输入、识别和查询。该系统将利用人工智能技术，实现对大量中文语料库的学习和训练，从而提高语音识别和自然语言处理的准确性和效率。同时，该系统还将实现对于用户输入的中文文本进行智能分析和查询，为用户提供更加智能化的信息查询服务。"
        # 获取 
        txt_get = text_content.get("1.0","end")
        
        cnt_id = "sum-" + str(uuid.uuid1())
        token_code = str(uuid.uuid1())
        sTxt = controller.GenerateContent(txt_get) #utils.LlmConversation(txt_get,his=[],cnt_id=cnt_id, sToken=token_code,iTemplateType=1) #,iTemplateType=1 详细描述内容
        # print(sTxt)
        text_content_split.insert("insert",str(sTxt))
        
        return
        splited_content = utils.SplitParagraphs(sContent=txt_get,iMaxContentLength=0) # 按段落拆分
        sFilteredText = ""
        toExpandContents = []
        for i in range(len(splited_content)) :
            sTemp = splited_content[i].strip().strip('\n').strip('\t').strip()
            if len(sTemp) == 0:
                continue
            elif sTemp.startswith('、',1):
                print(sTemp)
            elif sTemp.endswith('：'):
                print(sTemp)
            else :
                toExpandContents.append(sTemp)
                sFilteredText += sTemp + "\n"
        # print(splited_content) 
        cnt_id = "cnt-" + str(uuid.uuid1())
        token_code = str(uuid.uuid1())
        # text_content_split.insert("insert",str(sFilteredText))
        sExpandContent = ""
        for i in range(len(toExpandContents)) :
            # 使用Glm获取对话内容（概括）------------------------------
            # glmapi = GlmApi() #使用GlmApi
            sTxt = utils.LlmConversation(toExpandContents[i],his=[[qHis,aHis]],cnt_id=cnt_id, sToken=token_code,iTemplateType=1) #,iTemplateType=1 详细描述内容
            print(sTxt)
            print(".................................")
            sExpandContent += "({})".format(toExpandContents[i]) + "\r\n" + (sTxt)
            sExpandContent += "\n" + "................................." + "\n"
        text_content_split.insert("insert",str(sFilteredText))
    
    button1 = tkinter.Button(framebtn1,text='Start' , width=150,height=2,font=("Arial,宋体", 9, "normal"),command=expDoc)
    button1.pack(expand=True)
    
    # 将其加入主循环
    mainwin.mainloop()


if __name__ == "__main__" :
    
    bSearchSave = False
    
    
    '''
    # BingApi查询
    bing = BingApi()
    contacts = bing.Search("LLM大模型")
    if bSearchSave:
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
            confirm_token = dbconn.InsertLlmContent(cnt_id=cnt_id,cnt_text=cnt_text,cnt_title=cnt_title,cnt_summary=cnt_summary,cnt_link=cnt_link) #
            # -----------------------------------------------------------------------------------
    '''
    
    # 显示窗体
    showMainWindow() #contacts
    
    sys.exit(0)