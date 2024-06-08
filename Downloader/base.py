from Logging.logg_create import logger
from utils.tools import init_proxy
import asyncio
import aiohttp
import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
"""此文件作为请求的基础文件"""
"""class Async_req:
    def __init__(self,settings = None,vendor = None,ts_list = None) -> None:
        self.settings = settings
        self.vendor = vendor
        self.ts_list = ts_list
        self.tasks = None
        self.proxies = None
        self.Semph = asyncio.Semaphore(self.settings.__getitem__('ASEMAPHORE'))
        # 注意要加锁
        self.event_loop = asyncio.new_event_loop()
        self.session = None
    def _req_get_proxy(self):
        pass
    async def _req_pre(self,item,session):
        temp_p = {
            'http':'http://{}',
            'https':'https://{}',
        }
        async with self.Semph:
            try:
                temp_proxy = self.proxies.get()
                prox = init_proxy(temp_p,temp_proxy)
                logger.debug("检测是否得到代理{}".format(prox))
                # ss = requests.get(url = "https://httpbin.org/ip",proxies=prox,verify=False)
                # logger.debug(f'检测request库是否可以使用代理{ss.text}')
                async with session.get(url = "https://httpbin.org/ip",headers = self.settings.__getitem__('HEADERS'),proxy = prox['https'],ssl=False) as resp:
                    text = await resp.read()
                    logger.info(f"成功完成请求任务{text}")
            except Exception as e:
                logger.error(f"未知错误----{e}")
                await asyncio.sleep(random.uniform(0.1, 0.5))
                return await self._req_pre(item,session)
                # 如果在这里用递归地话，信号量还是会减少，他始终切换不到下一个任务去

                
    # async def test(self):
    #     async with self.Semph:
    #         await self.lock.acquire()
    #         global i
    #         i+=1
    #         t =2 
    #         t+=1
    #         await asyncio.sleep(1)
    #         print(f'{i}        {t}')
    #         self.lock.release()

    async def run(self):
        con  = aiohttp.TCPConnector(ssl=False)
        session = aiohttp.ClientSession(connector=con,trust_env=True,timeout=aiohttp.ClientTimeout(total=5))
        temp_tasks = []
        for item in self.tasks:
            temp_task = asyncio.create_task(self._req_pre(item,session))
            temp_tasks.append(temp_task)
        try:
            await asyncio.gather(*temp_tasks)
            await session.close()
        except Exception as e:
            
            logger.error(f"出错了{e}")

    def start(self,tasks,proxy = None):
        # 注意，传递进来的任务是这个样子(('名字','url'),('名字','url'))
        asyncio.set_event_loop(self.event_loop)
        self.tasks = tasks
        self.proxies = proxy
        self.event_loop.run_until_complete(self.run())
        """

class multi_Thread:
    def __init__(self,settings = None,vendor = None,ts_list = None,NUMBER_STR = None) -> None:
        self.settings = settings
        self.vendor = vendor
        self.ts_list = ts_list
        self.tasks = None
        self.proxies = None
        self.retry_time = self.settings['RETRY']
        # 传递的NUMBER_STR = None这个值是你在config里面设置的并发数量
        self.executor = ThreadPoolExecutor(max_workers=self.settings[NUMBER_STR])
        logger.info("得到的并发数设置为{}".format(self.settings[NUMBER_STR]))
        
    def start(self,tasks,proxy = None):
        # 注意，传递进来的任务是这个样子(('名字','url'),('名字','url'))
        self.tasks = tasks
        self.proxies = proxy
        res = self._req_start()
        return res
    def _req_start(self):
        temp_data = []
        for data in self.executor.map(self._req_run, self.tasks):
            logger.info(f"当前任务完成了结果为--------{data}")
            temp_data.append(data)
        logger.debug("测试列表是否添加完成值{}".format(temp_data))
        return temp_data

    # 通过判断设置是否使用代理
    def check_without_proxy(self,tasks_name):
        # logger.info(f"检测check_without_proxy{tasks_name}")
        # import sys
        # sys.exit()
        get_proxy_open = self.settings.get('PROXY_SET')
        try:
            i = 0  # 初始化重试计数器
            while True:
                prox = self.get_proxy()
                try:
                    # get_proxy_open = self.settings.get('PROXY_SET')
                    # import sys
                    # sys.exit()
                    if get_proxy_open:
                        logger.info(f"当前使用代理为{prox}")
                        resp = requests.get(url=self.tasks[tasks_name],headers=self.settings['HEADERS'],proxies=prox)
                        # resp = requests.get(url='https://httpbin.org/ip', headers=self.settings['HEADERS'], proxies=prox, timeout=self.settings['TIMEOUT'])
                        if resp.status_code ==200:
                            return (tasks_name,resp)
                        else:
                            logger.error(f"网络访问错误，请检查是否关闭了代理{prox}")
                            return (tasks_name,self.tasks[tasks_name])
                        
                    elif get_proxy_open is False:
                        logger.info(f"代理未设置以下任务{tasks_name}未使用代理")
                        resp = requests.get(url=self.tasks[tasks_name],headers=self.settings['HEADERS'])

                        # resp = requests.get(url='https://httpbin.org/ip', headers=self.settings['HEADERS'])
                        if resp.status_code ==200:
                            return (tasks_name,resp)
                        else:
                            logger.error(f"网络访问错误，请检查是否关闭了代理,{prox}")
                            return (tasks_name,self.tasks[tasks_name])
                except Exception as e:
                    logger.error(f"出现网络链接错误----{e}")
                    if get_proxy_open:
                        self.proxies.delete(prox)
                    i += 1
                    logger.info(f"重试{i}次")
                    if i > self.retry_time:
                        logger.debug("尝试次数大于设置，正在取消代理请求尝试中")
                        # 第三次不成功的话直接不使用代理尝试
                        resp = requests.get(url=self.tasks[tasks_name],headers=self.settings['HEADERS'])
                        logger.error(f"检测是否正确{self.tasks[tasks_name]}")
                        # resp = requests.get(url='https://httpbin.org/ip', headers=self.settings['HEADERS'],timeout=self.settings['TIMEOUT'])
                        if resp.status_code ==200:
                            return (tasks_name,resp)
                        else:
                            logger.error(f"网络访问错误，请检查是否关闭了代理{prox}")
                            return (tasks_name,self.tasks[tasks_name])
        except Exception as e:
            logger.error(f"出现未处理的异常----{e}")
            if i > self.retry_time:
                return (tasks_name,self.tasks[tasks_name])
            

    def _req_run(self,tasks_name):
        logger.info(f"当前任务为----{tasks_name}")
        try:
            resp = self.check_without_proxy(tasks_name)
        except UnboundLocalError as e:
            logger.error(f"数据未成功得到----{e}")
        # 检查是否传输的失败的列表还是成功的列表
        return resp

    def get_proxy(self):
        temp_p = {
            'http':'http://{key}:{pd}@{ip}',
            'https':'http://{key}:{pd}@{ip}',
        }
        try:
            temp_proxy = self.proxies.get()
            if not temp_proxy:
                return None
            # 通过setting里面的账号密码选项进行验证，初始化代理
            prox = init_proxy(self.settings,temp_p,temp_proxy)
            logger.debug("检测是否得到代理{}".format(prox))
        except Exception as e:
            logger.error(f"原来tm的是代理出问题了{e}")
        return prox