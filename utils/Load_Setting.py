from os.path import abspath,dirname
from Core_setting.Basesetting import Setting
from Logging.logg_create import logger
import sys
import importlib
import inspect
# 这一个方法检测是否从设置里面得到需要的m3u8列表
def get_m3u8(*args,**kwargs):
    try:
        for item in args:
            if isinstance(item,Setting):
                logger.info("检测用户是否在config中配置m3u8网站列表")
                if item.__getitem__('INDEX_URL'):
                    return item,item.__getitem__('INDEX_URL')
                else:
                    return None
    except Exception as e:
        logger.error(f'获取视频列表出错----{e}')
def load_setting():
    init_env()
    setting_module = importlib.import_module('Configure.config')
    setting_sets = walk_setting(setting_module)
    return setting_sets
def init_env():
    sys.path.append(dirname(dirname(abspath(__file__))))

def walk_setting(module):
    temp_setting  = Setting()
    for attr_name in dir(module):
        if attr_name.isupper():
            temp_setting.__setitem__(attr_name,getattr(module,attr_name))
    logger.debug("配置加载完成输出为{}".format(str(temp_setting)))
    return temp_setting
