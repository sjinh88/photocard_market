from .base import *

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "photomarket",  # 데이터베이스 이름
        "USER": "photomarket",  # 데이터베이스 사용자 이름
        "PASSWORD": "photomarket",  # 데이터베이스 비밀번호
        "HOST": "market_db",  # 데이터베이스 호스트
        "PORT": "3306",  # MySQL 포트 (기본값: 3306)
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",  # MySQL 5.7에 적합한 모드 설정
            "charset": "utf8mb4",
        },
    }
}
