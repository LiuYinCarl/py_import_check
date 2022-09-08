import os

DJANGO_DIR =  os.path.join(os.getcwd(), "django")

ROOT_DIR = DJANGO_DIR

IGNORE_PATH_PREFIX = DJANGO_DIR

IGNORE_MODULE = []

IGNORE_PATH = [
    os.path.join(DJANGO_DIR, "/django/test")
]

if not ROOT_DIR.endswith("/"):
    ROOT_DIR += "/"
if not IGNORE_PATH_PREFIX.endswith("/"):
    IGNORE_PATH_PREFIX += "/"