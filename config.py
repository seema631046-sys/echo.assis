"""
=========================================================
ECHO v0.1 - config.py
=========================================================
This file stores all the FIXED settings and FILE PATHS
used by the whole ECHO project.

Why a separate config file?
- So that if we ever need to change a file name or folder
  location, we only change it HERE, in one place, instead
  of hunting through every module.

This file does NOT contain any logic (functions/menus).
It only contains constants (fixed values).
=========================================================
"""

import os

# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------
# This finds the folder where THIS config.py file is saved.
# That way, ECHO works no matter where the "astra" folder
# is placed on your phone (Pydroid 3 friendly).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# DATA FOLDER
# ---------------------------------------------------------
# All JSON files (our "database") live inside this folder.
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------------------------------------------------------
# INDIVIDUAL JSON FILE PATHS
# ---------------------------------------------------------
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")
STUDY_FILE = os.path.join(DATA_DIR, "study.json")
RESEARCH_FILE = os.path.join(DATA_DIR, "research.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# ---------------------------------------------------------
# DEFAULT SETTINGS
# ---------------------------------------------------------
# These values are used ONLY the very first time ECHO runs,
# i.e. when settings.json does not exist yet.
DEFAULT_SETTINGS = {
    "user_name": "Seema Sahu",
    "nickname": "Aayo",
    "assistant_name": "ECHO",
    "version": "0.1"
}

# ---------------------------------------------------------
# APP INFO
# ---------------------------------------------------------
APP_NAME = "ECHO"
APP_VERSION = "0.1"
DEVELOPER_NAME = "Seema Sahu"
COLLEGE_NAME = "Shri Shankaracharya Technical Campus (SSTC), Bhilai"


def ensure_data_folder_exists():
    """
    Makes sure the 'data' folder exists.
    If it doesn't exist, this function creates it.

    We call this once when ECHO starts (from main.py),
    so that every module can safely read/write JSON files
    without worrying about missing folders.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        