from Logging.logg_create import logger
from Data_Base.Mongodb import Mongodb
from collections import namedtuple
def save_Data_handler(data,settings):
    
    if settings.__getitem__('MONGODB_SAVE'):
        logger.info("存储数据在mongodb中")
        mongo = Mongodb(settings=settings)
        for item in data:
            mongo.save(item._asdict())
    if settings.__getitem__('CSV_SAVE'):
        logger.info("存储数据中2")