import os

# need checked project's root dir
ROOT_DIR = ""

# if you want to shorter print path in output, can set
# this same as ROOT_DIR
IGNORE_PATH_PREFIX = ROOT_DIR

# if you confirm some module will never hotfix, put them here
IGNORE_MODULE = [
    # project_name.const_define,
]

# if you don't want to check some files or directories
# put them here using absolute path
IGNORE_PATH = [
    # "/absolute/path/to/project_name/test",
]

if not ROOT_DIR.endswith("/"):
    ROOT_DIR += "/"
if not IGNORE_PATH_PREFIX.endswith("/"):
    IGNORE_PATH_PREFIX += "/"