import os
from dotenv import load_dotenv

load_dotenv()

bind = f'0.0.0.0:{os.getenv("PORT", 8000)}'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = int(os.getenv('WORKER_NUM', 4))
log_level = os.getenv('LOG_LEVEL', 'INFO')
