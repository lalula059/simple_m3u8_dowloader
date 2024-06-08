from Proxy.pool_get import proxy_pool
from Logging.logg_create import logger
from Downloader.M3_Analy import M3_Analy
from typing import Union
from utils.tools import check
from Data_Base.base import save_Data_handler
class Schedule:
    def __init__(self,settings = None,*args,**kwargs) -> None:
        self.settingss = settings
        self.pool:Union[proxy_pool,None] = check(self.settingss,'PROXY_SET')
        # 这是第一个M3分析器
        self.M3_Fi = M3_Analy(settings = self.settingss,pool = self.pool,*args,**kwargs)
        self.DS = None
        self.M3_TWO =None
    def start(self):
        data = self.M3_Fi.start()
        save_Data_handler(data=data,settings=self.settingss)
        # 接下来是开始多进程
        pass