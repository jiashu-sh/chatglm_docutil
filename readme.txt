Milvus安装
https://zhuanlan.zhihu.com/p/405186060

web管理界面
http://10.19.1.251:8000/





参考文献：
https://blog.csdn.net/a914541185/article/details/130150101

--Python 中request以json形式发送post请求:
https://zhuanlan.zhihu.com/p/109486247
--SyntaxError: Non-UTF-8 code starting with ‘\xe4‘ in file解决办法
https://blog.csdn.net/ctrigger/article/details/111189653


db：
llm_content_db


CREATE SEQUENCE "seq_llm_content_cnt_no" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
-- ----------------------------
-- Table structure for llm_content
-- ----------------------------
DROP TABLE IF EXISTS llm_content;
CREATE TABLE llm_content (
  llm_content_id serial NOT NULL PRIMARY KEY ,
  cnt_no integer NULL DEFAULT nextval('seq_llm_content_cnt_no'::regclass),
  cnt_id varchar(60) null ,
  cnt_type_no integer NULL default 0 ,
  cnt_title varchar(200) null ,
  cnt_summary varchar(2000) null ,
  cnt_text text null ,
  cnt_link varchar(500) null ,
  void integer default 0 ,
  update_time timestamp DEFAULT (now()),
  update_uid integer default 0 
)
;

-- ----------------------------
-- Uniques structure for table llm_content
-- ----------------------------
CREATE UNIQUE INDEX uk_llm_content
ON llm_content (
cnt_no ASC
);

 
--DROP SEQUENCE IF EXISTS "seq_llm_resp_resp_no";
CREATE SEQUENCE "seq_llm_resp_resp_no" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
-- ----------------------------
-- Table structure for llm_resp
-- ----------------------------
DROP TABLE IF EXISTS llm_resp;
CREATE TABLE llm_resp(
  llm_resp_id serial NOT NULL PRIMARY KEY ,
  resp_no integer NOT  NULL DEFAULT nextval('seq_llm_resp_resp_no'::regclass),
  resp_uuid varchar(60) null ,
  cnt_id varchar(60) null ,
  token_code varchar(60) null ,
  req_text varchar(2000) null ,
  resp_text varchar(4000) null ,
  resp_his varchar(4000) null ,
  resp_content text null ,
  void integer default 0 ,
  update_time timestamp DEFAULT (now()),
  update_uid integer default 0 
)
;

-- ----------------------------
-- Uniques structure for table llm_resp
-- ----------------------------
CREATE UNIQUE INDEX uk_llm_resp
ON llm_resp(
resp_no ASC
);


CREATE SEQUENCE "seq_llm_content_vs_doc_id" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
-- ----------------------------
-- Table structure for llm_content
-- ----------------------------
DROP TABLE IF EXISTS llm_content_vs_doc ;
CREATE TABLE llm_content_vs_doc (
  llm_content_vs_doc_id serial NOT NULL PRIMARY KEY ,
  cnt_id varchar(60) null ,
  doc_id integer NULL DEFAULT nextval('seq_llm_content_vs_doc_id'::regclass),
  fin_flag integer default 0 ,
  void integer default 0 ,
  update_time timestamp DEFAULT (now()),
  update_uid integer default 0 
)
;

