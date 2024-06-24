import logging
from datetime import date
import os
import setting

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

log_dir_path = os.path.join(setting.BASE_DIR, 'logs')
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

date_today = date.today()
file_name = "log_" + date_today.__str__() + ".log"

log_file_path = os.path.join(log_dir_path, file_name)
file_handler = logging.FileHandler(log_file_path)

file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
