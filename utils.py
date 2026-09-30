"""
=========================================================
ECHO v0.1 - utils.py
=========================================================
This file contains small REUSABLE helper functions that
are used by many other modules (memory.py, notes.py,
tasks.py, etc.)

Keeping them here avoids repeating the same code again
and again in every module (this is called "DRY" -
"Don't Repeat Yourself").
=========================================================
"""

import json
import os


# ---------------------------------------------------------
# JSON LOAD / SAVE HELPERS
# ---------------------------------------------------------

def load_json(file_path, default_data):
    """
    Reads a JSON file and returns its content as a Python
    dictionary/list.

    file_path    -> path of the .json file to read
    default_data -> what to return if the file does not
                    exist yet, or is empty/corrupted

    This function is "safe" - it will never crash the app
    even if the file is missing or damaged.
    """
    # If the file doesn't exist yet, just return the default
    if not os.path.exists(file_path):
        return default_data

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # If the file is empty, return default data
            if not content:
                return default_data

            return json.loads(content)

    except (json.JSONDecodeError, OSError):
        # File is corrupted or unreadable - fall back safely
        print("⚠ Warning: Could not read", file_path, "- using default data.")
        return default_data


def save_json(file_path, data):
    """
    Saves a Python dictionary/list into a JSON file.

    file_path -> path of the .json file to write to
    data      -> the Python data (dict/list) to save

    indent=4 makes the JSON file human-readable if you
    ever open it manually.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("⚠ Error: Could not save data to", file_path)
        return False


# ---------------------------------------------------------
# SCREEN / DISPLAY HELPERS
# ---------------------------------------------------------

def clear_screen():
    """
    Clears the terminal screen.
    Works on both Windows ('cls') and Linux/Android ('clear'),
    which makes it Pydroid 3 friendly.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    """
    Prints a nice, consistent header/banner for any menu.

    Example:
    ============================
             MEMORY MENU
    ============================
    """
    line = "=" * 30
    print(line)
    print(title.center(30))
    print(line)


def press_enter_to_continue():
    """
    Pauses the program until the user presses Enter.
    Useful after showing a result, before going back to a menu.
    """
    input("\nPress Enter to continue...")


# ---------------------------------------------------------
# INPUT HELPERS
# ---------------------------------------------------------

def get_nonempty_input(prompt):
    """
    Keeps asking the user for input until they type
    something that is NOT empty (i.e. not just spaces).

    This avoids saving blank notes, blank tasks, etc.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("⚠ This field cannot be empty. Please try again.")


def get_menu_choice(prompt, valid_choices):
    """
    Asks the user to enter a menu choice and keeps asking
    until the input matches one of the valid_choices.

    prompt        -> text to show the user
    valid_choices -> list of allowed strings, e.g. ["1","2","3"]
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("⚠ Invalid choice. Please try again.")


def get_yes_no(prompt):
    """
    Asks a Yes/No question and returns True for yes,
    False for no. Accepts y/n/yes/no (any case).
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        print("⚠ Please answer with y/n.")


def get_next_id(items):
    """
    Generates the next unique ID for a list of dictionary
    items, where each item has an "id" key.

    Example: if items already have ids 1, 2, 3 -> returns 4
    If the list is empty -> returns 1

    This is used by notes, tasks, reminders, memory, etc.
    so every entry gets a unique number.
    """
    if not items:
        return 1
    return max(item["id"] for item in items) + 1
    