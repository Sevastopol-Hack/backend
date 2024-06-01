import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from passlib.context import CryptContext
from yookassa import Configuration

load_dotenv()

METRICS = os.environ.get("METRICS", "") == "true"

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

PRODUCTION = os.environ.get("PRODUCTION") == "true"

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# S3
MINIO_ADDRESS = os.environ.get("MINIO_ADDRESS")
S3_WORKER_API = os.environ.get("S3_WORKER_API")
BUCKET_NAME = "biwork"

# YOOKASSA

YAGPT_KEY = os.environ.get("YAGPT_KEY")
YAGPT_MODEL_URI = os.environ.get("YAGPT_MODEL_URI")

MONGODB_URL = os.environ.get("MONGODB_URL")

ds_keyword = [
    "tensorflow",
    "keras",
    "pytorch",
    "machine learning",
    "deep Learning",
    "flask",
    "streamlit",
]
web_keyword = [
    "react",
    "django",
    "node jS",
    "react js",
    "php",
    "laravel",
    "magento",
    "wordpress",
    "javascript",
    "angular js",
    "C#",
    "Asp.net",
    "flask",
]
android_keyword = ["android", "android development", "flutter", "kotlin", "xml", "kivy"]
ios_keyword = ["ios", "ios development", "swift", "cocoa", "cocoa touch", "xcode"]
uiux_keyword = [
    "ux",
    "adobe xd",
    "figma",
    "zeplin",
    "balsamiq",
    "ui",
    "prototyping",
    "wireframes",
    "storyframes",
    "adobe photoshop",
    "photoshop",
    "editing",
    "adobe illustrator",
    "illustrator",
    "adobe after effects",
    "after effects",
    "adobe premier pro",
    "premier pro",
    "adobe indesign",
    "indesign",
    "wireframe",
    "solid",
    "grasp",
    "user research",
    "user experience",
]

systems_analyst = [
    "knowledge modeling language",
    "knowledge representation and reasoning",
    "axure rp",
    "mockflow",
    "invision",
    "balsamiq",
    "sparx enterprise architect",
    "ibm rational rose",
    "visual paradigm",
    "ibm doors",
    "jira",
    "tfs",
    "microsoft power bi",
    "tableau",
    "qlikview",
    "selenium",
    "apache jmeter",
    "hp loadrunner",
    "microsoft word",
    "google docs",
    "confluence",
    "slack",
    "microsoft teams",
    "trello",
]

DEFAULT_STACKS = (
    ds_keyword
    + web_keyword
    + android_keyword
    + ios_keyword
    + uiux_keyword
    + systems_analyst
)

# LOGGING
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s | %(name)s | %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s | %(name)s | %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            # noqa: E501
        },
        "my_formatter": {
            "()": "logging.Formatter",
            "fmt": "%(asctime)s | %(name)s | %(levelname)-8s | [%(pathname)s:%(lineno)d] | %(message)s",
        },
    },
    "handlers": {
        "my_handler": {
            "formatter": "my_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {"handlers": ["my_handler"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
