"""
=========================================================
ECHO v0.1 - memory.py
=========================================================
This module lets ECHO "remember" things about you.

Every memory entry has:
    id       -> a unique number (auto-generated)
    category -> "Personal Info" or "Preference"
    key      -> short label, e.g. "Favorite Color"
    value    -> the actual info, e.g. "Blue"

All memories are stored in data/memory.json like this:

{
    "memories": [
        {
            "id": 1,
            "category": "Personal Info",
            "key": "Name",
            "value": "Seema Sahu"
        },
        {
            "id": 2,
            "category": "Preference",
            "key": "Favorite Color",
            "value": "Blue"
        }
    ]
}
=========================================================
"""

from config import MEMORY_FILE
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

# Default structure used when memory.json does not exist yet
DEFAULT_MEMORY_DATA = {"memories": []}


# ---------------------------------------------------------
# INTERNAL HELPERS (used only inside this file)
# ---------------------------------------------------------

def _load_memory():
    """Loads the memory data from the JSON file."""
    return load_json(MEMORY_FILE, DEFAULT_MEMORY_DATA)


def _save_memory(data):
    """Saves the memory data back to the JSON file."""
    save_json(MEMORY_FILE, data)


def _choose_category():
    """
    Asks the user to pick a category and returns it
    as a clean string.
    """
    print("\nChoose a category:")
    print("1. Personal Info")
    print("2. Preference")
    choice = get_menu_choice("Enter choice (1-2): ", ["1", "2"])
    return "Personal Info" if choice == "1" else "Preference"


def _find_memory_by_id(memories, memory_id):
    """
    Searches the list of memories for one matching memory_id.
    Returns the matching dictionary, or None if not found.
    """
    for item in memories:
        if item["id"] == memory_id:
            return item
    return None


# ---------------------------------------------------------
# CORE FEATURES
# ---------------------------------------------------------

def add_memory():
    """Adds a new personal info / preference entry."""
    clear_screen()
    print_header("ADD MEMORY")

    category = _choose_category()
    key = get_nonempty_input("Enter a short label (e.g. 'Name', 'Favorite Food'): ")
    value = get_nonempty_input("Enter the value/details: ")

    data = _load_memory()
    new_entry = {
        "id": get_next_id(data["memories"]),
        "category": category,
        "key": key,
        "value": value,
    }
    data["memories"].append(new_entry)
    _save_memory(data)

    print(f"\n✅ Saved! ({category}: {key} = {value})")
    press_enter_to_continue()


def view_memory():
    """Displays all saved memories, grouped by category."""
    clear_screen()
    print_header("ALL MEMORIES")

    data = _load_memory()
    memories = data["memories"]

    if not memories:
        print("No memories saved yet.")
    else:
        for item in memories:
            print(f"[{item['id']}] ({item['category']}) {item['key']}: {item['value']}")

    press_enter_to_continue()


def edit_memory():
    """Lets the user edit an existing memory entry by ID."""
    clear_screen()
    print_header("EDIT MEMORY")

    data = _load_memory()
    memories = data["memories"]

    if not memories:
        print("No memories to edit yet.")
        press_enter_to_continue()
        return

    # Show existing memories so the user can pick an ID
    for item in memories:
        print(f"[{item['id']}] ({item['category']}) {item['key']}: {item['value']}")

    id_input = get_nonempty_input("\nEnter the ID of the memory to edit: ")

    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    memory_id = int(id_input)
    entry = _find_memory_by_id(memories, memory_id)

    if entry is None:
        print("⚠ No memory found with that ID.")
        press_enter_to_continue()
        return

    print(f"\nEditing: ({entry['category']}) {entry['key']}: {entry['value']}")
    new_key = get_nonempty_input(f"New label (leave same by re-typing) [{entry['key']}]: ")
    new_value = get_nonempty_input(f"New value [{entry['value']}]: ")

    entry["key"] = new_key
    entry["value"] = new_value

    _save_memory(data)
    print("\n✅ Memory updated!")
    press_enter_to_continue()


def delete_memory():
    """Lets the user delete a memory entry by ID."""
    clear_screen()
    print_header("DELETE MEMORY")

    data = _load_memory()
    memories = data["memories"]

    if not memories:
        print("No memories to delete yet.")
        press_enter_to_continue()
        return

    for item in memories:
        print(f"[{item['id']}] ({item['category']}) {item['key']}: {item['value']}")

    id_input = get_nonempty_input("\nEnter the ID of the memory to delete: ")

    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    memory_id = int(id_input)
    entry = _find_memory_by_id(memories, memory_id)

    if entry is None:
        print("⚠ No memory found with that ID.")
        press_enter_to_continue()
        return

    confirm = get_yes_no(f"Are you sure you want to delete '{entry['key']}'? (y/n): ")
    if confirm:
        data["memories"].remove(entry)
        _save_memory(data)
        print("\n🗑️ Memory deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def search_memory():
    """Searches memories by key or value (case-insensitive)."""
    clear_screen()
    print_header("SEARCH MEMORY")

    query = get_nonempty_input("Enter a keyword to search: ").lower()

    data = _load_memory()
    results = [
        item for item in data["memories"]
        if query in item["key"].lower() or query in item["value"].lower()
    ]

    if not results:
        print("\nNo matching memories found.")
    else:
        print(f"\nFound {len(results)} result(s):\n")
        for item in results:
            print(f"[{item['id']}] ({item['category']}) {item['key']}: {item['value']}")

    press_enter_to_continue()


# ---------------------------------------------------------
# MEMORY MENU (entry point called from main.py)
# ---------------------------------------------------------

def memory_menu():
    """
    Displays the Memory module menu in a loop until the
    user chooses to go back to the main menu.
    """
    while True:
        clear_screen()
        print_header("MEMORY MENU")
        print("1. Add Memory")
        print("2. View All Memories")
        print("3. Edit Memory")
        print("4. Delete Memory")
        print("5. Search Memory")
        print("6. Back to Main Menu")

        choice = get_menu_choice("Enter choice (1-6): ", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            add_memory()
        elif choice == "2":
            view_memory()
        elif choice == "3":
            edit_memory()
        elif choice == "4":
            delete_memory()
        elif choice == "5":
            search_memory()
        elif choice == "6":
            break
            