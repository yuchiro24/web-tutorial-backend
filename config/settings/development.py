from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # MySQLの設定
        'NAME': 'app',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '53306',
        # Dockerコンテナからホストを参照する
        'HOST': 'host.docker.internal',
        # データベースの接続を永続化する。処理が成功した場合のみ変更が反映される。
        'ATOMIC_REQUESTS': True,
    }
}