### Bitech Backend

### Технологии

#### Основные технологии:

- postgresql
- minio
- mongodb
- docker
- python 3.10
- FastAPI
- ormar
- pydantic
- yagpt

#### Библиотеки

```txt
aiohttp==3.9.5
aiosignal==1.3.1
alembic==1.13.1
anyio==3.7.1
async-timeout==4.0.3
asyncpg==0.27.0
attrs==23.2.0
bcrypt==4.1.2
certifi==2024.2.2
cffi==1.16.0
cfgv==3.4.0
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
cryptography==42.0.5
databases==0.6.2
decorator==5.1.1
defusedxml==0.7.1
Deprecated==1.2.14
distlib==0.3.8
distro==1.9.0
dnspython==2.6.1
docx2txt==0.8
ecdsa==0.19.0
exceptiongroup==1.2.0
fastapi==0.110.1
filelock==3.13.3
frozenlist==1.4.1
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
identify==2.5.35
idna==3.6
iniconfig==2.0.0
Mako==1.3.2
MarkupSafe==2.1.5
motor==3.4.0
multidict==6.0.5
netaddr==1.2.1
nodeenv==1.8.0
odfpy==1.4.1
ormar==0.12.2
packaging==24.0
passlib==1.7.4
platformdirs==4.2.0
pluggy==1.4.0
pre-commit==3.7.0
prometheus-fastapi-instrumentator==7.0.0
prometheus_client==0.20.0
psycopg2-binary==2.9.9
py==1.11.0
pyasn1==0.6.0
pycparser==2.22
pydantic==1.10.8
PyJWT==2.8.0
pymongo==4.7.2
PyPDF2==3.0.1
pytest==7.4.3
pytest-asyncio==0.21.1
python-dotenv==1.0.1
python-jose==3.3.0
python-magic==0.4.15
python-multipart==0.0.9
PyYAML==6.0.1
requests==2.31.0
retry==0.9.2
rsa==4.9
six==1.16.0
sniffio==1.3.1
SQLAlchemy==1.4.41
starlette==0.37.2
striprtf==0.0.26
tomli==2.0.1
typing_extensions==4.10.0
urllib3==2.2.1
uvicorn==0.29.0
virtualenv==20.25.1
wrapt==1.16.0
yarl==1.9.4
```

### Запуск локально

1. Отредактируйте .env

```txt
MONGODB_URL - url для подключения
SECRET_KEY - сикретный ключь для jwt
MINIO_ENDPOINT_URL - ссылка н minio
S3_WORKER_API - ссылка на s3_worker
YAGPT_KEY - ключь YAGPT
YAGPT_MODEL_URI - YAGPT URL
MINIO_ADDRESS - ссылка н minio
```

2. Запустить docker

```shell
docker compose --env-file .env -f docker-compose.yml up --build
```

3. После запуска api будет доступно по
   адресу [`http://localhost:8078`](http://localhost:8078) ([swagger](http://localhost:8078/docs))

### Архитектура

В проекте используется луковая архитектура
![img.png](img.png)

Для хранения данных используется minio s3, postgresql 14, mongodb 6. Для распознавания
данных резюме используется YandexGPT. Для миграций используется alembic. 
