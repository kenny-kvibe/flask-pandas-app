import dotenv
import os
import sys


ROOT_PATH = os.path.dirname(__file__)

FLASK_STATIC_DIR_PATH    = os.path.join(ROOT_PATH, 'static')
FLASK_TEMPLATES_DIR_PATH = os.path.join(ROOT_PATH, 'templates')

if ROOT_PATH not in sys.path:
	sys.path.insert(0, ROOT_PATH)

dotenv.load_dotenv()

DEV_MODE = os.environ.get('DEV_MODE', '').lower() in ('1', 'true')

