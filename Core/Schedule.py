from Proxy.pool_get import proxy_pool
from Logging.logg_create import logger
from Downloader.M3_Analy import M3_Analy
from typing import Union
from utils.tools import check,AES_handler,merge
from Data_Base.base import save_Data_handler,get_Data_handler,Data_clean
from multiprocessing import Process

class Schedule:
    def __init__(self,settings = None,*args,**kwargs) -> None:
        self.settingss = settings
        self.pool:Union[proxy_pool,None] = check(self.settingss,'PROXY_SET')
        # 这是第一个M3分析器
        self.M3_Fi = M3_Analy(settings = self.settingss,pool = self.pool,*args,**kwargs)
        self.DS = None
        self.M3_TWO =None
    def start(self):
        """第一部分"""
        
        data = self.M3_Fi.start()
        save_Data_handler(data=data,settings=self.settingss)

        """第二部分"""

        # 接下来是取得视频文件爬取视频
        dataas = get_Data_handler(settings = self.settingss)
        for data in dataas:
            # 处理ts格式，添加ts字段
            af_data = Data_clean(data)
            # 处理aes加密字段，生成对应的加密类
            task = AES_handler(af_data,self.settingss)
            task.start()
        
        
        # 合并所有的视频 需要ffmpeg，请提前配置好环境变量
        """第三部分"""
        merge()