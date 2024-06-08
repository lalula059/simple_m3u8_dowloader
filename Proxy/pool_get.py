from os.path import dirname,exists
from Logging.logg_create import logger
import random
class proxy_pool:
    txt_proxy = []
    instance = None
    def __new__(cls,*args,**kwargs) :
        if cls.instance is None:
            cls.instance = super().__new__(cls,*args,**kwargs) 
        return cls.instance
        
    def __init__(self) -> None:
        txt_loader(self)
    def set_ip_pool(self,value):
        proxy_pool.txt_proxy = value
    def get(self):
        if proxy_pool.txt_proxy:
            return random.choice(proxy_pool.txt_proxy)
        else:
            return False
    def delete(self,ip):
        try:
            if isinstance(ip,dict):
                ip = ip['http'].split('@')[1]
            proxy_pool.txt_proxy.remove(ip)
            logger.debug("检测是否被删除{}".format(proxy_pool.txt_proxy))
        except ValueError as e:
            logger.debug(f"元素已被删除")


def txt_loader(ins):
    # 设置txt文件
    txt_file = dirname(dirname(__file__)) + '\proxy.txt'
    if exists(txt_file):
        logger.info("检测txt文件中是否存在代理{}".format(txt_file))
        with open(txt_file,'r') as f:
            text = [i.strip() for i in (f.read().split('\n'))]
            logger.info("代理池为{}".format(text))
            ins.set_ip_pool(value=text)       