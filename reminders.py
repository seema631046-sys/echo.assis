"""
=========================================================
ECHO v0.1 - reminders.py
=========================================================
Reminders module.

Each reminder is stored as a dictionary with this shape:
{
    "id": 1,
    "text": "Call the electrician",
    "done": False
}

All reminders live inside data/reminders.json under the
key "reminders". This module handles: add, view, delete,
and mark done.
=========================================================
"""

from config import REMINDERS_FILE
from utils import (
    load_json,
    save_json,
    clear_screen,
    print_header,
    press_enter_to_continue,
    get_nonempty_input,
    get_menu_choice,
    get_yes_no,
    get_next_id,
)

# Default structure used when reminders.json does not exist yet
DEFAULT_REMINDERS_DATA = {"reminders": []}


# ---------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------

def _load_reminders():
    """Reads reminders.json and returns the data dictionary."""
    return load_json(REMINDERS_FILE, DEFAULT_REMINDERS_DATA)


def _save_reminders(data):
    """Writes the data dictionary back to reminders.json."""
    save_json(REMINDERS_FILE, data)


def _find_reminder_by_id(reminders, reminder_id):
    """
    Loops through the list of reminders and returns the one
    whose "id" matches reminder_id. Returns None if not found.
    """
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            return reminder
    return None


def _print_reminder_line(reminder):
    """
    Prints a single reminder with a checkbox-style status:
    [x] for done, [ ] for not done yet.
    """
    status = "x" if reminder["done"] else " "
    print(f"[{reminder['id']}] [{status}] {reminder['text']}")


# ---------------------------------------------------------
# CORE FEATURES
# ---------------------------------------------------------

def add_reminder():
    """Asks the user for reminder text and saves it as not done."""
    clear_screen()
    print_header("ADD REMINDER")

    text = get_nonempty_input("Reminder text: ")

    data = _load_reminders()
    new_reminder = {
        "id": get_next_id(data["reminders"]),
        "text": text,
        "done": False,  # new reminders start as not done
    }
    data["reminders"].append(new_reminder)
    _save_reminders(data)

    print("\n✅ Reminder saved!")
    press_enter_to_continue()


def view_reminders():
    """Shows every saved reminder, done and not done."""
    clear_screen()
    print_header("ALL REMINDERS")

    data = _load_reminders()
    reminders = data["reminders"]

    if not reminders:
        print("No reminders saved yet.")
    else:
        for reminder in reminders:
            _print_reminder_line(reminder)

    press_enter_to_continue()


def delete_reminder():
    """Removes a reminder permanently, after confirming with the user."""
    clear_screen()
    print_header("DELETE REMINDER")

    data = _load_reminders()
    reminders = data["reminders"]

    if not reminders:
        print("No reminders to delete.")
        press_enter_to_continue()
        return

    for reminder in reminders:
        _print_reminder_line(reminder)

    id_input = get_nonempty_input("\nEnter ID of reminder to delete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    reminder = _find_reminder_by_id(reminders, int(id_input))
    if reminder is None:
        print("⚠ Reminder not found.")
        press_enter_to_continue()
        return

    if get_yes_no(f"Delete '{reminder['text']}'? (y/n): "):
        data["reminders"].remove(reminder)
        _save_reminders(data)
        print("\n🗑️ Reminder deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def mark_done():
    """Flips a reminder's 'done' value to True."""
    clear_screen()
    print_header("MARK REMINDER DONE")

    data = _load_reminders()
    not_done = [r for r in data["reminders"] if not r["done"]]

    if not not_done:
        print("No pending reminders to mark done.")
        press_enter_to_continue()
        return

    for reminder in not_done:
        _print_reminder_line(reminder)

    id_input = get_nonempty_input("\nEnter ID of reminder to mark done: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    reminder = _find_reminder_by_id(data["reminders"], int(id_input))
    if reminder is None:
        print("⚠ Reminder not found.")
        press_enter_to_continue()
        return

    reminder["done"] = True
    _save_reminders(data)

    print(f"\n✅ '{reminder['text']}' marked as done!")
    press_enter_to_continue()


# ---------------------------------------------------------
# REMINDERS MENU (entry point called from main.py)
# ---------------------------------------------------------

def reminders_menu():
    """
    Displays the Reminders module menu in a loop until the
    user chooses to go back to the main menu.
    """
    while True:
        clear_screen()
        print_header("REMINDERS MENU")
        print("1. Add Reminder")
        print("2. View Reminders")
        print("3. Delete Reminder")
        print("4. Mark Reminder Done")
        print("5. Back to Main Menu")

        choice = get_menu_choice("Enter choice (1-5): ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            add_reminder()
        elif choice == "2":
            view_reminders()
        elif choice == "3":
            delete_reminder()
        elif choice == "4":
            mark_done()
        elif choice == "5":
            break
            