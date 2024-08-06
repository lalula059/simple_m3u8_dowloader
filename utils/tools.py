from Logging.logg_create import logger
from Proxy.pool_get import proxy_pool
from collections import namedtuple
import base64
from Downloader.subthread import No_AThread,EX_AThread
import os
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



def AES_handler(data,settings):
    # 此方法分出创造哪个类，是AES请求的子类或者是原部分的子类
    logger.info("正在检测AES关键词")
    import re
    patterns = re.compile('EXT.*?(METHOD.*)')
    AES_KEY_WORD = patterns.findall(data.get('Second_m3u8_content'),re.M)
    if AES_KEY_WORD:
        # 取后缀，改后缀
        patterns_pre = re.compile(r'\w+.m3u8')
        aft = patterns_pre.findall(data.get('Second_m3u8'))[0]
        # 固定了加密字段网页，且取后面URI关键字段
        AES_KEY_THREE = AES_KEY_WORD[0].split(',')
        AES_KEY_URL = data.get('Second_m3u8').replace(aft,AES_KEY_THREE[1].split('=')[1][1:-1])
        logger.info(f"检测到关键字{AES_KEY_WORD}")
        # 添加匹配到的关键字段
        data.__setitem__('AES_KEY_WORDS',AES_KEY_THREE)
        data.__setitem__('AES_URL',AES_KEY_URL)
        return EX_AThread(data,settings=settings)
    else:
        return No_AThread(data,settings=settings)

# 需要一个字典来存储对应的名字，因为每个链接都不能有中文
def merge():
    logger.info("正在合并视频文件")
    # 设置根目录
    _movie_root__path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))+'\\Movies'
    # 创建一个额外文件存储保存的txt文件以及合并后的ts文件
    movie_list = _movie_root__path+'\\movielist'
    if not os.path.exists(movie_list):
        os.mkdir(movie_list)
    # 遍历每一个目录
    for name in os.listdir(_movie_root__path):
        _movie_name_path = _movie_root__path +'\\'+ name
        # 拼接ts文件这样写入到txt文件中
        if name != 'movielist':
            # 将字符串变成数字，好排序
            sorted_list = [int(i.split('.')[0]) for i in os.listdir(_movie_name_path)]
            
            _movie_list_path = [_movie_name_path +'\\' + str(i) + '.ts' for i in sorted(sorted_list)]
            # order = '|'.join(_movie_list_path)
            for item in _movie_list_path:
                with open(movie_list + f'\\{name}.txt','a') as f:
                    f.write(f'file \'{item}\'')
                    f.write('\n')
        
        # 执行合并操作
            os.popen(f'ffmpeg -f concat -safe 0 -i  {movie_list + f'\\{name}.txt'} -c copy E://movie//{''.join((base64.b64decode(name.replace('BOOM','/')).decode('utf-8')).split(' '))}.mkv')