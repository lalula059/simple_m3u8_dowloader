"""多线程和多协程比较测试"""
import asyncio
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time
# def shuchu():
#     time.sleep(1)
#     print(2)
#     return 
# if __name__ == "__main__":
#     x= time.time()
#     ths = []
#     for _ in range(0,10000):
#         th = Thread(target=shuchu)
#         th.start()
#         ths.append(th)
#     for temp in ths:
#         temp.join()        
#     y = time.time()
#     print("总时间未{}".format(y-x))
"""4.650296926498413"""
# def shuchu(x):
#     print(2)
#     return 'niuibi'

# if __name__ == "__main__":
#     x = time.time()
#     ths = []
#     with ThreadPoolExecutor(max_workers=5000) as executor:
#         for data in executor.map(shuchu, range(10000)):  # 指定迭代范围
#             print(data)
#     y = time.time()
#     print("总时间为{}".format(y-x))

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Util.Padding import pad, unpad

# # 加密函数

# # 解密函数
# def decrypt(key, data,iv):
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     pt = unpad(cipher.decrypt(data), AES.block_size)
#     return pt

# # 测试函数
# def main():
#     with open('af_Key.txt','+rb') as f:
#         key = f.read()
#     with open('iv.txt','+rb') as f:
#         iv = f.read().decode('utf-8')[:AES.block_size].encode('utf-8')
#     with open('ceshi.txt','+rb') as f:
#         data = f.read()
#     decrypted_data = decrypt(key, data,iv)
#     with open("1.ts",'wb') as f:
#         f.write(decrypted_data)
#     print("Decrypted:", decrypted_data)

# if __name__ == "__main__":
#     main()

""""""
# async def shuchu():
#     await asyncio.sleep(1)
#     print(2)
#     return 
# async def main():
#     tasks = [asyncio.create_task(shuchu()) for _ in range(0,10000)]
#     await asyncio.gather(*tasks)
# if __name__ == "__main__":
#     x = time.time()
#     asyncio.run(main())
#     y = time.time()     
#     print("总时间未{}".format(y-x))
"""总时间未1.1242480278015137  总结，在io任务数量很多的时候，协程要比线程池快"""

"""设置nametuple存储视频数据"""
# from collections import namedtuple
# M3u8_list = namedtuple('M3u8_list',['name','first_m3u8','second_m3u8','fi_content','second_content','is_get_second','proxy'],defaults=[None,None,None,None,None,"NO",None])
# m3u8_first = M3u8_list(name='哥布林杀手',first_m3u8='asd',is_get_second='no')
# m3u8_first = m3u8_first._replace(is_get_second = 'YES')
# print(m3u8_first)
# __KEYWORDS__ = [
#     'name',
#     'First_m3u8',
#     'Second_m3u8',
#     'First_m3u8_content',
#     'Second_m3u8_content',
#     'tags'
# ]
# M3U8_List1 = namedtuple('M3U8_List1',__KEYWORDS__,defaults=[None for i in __KEYWORDS__])

"""练习mongodb存储"""
import pymongo
# default_client = pymongo.MongoClient()
# new_database = default_client['test']
# new_col = new_database['first']
# new_col.insert_one({'a':'s','b':'d'})
# """练习存储nametuple"""
# new_col.insert_one(m3u8_first._asdict())

# dbs = pymongo.MongoClient()
# db = dbs['M3U8_LIST']
# col  = db['FIRST'] 
# res = col.find({'name':{'$regex':'.*'}})
# for i in res:
#     print(i['name'])
    
# class A:
#     def __init__(self) -> None:
#         self.x = False

"""练习多进程"""
# import multiprocessing
# def add(x):
#     time.sleep(2)
    
#     for i in x:
#         print(i*i)
# ty = [1,2,3,4,5]
# tr= [5,5,5,5,5]
# temp = []
# if __name__ == '__main__':
#     pr1 = multiprocessing.Process(target=add,args=(tr,))
#     pr2 = multiprocessing.Process(target=add,args=(ty,))
#     pr1.start()
#     pr2.start()

#     pr1.join()
#     pr2.join()


import requests
x = '123123'
print(x[-2:])
resp = requests.get('https://jpzy01.com/20240812/XaIDhjOt/800kb/hls/OBo0czj4.jpg')
with open('1.ts','+wb') as f:
    f.write(resp.content)