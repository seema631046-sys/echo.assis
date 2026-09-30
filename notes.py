from config import NOTES_FILE
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

DEFAULT_NOTES_DATA = {"notes": []}


def _load_notes():
    return load_json(NOTES_FILE, DEFAULT_NOTES_DATA)


def _save_notes(data):
    save_json(NOTES_FILE, data)


def _find_note_by_id(notes, note_id):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None


def add_note():
    clear_screen()
    print_header("ADD NOTE")

    title = get_nonempty_input("Title: ")
    content = get_nonempty_input("Content: ")

    data = _load_notes()
    new_note = {
        "id": get_next_id(data["notes"]),
        "title": title,
        "content": content,
    }
    data["notes"].append(new_note)
    _save_notes(data)

    print("\n✅ Note saved!")
    press_enter_to_continue()


def view_notes():
    clear_screen()
    print_header("ALL NOTES")

    data = _load_notes()
    notes = data["notes"]

    if not notes:
        print("No notes yet.")
    else:
        for note in notes:
            print(f"[{note['id']}] {note['title']}")
            print(f"    {note['content']}\n")

    press_enter_to_continue()


def edit_note():
    clear_screen()
    print_header("EDIT NOTE")

    data = _load_notes()
    notes = data["notes"]

    if not notes:
        print("No notes to edit.")
        press_enter_to_continue()
        return

    for note in notes:
        print(f"[{note['id']}] {note['title']}")

    id_input = get_nonempty_input("\nEnter ID of note to edit: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    note = _find_note_by_id(notes, int(id_input))
    if note is None:
        print("⚠ Note not found.")
        press_enter_to_continue()
        return

    print(f"\nCurrent title: {note['title']}")
    print(f"Current content: {note['content']}")

    new_title = get_nonempty_input("New title: ")
    new_content = get_nonempty_input("New content: ")

    note["title"] = new_title
    note["content"] = new_content
    _save_notes(data)

    print("\n✅ Note updated!")
    press_enter_to_continue()


def delete_note():
    clear_screen()
    print_header("DELETE NOTE")

    data = _load_notes()
    notes = data["notes"]

    if not notes:
        print("No notes to delete.")
        press_enter_to_continue()
        return

    for note in notes:
        print(f"[{note['id']}] {note['title']}")

    id_input = get_nonempty_input("\nEnter ID of note to delete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    note = _find_note_by_id(notes, int(id_input))
    if note is None:
        print("⚠ Note not found.")
        press_enter_to_continue()
        return

    if get_yes_no(f"Delete '{note['title']}'? (y/n): "):
        data["notes"].remove(note)
        _save_notes(data)
        print("\n🗑️ Note deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def search_notes():
    clear_screen()
    print_header("SEARCH NOTES")

    query = get_nonempty_input("Search keyword: ").lower()

    data = _load_notes()
    results = [
        n for n in data["notes"]
        if query in n["title"].lower() or query in n["content"].lower()
    ]

    if not results:
        print("\nNo matching notes found.")
    else:
        print(f"\nFound {len(results)} result(s):\n")
        for n in results:
            print(f"[{n['id']}] {n['title']}")
            print(f"    {n['content']}\n")

    press_enter_to_continue()


def notes_menu():
    while True:
        clear_screen()
        print_header("NOTES MENU")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Search Notes")
        print("6. Back to Main Menu")

        choice = get_menu_choice("Enter choice (1-6): ", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            edit_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            search_notes()
        elif choice == "6":
            break
            