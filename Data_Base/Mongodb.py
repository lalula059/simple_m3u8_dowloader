import pymongo
from Logging.logg_create import logger
import pymongo.mongo_client

class Mongodb:
    def __init__(self,settings) -> None:
        self.dbs = pymongo.MongoClient()
        self.setting = settings
        self.db = self.dbs[self.setting.__getitem__('MONGODB_DATABAS')]
        self.col  = self.db[self.setting.__getitem__('MONGODB_COL')] 
    def save(self,data,index):
        if self.col.find_one({'name':{'$regex':data['name']}}):
            logger.info("此数据已经存在，返回数据")
            return
        data['index'] = index
        self.col.insert_one(data)
    def get_all(self):
        return self._get_all()
    def _get_all(self):
        data = self.col.find({'name':{'$regex':'.*'}})
        return iter(data)