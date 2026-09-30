"""
main.py
-------
Entry point for ECHO v0.1. Displays the startup banner and
routes main menu choices to each module's own menu function.
"""

import config
import utils
from memory import memory_menu
from notes import notes_menu
from tasks import tasks_menu
from reminders import reminders_menu
from study import study_menu
from research import research_menu
from settings import settings_menu


def _get_settings():
    return utils.load_json(config.SETTINGS_FILE, config.DEFAULT_SETTINGS.copy())


def print_banner():
    settings = _get_settings()
    print("=" * 42)
    print("ECHO v0.1")
    print("Personal AI Assistant")
    print()
    print("Developer:")
    print(config.DEVELOPER_NAME)
    print()
    print("College:")
    print(config.COLLEGE_NAME)
    print()
    print("Platform:")
    print("Python 3.11")
    print("Pydroid 3")
    print()
    print("Status:")
    print("System Ready")
    print("=" * 42)
    print(f"\nWelcome, {settings['nickname']}!\n")


def print_main_menu():
    print("Main Menu\n")
    print("1. Dashboard")
    print("2. Memory")
    print("3. Notes")
    print("4. Tasks")
    print("5. Reminders")
    print("6. Study Planner")
    print("7. Research")
    print("8. Settings")
    print("9. About ECHO")
    print("0. Exit")


def dashboard():
    """Quick read-only summary pulled from each module's JSON file."""
    utils.clear_screen()
    utils.print_header("DASHBOARD")

    memory_data = utils.load_json(config.MEMORY_FILE, {"memories": []})
    notes_data = utils.load_json(config.NOTES_FILE, {"notes": []})
    tasks_data = utils.load_json(config.TASKS_FILE, {"tasks": []})
    reminders_data = utils.load_json(config.REMINDERS_FILE, {"reminders": []})
    study_data = utils.load_json(config.STUDY_FILE, {"subjects": []})
    research_data = utils.load_json(config.RESEARCH_FILE, {"ideas": []})

    pending_tasks = sum(1 for t in tasks_data["tasks"] if not t["completed"])
    completed_tasks = sum(1 for t in tasks_data["tasks"] if t["completed"])
    pending_reminders = sum(1 for r in reminders_data["reminders"] if not r["done"])

    print(f"Memories saved      : {len(memory_data['memories'])}")
    print(f"Notes saved         : {len(notes_data['notes'])}")
    print(f"Tasks pending       : {pending_tasks}")
    print(f"Tasks completed     : {completed_tasks}")
    print(f"Reminders pending   : {pending_reminders}")
    print(f"Study subjects      : {len(study_data['subjects'])}")
    print(f"Research ideas      : {len(research_data['ideas'])}")

    utils.press_enter_to_continue()


def about_astra():
    utils.clear_screen()
    utils.print_header("ABOUT ECHO")

    settings = _get_settings()
    print(f"Assistant Name : {settings['assistant_name']}")
    print(f"Version        : {settings['version']}")
    print(f"Developer      : {config.DEVELOPER_NAME}")
    print(f"College        : {config.COLLEGE_NAME}")
    print("Platform       : Python 3.11 / Pydroid 3")
    print("Mode           : Offline, JSON-based storage")

    utils.press_enter_to_continue()


def main():
    config.ensure_data_folder_exists()

    utils.clear_screen()
    print_banner()

    while True:
        print_main_menu()
        choice = utils.get_menu_choice(
            "\nEnter choice: ",
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        )

        if choice == "1":
            dashboard()
        elif choice == "2":
            memory_menu()
        elif choice == "3":
            notes_menu()
        elif choice == "4":
            tasks_menu()
        elif choice == "5":
            reminders_menu()
        elif choice == "6":
            study_menu()
        elif choice == "7":
            research_menu()
        elif choice == "8":
            settings_menu()
        elif choice == "9":
            about_astra()
        elif choice == "0":
            utils.clear_screen()
            print("Goodbye! ECHO signing off.")
            break

        utils.clear_screen()


if __name__ == "__main__":
    main()
    