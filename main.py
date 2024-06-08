from Core.excute import excute
import time
from Logging.logg_create import logger

if __name__ == '__main__':
    x  = time.time()
    excute()
    y  = time.time()
    logger.info(f"*****************总计花费时间为{y-x}*****************")