from starlette.config import Config

config = Config('.env')
FRONTEND_URL = config('FRONTEND_URL')
POSTGRES_URL = config('POSTGRES_URL')
SECRET_KEY = config('SECRET_KEY')
BASE_URL = config.get('BASE_URL')
GOOGLE_CLIENT_ID = config.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config.get('GOOGLE_CLIENT_SECRET')
NAVER_CLIENT_ID = config.get('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config.get('NAVER_CLIENT_SECRET')
GITHUB_CLIENT_ID = config.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = config.get('GITHUB_CLIENT_SECRET')
IS_PRODUCTION = config('IS_PRODUCTION', cast=bool, default=False)
