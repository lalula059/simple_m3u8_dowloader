from Logging.logg_create import logger
from Proxy.pool_get import proxy_pool
from collections import namedtuple
__KEYWORDS__ = [
    'name',
    'First_m3u8',
    'unknow_url',
    'Second_m3u8',
    'First_m3u8_content',
    'Second_m3u8_content',
    'tags',
]
def _create_m3u8_save_no_tag(resp_data,m3u8s,da_save,setting):
    data_list = []
    count = 0
    # 检查是否设置标签
    try:
        if setting:
            pass
        else:
            for item in resp_data:
                if 'EXTINF' in item[1].text:
                    logger.info(f"检测到该{m3u8s[count]}是第二层链接")
                    da_temp = da_save(name=item[0],Second_m3u8=m3u8s[count][1],Second_m3u8_content=item[1].text)
                else:
                    logger.info(f"检测到该{m3u8s[count]}是第一层链接")
                    da_temp = da_save(name=item[0],First_m3u8=m3u8s[count][1],First_m3u8_content=item[1].text)
                count+=1
                data_list.append(da_temp)
    except AttributeError as e:
        logger.error("该存储值并没有text选项，返回的是url链接")
        da_temp = da_save(name=item[0],unknow_url=m3u8s[count][1])
        data_list.append(da_temp)
    logger.info(f"检测一共多少个视频链接{len(data_list)}")  
    return data_list



# 将m3u8的获取数据进行清洗处理
def First_m3u8_handler(resp_data,m3u8s,setting):
    logger.info("正在处理相关的数据")
    if setting:
        M3U8_List = namedtuple('M3U8_List',__KEYWORDS__,defaults=[None for i in __KEYWORDS__])
        # tags表示现在不想开发
    else:
        __KEYWORDS__.pop()
        M3U8_List = namedtuple('M3U8_List',__KEYWORDS__,defaults=[None for i in __KEYWORDS__])
        logger.info(f"检测First_m3u8_handler传值{resp_data,m3u8s}")
        data_list = _create_m3u8_save_no_tag(resp_data,m3u8s,M3U8_List,setting)
    return data_list


def format_m3u8_list(data):
    if isinstance(data,dict):
        logger.info(f"当前数据为{data}")       
        m3u8s = list(data.items()) 
        logger.info("正在转换成列表-元组序列{}".format(m3u8s))
        return m3u8s
        
def check(setting,key):
    if key == 'PROXY_SET':
        logger.info("检测代理设置选项")
        value = setting.__getitem__(key)
        return proxy_pool()
        
def init_proxy(settings,prefix,after):
    prefix['http'] = prefix['http'].format(key=settings['KEY_PROXY'],pd =settings['PD_PROXY'] ,ip=after)
    prefix['https'] = prefix['https'].format(key=settings['KEY_PROXY'],pd =settings['PD_PROXY'] ,ip=after)
    return prefix
