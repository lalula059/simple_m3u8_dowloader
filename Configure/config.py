# 设置代理及验证账号密码
PROXY_SET =False
KEY_PROXY = 13388221448
PD_PROXY = 'KAOuSIYn'
# 并发线程池数量设置
THREADNUMBER_M3U8 = 20
THREADNUMBER_TS = 2000
# redis 和 mongodb设置
MONGODB_SAVE = True
MONGODB_DATABAS = 'M3U8_LIST'
MONGODB_COL = 'FIRST'

CSV_SAVE = False


# 网站和名字设置
INDEX_URL = {"真人娃娃的目的":'https://yzzy.play-cdn22.com/20240323/210_f75cd762/2000k/hls/mixed.m3u8',
            'MegaloBox第一集':'https://cdn15.yzzy-tv-cdn.com/20230406/6535_889455b6/2000k/hls/index.m3u8' }
# 请求头设置
HEADERS = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer':'https://jx.ijujitv.cc/'}

# 设置链接超时选项
TIMEOUT = 10
# 设置重试次数
RETRY = 3
# 设置是否存储视频时设置tag
# 注意如果设置了tag,存入的网站和名字应该是INDEX_URL = {"哥布林杀手_(动漫_等等)":'https://yzzy.play-cdn22.com/20240323/210_f75cd762/2000k/hls/mixed.m3u8',}
# 用下划线分开系统会根据传入的名字参数进行对应的nametuple创建
TAGS = False

