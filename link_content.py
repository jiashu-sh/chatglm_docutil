import requests
from bs4 import BeautifulSoup

class LinkDetail():
    
    def __init__(self,log_flag=False) :
        self.log_flag = False

    def GetContent(self,slink="http://www.iciba.com/word?w=snippet"):
        
        # slink = "https://zhuanlan.zhihu.com/p/633786753"

        page = requests.get(slink)
        # page.encoding = "gbk" #gbk
        # page.encoding = "gb2312" #gbk
        page.encoding = "utf-8" #gbk
        # sGetTxt = page.text.encode('iso-8859-1').decode('gbk')
        sGetTxt = page.text

        # print(page.text)
        soup = BeautifulSoup(sGetTxt,"lxml")
        contents = soup.find_all(["p","h2","li"])

        txt = "" # slink + "\n" # ""
        for p in contents:
            s = str(p.string)
            if (len(s.strip()) > 0):
                txt += s.strip() + "\n"
            # print(p.string)
        # print(len(txt))
        # print(txt)
        return txt





