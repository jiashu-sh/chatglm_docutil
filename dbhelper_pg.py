import io
import psycopg2
import uuid


class DbConnection():
    
    def __init__(self,
                 host="192.168.171.53",
                 port="5432",
                 user="postgres",
                 password="p@sscode1234!",
                 database="llm_content_db") :
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def Version(self):
        sVersion = "1.0 20230530"
        sReturn = "version:{0} , host:{1}".format(sVersion,self.host)
        return sReturn
        
    def InsertLlmResp(self,txt_req,txt_resp,txt_his,cnt_id="", resp_uuid = "",token_code = "",user_id=0):
        # 插入与LLM对话的问题与返回信息
        iResult = 0
        conn = None
        # 连接PostgreSQL数据库
        try:
            # conn = psycopg2.connect(host="192.168.171.53", port="5432", user="postgres", password="p@sscode1234!", database="llm_content_db")
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            # print("Connection successful!")
        except Exception as e:
            print("Connection failed:", e)
            return sReturnVal

        # 设置数据
        # print(uuid.uuid1())
        token = str(uuid.uuid1())
        # print(token_code)
        if len(token_code) > 0:
            token = token_code
            # print(token)
            
        if len(txt_req)==0:
            return iResult
        if len(txt_resp)==0:
            return iResult
        
        if len(resp_uuid)==0:
            resp_uuid = str(uuid.uuid1())
            
        # req_text = "你好"
        # resp_text = "你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"

        cur = conn.cursor()
        # 插入数据
        try:
            # cur_exe = 
            # sql = "INSERT INTO llm_resp (cnt_id,resp_uuid,token_code,req_text,resp_text,resp_his,update_uid) VALUES (%s, %s ,%s, %s, %s, %s, %s)", (cnt_id,resp_uuid, token, txt_req, txt_resp,txt_his,str(user_id))
            cur.execute("INSERT INTO llm_resp (cnt_id,resp_uuid,token_code,req_text,resp_text,resp_his,update_uid) VALUES (%s, %s ,%s, %s, %s, %s, %s)", (cnt_id,resp_uuid, token, txt_req, txt_resp,txt_his,str(user_id)))
            # print("cur:")
            # print(cur_exe)
            conn.commit()
            iResult = 1
            # print("Insert success ",iResult)
        except Exception as e:
            print("Insert failed:", e)

        # 关闭数据库连接
        conn.close()
        
        sReturnVal = ""
        if (iResult > 0):
            sReturnVal = resp_uuid
        
        return sReturnVal
        
    def InsertContentDocId(self,cnt_id="",user_id=0):
        # 插入一个cnt_id，然后查询获取一个doc_id
        conn = None
        # 连接PostgreSQL数据库
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            # print("Connection successful!")
        except Exception as e:
            print("Connection failed:", e)
            return ""

        cnt_id = cnt_id.strip()
        # 设置数据
        if len(cnt_id)==0:
            return ""
        
        # print(cnt_id)
        
        cur = conn.cursor()
        # 插入数据
        try:
            # iResult = cur.execute("INSERT INTO llm_content_vs_doc (cnt_id,update_uid) VALUES (%s, %s)", (cnt_id,str(user_id)))
            cur.execute("INSERT INTO llm_content_vs_doc (cnt_id,update_uid) VALUES (%s, %s)", (cnt_id,str(user_id)))
            conn.commit()
            # print("Insert success : {}".format(cnt_id))
        except Exception as e:
            print("Insert failed:", e)
        cur.close()
        # 关闭数据库连接
        conn.close()
        
        return cnt_id
    
    
    def GetContentDocId(self,cnt_id=""):
        # 通过之前插入的nt_id，查询获取一个doc_id
        iResult = 0
        conn = None
        # 连接PostgreSQL数据库
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            # print("Connection successful!")
        except Exception as e:
            print("Connection failed:", e)
            return iResult

        cnt_id = cnt_id.strip()
        # 设置数据
        if len(cnt_id)==0:
            return iResult
        
        cur_sel = conn.cursor()
        # 插入数据
        try:
            sql = "SELECT doc_id FROM llm_content_vs_doc WHERE void=0 and cnt_id='{}' order by update_time desc limit 1 ".format(cnt_id)
            cur_sel.execute(sql)
            # print(sql)
            # print(cur_sel.rowcount)
            # 获取结果
            row = cur_sel.fetchone()
            # print(row)
            while row is not None:
                iResult = int(str(row[0]))
                # print(row)
                row = cur_sel.fetchone()
                
        except Exception as e:
            print("Fetch failed:", e)
        
        cur_sel.close()
        # 关闭数据库连接
        conn.close()
        
        return iResult
        
    def InsertLlmContent(self,cnt_id,cnt_text,cnt_title="",cnt_summary = "",cnt_link="",cnt_type_no=0,user_id=0):
        bInsert = False
        conn = None
        # 连接PostgreSQL数据库
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            # print("Connection successful!")
        except Exception as e:
            print("Connection failed:", e)
            return bInsert
        cnt_id = cnt_id.strip()
        cnt_text = cnt_text.strip().strip('\n').strip('\t')
        # 检查数据
        if len(cnt_id)==0:
            print("cnt_id can not be empty!")
            return False
        if len(cnt_text)==0:
            print("cnt_text can not be empty!")
            return False

        cur = conn.cursor()
        # 插入数据
        try:
            cur.execute("INSERT INTO llm_content (cnt_id,cnt_type_no,cnt_title,cnt_summary,cnt_link,cnt_text,update_uid) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                  (cnt_id, cnt_type_no, cnt_title,cnt_summary,cnt_link,cnt_text,str(user_id)))
            conn.commit()
            # print("Insert success : {}".format(cnt_id))
            bInsert = True
        except Exception as e:
            print("Insert failed:", e)

        # 关闭数据库连接
        conn.close()
        
        return bInsert