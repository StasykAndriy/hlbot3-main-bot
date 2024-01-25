TOKEN = "6718793281:AAE251kBRl_G9K7EKt6upyZPXQ3tr-dwbR8"


import os
from gino import Gino
from dotenv import load_dotenv


db = Gino()
load_dotenv()
app_prefix = str(os.getenv('APP_PREFIX'))

admin_id = 5763984902


PG_IP = str(os.getenv('PG_IP'))
PG_DATABASE = str(os.getenv('PG_DATABASE'))
PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))

POSTGRES_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_IP}/{PG_DATABASE}"