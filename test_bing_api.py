
from bing_api import BingApi

if __name__ == "__main__" :
    sContent = "LLM大模型"
    bing = BingApi()
    contacts = bing.Search(search_text=sContent,s_count=5)
    print("result count: {}".format(len(contacts)))
    print(contacts)