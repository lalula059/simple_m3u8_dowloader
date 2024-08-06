from Logging.logg_create import logger
from Data_Base.Mongodb import Mongodb
from collections import namedtuple
import json
__all__ = ['ts_all_list']
def get_mongo(settings):
    mongo = Mongodb(settings=settings)
    return mongo
def save_Data_handler(data,settings):
    if settings.__getitem__('MONGODB_SAVE'):
        logger.info("存储数据在mongodb中")
        mongo = get_mongo(settings=settings)
        count = 0
        for item in data:
            count +=1
            mongo.save(item._asdict(),count)
    if settings.__getitem__('CSV_SAVE'):
        logger.info("存储数据中2")

def  get_Data_handler(settings,control = None):
    # 暂时设置control位控制得到多少视频数据
    if settings.__getitem__('MONGODB_SAVE'):
        logger.info("正在获取数据-----")
        return Mongodb(settings=settings).get_all()
        

def Data_clean(args):
    # 首先格式化ts视频链接,并且添加进去临时内存值,首先是检测是否为ts格式
    if('ts' in args.get('Second_m3u8_content')):
        import re
        # 提取ts列表,用不取分组
        patterns = re.compile('((?:http)?\w.*.ts)')
        res = patterns.findall(args.get('Second_m3u8_content'),re.M)
        # 添加新字段
        
        #因为加了密后面也是ts结尾，所以说还要判断
        if('URI' in res[0]):
            res = res[1:]    

        # ts前缀,并不是，取得是后面
        patterns_pre = re.compile('\w+.m3u8')
        prefix = patterns_pre.findall(args.get('Second_m3u8'))[0]
        
        # 如果不是http开头则重新设置ts文件,通过正则提取ts
        if 'http' not in res[0]:
            res_af = [args.get('Second_m3u8').replace(prefix,i) for i in res]
            args.__setitem__(__all__[0],res_af)  
        else:
            args.__setitem__(__all__[0],res) 
        return args
    else:
        logger.error("该文件不是以ts后缀结尾")