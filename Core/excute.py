from Logging.logg_create import logger
from Core.Schedule import Schedule
from utils.Load_Setting import load_setting,get_m3u8
from multiprocessing import Process
from Downloader.M3_Analy import M3_Analy
from multiprocessing import Process            
def excute():
    A_Setting = load_setting()
    """
    分三个进程，
    第一个进程进行m3u8数据层级的分析和爬取
    第二个进程进行数据库的搜寻，根据配置选项进行对应的搜索并且得到m3u8的对象信息
    ，还有ts列表进行爬取视频，
    第三个进程或者多开几个进程写入文件和第二个进程进行进程间通信使用rabbitmq，
    """

    Schedule(settings=A_Setting).start()
