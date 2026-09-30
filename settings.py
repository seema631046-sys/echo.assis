"""
settings.py
-----------
Settings module for ECHO v0.1.

Stores user_name, nickname, assistant_name, and version in
data/settings.json. Falls back to config.DEFAULT_SETTINGS the
first time the app runs (file does not exist yet).
"""

from config import SETTINGS_FILE, DEFAULT_SETTINGS
from utils import (
    load_json,
    save_json,
    clear_screen,
    print_header,
    press_enter_to_continue,
    get_nonempty_input,
    get_menu_choice,
    get_yes_no,
)


def _load_settings():
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())


def _save_settings(data):
    save_json(SETTINGS_FILE, data)


def view_settings():
    clear_screen()
    print_header("CURRENT SETTINGS")

    settings = _load_settings()
    print(f"User Name       : {settings['user_name']}")
    print(f"Nickname        : {settings['nickname']}")
    print(f"Assistant Name  : {settings['assistant_name']}")
    print(f"Version         : {settings['version']}")

    press_enter_to_continue()


def change_user_name():
    clear_screen()
    print_header("CHANGE USER NAME")

    settings = _load_settings()
    print(f"Current user name: {settings['user_name']}")

    settings["user_name"] = get_nonempty_input("New user name: ")
    _save_settings(settings)

    print("\n✅ User name updated!")
    press_enter_to_continue()


def change_nickname():
    clear_screen()
    print_header("CHANGE NICKNAME")

    settings = _load_settings()
    print(f"Current nickname: {settings['nickname']}")

    settings["nickname"] = get_nonempty_input("New nickname: ")
    _save_settings(settings)

    print("\n✅ Nickname updated!")
    press_enter_to_continue()


def change_assistant_name():
    clear_screen()
    print_header("CHANGE ASSISTANT NAME")

    settings = _load_settings()
    print(f"Current assistant name: {settings['assistant_name']}")

    settings["assistant_name"] = get_nonempty_input("New assistant name: ")
    _save_settings(settings)

    print("\n✅ Assistant name updated!")
    press_enter_to_continue()


def change_version():
    clear_screen()
    print_header("CHANGE VERSION")

    settings = _load_settings()
    print(f"Current version: {settings['version']}")

    settings["version"] = get_nonempty_input("New version: ")
    _save_settings(settings)

    print("\n✅ Version updated!")
    press_enter_to_continue()


def reset_settings():
    clear_screen()
    print_header("RESET SETTINGS")

    if get_yes_no("Reset all settings to default values? (y/n): "):
        _save_settings(DEFAULT_SETTINGS.copy())
        print("\n✅ Settings reset to default.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def settings_menu():
    while True:
        clear_screen()
        print_header("SETTINGS MENU")
        print("1. View Settings")
        print("2. Change User Name")
        print("3. Change Nickname")
        print("4. Change Assistant Name")
        print("5. Change Version")
        print("6. Reset to Default")
        print("7. Back to Main Menu")

        choice = get_menu_choice(
            "Enter choice (1-7): ",
            ["1", "2", "3", "4", "5", "6", "7"],
        )

        if choice == "1":
            view_settings()
        elif choice == "2":
            change_user_name()
        elif choice == "3":
            change_nickname()
        elif choice == "4":
            change_assistant_name()
        elif choice == "5":
            change_version()
        elif choice == "6":
            reset_settings()
        elif choice == "7":
            break
            