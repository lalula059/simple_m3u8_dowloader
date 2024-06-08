from utils.Load_Setting import get_m3u8
from Logging.logg_create import logger
from Downloader.base import multi_Thread
from utils.tools import format_m3u8_list,First_m3u8_handler
class M3_Analy:
    def __init__(self,settings = None,pool = None) -> None:
        self.setting = settings
        logger.info(self.setting)
        self.pool = pool
        self.mul_thread = None
    def start(self):
        self.setting , m3u8s = get_m3u8(self.setting)
        # 初始化第一次的请求类，将请求逻辑和业务逻辑分开，以便后面存储数据
        self.mul_thread = multi_Thread(settings=self.setting,NUMBER_STR='THREADNUMBER_M3U8')
        m3u8s_fix = self._format_m3u8_list(m3u8s)
        if m3u8s_fix is None:
            return
        else:
            logger.debug(f"测试pool{self.pool}")
            # get方法用于检测是否是txt文件或者是存在这个类
            proxy = self.pool if self.pool else None
            logger.debug(f"测试proxy{proxy}")
            # 用多线程来爬取
            _data = self.mul_thread.start(tasks=m3u8s,proxy=proxy)
            logger.info(f"检测M3U8分析器{_data}")
            # 处理得到的文件,进行清洗以便存储
            data = First_m3u8_handler(_data,m3u8s_fix,getattr(self.setting,'TAGS',False))
            return data
    def _format_m3u8_list(self, m3u8s):
        # 格式话爬取列表
        if m3u8s is None:
            logger.error("出错了，未得到列表")
        else:
            logger.info(f'得到待爬取列表{m3u8s}')
            m3u8s = format_m3u8_list(m3u8s)
            return m3u8s
    
