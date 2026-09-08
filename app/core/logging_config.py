import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = str(Path(__file__).resolve().parent.parent.parent / "logs")
os.makedirs(LOG_DIR, exist_ok = True) # 确保日志目录存在

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" # 日志格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S" # 日期格式

def setup_logging():
    """初始化日志配置 （控制台 + 滚动文件）"""
    logger = logging.getLogger() # 获取根日志器
    logger.setLevel(logging.INFO) # 设置日志级别为INFO

    # 避免重复添加 Handler（例如热重载时）
    if logger.handlers:
        return

    # 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(console_handler)

    # 滚动文件 Handler
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR,"app.log"),
        maxBytes= 10 * 1024 * 1024, # 10MB
        backupCount=5, # 保留5个备份文件
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)