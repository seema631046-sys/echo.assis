"""
=========================================================
ECHO v0.1 - tasks.py
=========================================================
Task Manager module.

Each task is stored as a dictionary with this shape:
{
    "id": 1,
    "title": "Buy groceries",
    "completed": False
}

All tasks live inside data/tasks.json under the key "tasks".
This module handles: add, view, edit, delete, mark complete,
and search tasks.
=========================================================
"""

from config import TASKS_FILE
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

# Default structure used when tasks.json does not exist yet
DEFAULT_TASKS_DATA = {"tasks": []}


# ---------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------

def _load_tasks():
    """Reads tasks.json and returns the data dictionary."""
    return load_json(TASKS_FILE, DEFAULT_TASKS_DATA)


def _save_tasks(data):
    """Writes the data dictionary back to tasks.json."""
    save_json(TASKS_FILE, data)


def _find_task_by_id(tasks, task_id):
    """
    Loops through the list of tasks and returns the one
    whose "id" matches task_id. Returns None if not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def _print_task_line(task):
    """
    Prints a single task in a consistent format, showing
    a checkbox-style status: [x] for done, [ ] for pending.
    """
    status = "x" if task["completed"] else " "
    print(f"[{task['id']}] [{status}] {task['title']}")


# ---------------------------------------------------------
# CORE FEATURES
# ---------------------------------------------------------

def add_task():
    """Asks the user for a task title and saves it as pending."""
    clear_screen()
    print_header("ADD TASK")

    title = get_nonempty_input("Task description: ")

    data = _load_tasks()
    new_task = {
        "id": get_next_id(data["tasks"]),
        "title": title,
        "completed": False,  # new tasks always start as not done
    }
    data["tasks"].append(new_task)
    _save_tasks(data)

    print("\n✅ Task added!")
    press_enter_to_continue()


def view_pending_tasks():
    """Shows only the tasks that are NOT yet completed."""
    clear_screen()
    print_header("PENDING TASKS")

    data = _load_tasks()
    pending = [t for t in data["tasks"] if not t["completed"]]

    if not pending:
        print("No pending tasks. You're all caught up!")
    else:
        for task in pending:
            _print_task_line(task)

    press_enter_to_continue()


def view_completed_tasks():
    """Shows only the tasks that ARE marked completed."""
    clear_screen()
    print_header("COMPLETED TASKS")

    data = _load_tasks()
    completed = [t for t in data["tasks"] if t["completed"]]

    if not completed:
        print("No completed tasks yet.")
    else:
        for task in completed:
            _print_task_line(task)

    press_enter_to_continue()


def view_all_tasks():
    """Shows every task, pending and completed together."""
    clear_screen()
    print_header("ALL TASKS")

    data = _load_tasks()
    tasks = data["tasks"]

    if not tasks:
        print("No tasks yet.")
    else:
        for task in tasks:
            _print_task_line(task)

    press_enter_to_continue()


def edit_task():
    """Lets the user change the title of an existing task."""
    clear_screen()
    print_header("EDIT TASK")

    data = _load_tasks()
    tasks = data["tasks"]

    if not tasks:
        print("No tasks to edit.")
        press_enter_to_continue()
        return

    # Show all tasks so the user knows which ID to pick
    for task in tasks:
        _print_task_line(task)

    id_input = get_nonempty_input("\nEnter ID of task to edit: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    task = _find_task_by_id(tasks, int(id_input))
    if task is None:
        print("⚠ Task not found.")
        press_enter_to_continue()
        return

    print(f"\nCurrent title: {task['title']}")
    new_title = get_nonempty_input("New title: ")
    task["title"] = new_title

    _save_tasks(data)
    print("\n✅ Task updated!")
    press_enter_to_continue()


def delete_task():
    """Removes a task permanently from the list, after confirming."""
    clear_screen()
    print_header("DELETE TASK")

    data = _load_tasks()
    tasks = data["tasks"]

    if not tasks:
        print("No tasks to delete.")
        press_enter_to_continue()
        return

    for task in tasks:
        _print_task_line(task)

    id_input = get_nonempty_input("\nEnter ID of task to delete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    task = _find_task_by_id(tasks, int(id_input))
    if task is None:
        print("⚠ Task not found.")
        press_enter_to_continue()
        return

    if get_yes_no(f"Delete '{task['title']}'? (y/n): "):
        data["tasks"].remove(task)
        _save_tasks(data)
        print("\n🗑️ Task deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def mark_complete():
    """Flips a task's 'completed' value to True."""
    clear_screen()
    print_header("MARK TASK COMPLETE")

    data = _load_tasks()
    pending = [t for t in data["tasks"] if not t["completed"]]

    if not pending:
        print("No pending tasks to mark complete.")
        press_enter_to_continue()
        return

    for task in pending:
        _print_task_line(task)

    id_input = get_nonempty_input("\nEnter ID of task to mark complete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    task = _find_task_by_id(data["tasks"], int(id_input))
    if task is None:
        print("⚠ Task not found.")
        press_enter_to_continue()
        return

    task["completed"] = True
    _save_tasks(data)

    print(f"\n✅ '{task['title']}' marked as complete!")
    press_enter_to_continue()


def search_tasks():
    """Searches task titles for a keyword (case-insensitive)."""
    clear_screen()
    print_header("SEARCH TASKS")

    query = get_nonempty_input("Search keyword: ").lower()

    data = _load_tasks()
    results = [t for t in data["tasks"] if query in t["title"].lower()]

    if not results:
        print("\nNo matching tasks found.")
    else:
        print(f"\nFound {len(results)} result(s):\n")
        for task in results:
            _print_task_line(task)

    press_enter_to_continue()


# ---------------------------------------------------------
# TASKS MENU (entry point called from main.py)
# ---------------------------------------------------------

def tasks_menu():
    """
    Displays the Task Manager menu in a loop until the
    user chooses to go back to the main menu.
    """
    while True:
        clear_screen()
        print_header("TASKS MENU")
        print("1. Add Task")
        print("2. View Pending Tasks")
        print("3. View Completed Tasks")
        print("4. View All Tasks")
        print("5. Edit Task")
        print("6. Delete Task")
        print("7. Mark Task Complete")
        print("8. Search Tasks")
        print("9. Back to Main Menu")

        choice = get_menu_choice(
            "Enter choice (1-9): ",
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        )

        if choice == "1":
            add_task()
        elif choice == "2":
            view_pending_tasks()
        elif choice == "3":
            view_completed_tasks()
        elif choice == "4":
            view_all_tasks()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            mark_complete()
        elif choice == "8":
            search_tasks()
        elif choice == "9":
            break
            