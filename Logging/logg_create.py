import logging
from pathlib import Path
from os.path import abspath
def get_logger():
    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(filename)s------%(lineno)s\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # 创建流方式处理器
        strean_handler = logging.StreamHandler()
        strean_handler.setFormatter(formatter)
        #给日志文件创建路径    
        log_path = (Path(abspath(__file__)).parent / '程序日志.log')
        log_path.open('w')
        file_hadler = logging.FileHandler(log_path)

        file_hadler.setFormatter(formatter)
        
        logger.addHandler(strean_handler)
        logger.addHandler(file_hadler)
        return logger
    else:
        return logger
logger = get_logger()