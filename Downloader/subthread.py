from Logging.logg_create import logger
import requests
from Configure.config import THREADNUMBER_TS
from typing import Union
from Configure.config import HEADERS
import threading
import os
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
# 这一个文件是ts请求时调用
proxxy = {
    'http':'http://127.0.0.1:80',
    'https':'http://127.0.0.1:8080',
    
}
requests.packages.urllib3.disable_warnings()
def write_file(path,movie_name,index,data):
    # print(path+'//'+str(index)+'.ts')
    # time.sleep(3)
    with open(path+'\\'+str(index)+'.ts','wb') as f:
        f.write(data)
    
class Main_AThread:
    def __init__(self,data:Union[object],settings = None) -> None:
        self.data = data
        # 多并发任务开始
        self.tasks = []
        # 目录节点记录
        self.movie_name_path = ''
        self.create_file()
        self.create_Data()
        self.Sem = threading.Semaphore(THREADNUMBER_TS)
    def create_file(self):
        import base64
        # 创建对应的文件夹,用base64变成英文，这样后面使用ffmepg好合并程序
        _Root_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        name = str(base64.b64encode(self.data['name'].encode('utf-8')))[2:-1]
        # 注意，有可能编码出现斜杠要处理
        if '/' in name:
            name = name.replace('/','BOOM')
        if not os.path.exists(_Root_file+f'//Movies//{name}'):
            os.makedirs(_Root_file+f'//Movies//{name}')
        self.movie_name_path = _Root_file+f'//Movies//{name}'
        
        
    def create_Data(self):
        # flag = 3
        for i,url in enumerate(self.data.get('ts_all_list')):
            # flag += 1
            task = threading.Thread(target=self.run,args=(i,url))
            self.tasks.append(task)
            # if flag == 50:
                # break


    def _start(self):
        try:
            for item in self.tasks:
                item.start()
            for item in self.tasks:
                item.join()
        except KeyboardInterrupt as e:
            print("你已结束进程")
    def run(self,index,url):
        print(str(index)+"-------------------"+url)
        try:
            with self.Sem:

                logger.info(f'正在请求第{index}链接{url}')
                     
                resp = requests.get(url=url,headers=HEADERS,verify=False)
                if resp.status_code == 200:
                    if self.KEY:
                        logger.info("正在解密输出视频中")
                        datas = self.decry_pto(resp)
                        write_file(self.movie_name_path,self.data['name'],index=index,data = datas)
                    else:
                        write_file(self.movie_name_path,self.data['name'],index=index,data = resp.content)
                else:
                    logger.error("出错了，是不是被封禁了")
        except KeyboardInterrupt as e:
            print("你已结束进程")
    
    
        
        
class No_AThread(Main_AThread):
    def __init__(self, data: object, settings=None) -> None:
        super().__init__(data, settings)
        self.KEY = False
    def start(self):
        self._start()
        
        
        
class EX_AThread(Main_AThread):
    def __init__(self, data: object, settings=None) -> None:
        super().__init__(data, settings)
        self.KEY = self.req_key()
    def req_key(self):
        # 此函数用来请求得到AES关键密码
        try:
            resp = requests.get(self.data['AES_URL'],headers=HEADERS)
            # resp ='4DYZNHT6pjKQTC3k'
            return resp
        except Exception as e:
            logger.error(f"未能成功得到AES密码---------{e}")
    def start(self):
        self._start()
    def decry_pto(self,resp,**kwargs):
        # 偏移量等前置设置
        self.decry_set()
        # 正式解密
        data = self.decry(resp,**kwargs)
        return data
        
        
    def decry(self,resp,default = 'CBC'):
        # 默认为CBC
        if default == 'CBC':
            cipher = AES.new(self.af_Key, AES.MODE_CBC, self.IV)
            # 有些数据需要进行
            if len(resp.content) % 16 != 0:
                resp.content = pad(resp.content,16)
            data = unpad(cipher.decrypt(resp.content),AES.block_size)
            return data

    def decry_set(self):
        self.IV = (self.data['AES_KEY_WORDS'][2].split('=')[1])[:AES.block_size].encode('utf-8')
        self.af_Key =  self.KEY.content