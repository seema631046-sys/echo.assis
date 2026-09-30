"""
research.py
------------
Research / Idea module for ECHO v0.1.

Stores ideas under categories: Research, AI, Coding, Business.
Each idea is a dictionary:

{
    "id": 1,
    "category": "AI",
    "title": "Voice-based note taker",
    "description": "An app that transcribes voice notes."
}

All ideas are saved in data/research.json under the key "ideas".
"""

from config import RESEARCH_FILE
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

DEFAULT_RESEARCH_DATA = {"ideas": []}

CATEGORIES = ["Research/Project", "AI", "Coding", "Business"]


def _load_ideas():
    return load_json(RESEARCH_FILE, DEFAULT_RESEARCH_DATA)


def _save_ideas(data):
    save_json(RESEARCH_FILE, data)


def _find_idea_by_id(ideas, idea_id):
    for idea in ideas:
        if idea["id"] == idea_id:
            return idea
    return None


def _print_idea_line(idea):
    print(f"[{idea['id']}] ({idea['category']}) {idea['title']}")
    print(f"    {idea['description']}")


def _choose_category():
    print("\nChoose a category:")
    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")
    valid_choices = [str(i) for i in range(1, len(CATEGORIES) + 1)]
    choice = get_menu_choice(f"Enter choice (1-{len(CATEGORIES)}): ", valid_choices)
    return CATEGORIES[int(choice) - 1]


def add_idea():
    clear_screen()
    print_header("ADD IDEA")

    category = _choose_category()
    title = get_nonempty_input("Idea title: ")
    description = get_nonempty_input("Description: ")

    data = _load_ideas()
    new_idea = {
        "id": get_next_id(data["ideas"]),
        "category": category,
        "title": title,
        "description": description,
    }
    data["ideas"].append(new_idea)
    _save_ideas(data)

    print("\n✅ Idea saved!")
    press_enter_to_continue()


def view_all_ideas():
    clear_screen()
    print_header("ALL IDEAS")

    data = _load_ideas()
    ideas = data["ideas"]

    if not ideas:
        print("No ideas saved yet.")
    else:
        for idea in ideas:
            _print_idea_line(idea)
            print()

    press_enter_to_continue()


def search_ideas():
    clear_screen()
    print_header("SEARCH IDEAS")

    query = get_nonempty_input("Search keyword: ").lower()

    data = _load_ideas()
    results = [
        idea for idea in data["ideas"]
        if query in idea["title"].lower()
        or query in idea["description"].lower()
        or query in idea["category"].lower()
    ]

    if not results:
        print("\nNo matching ideas found.")
    else:
        print(f"\nFound {len(results)} result(s):\n")
        for idea in results:
            _print_idea_line(idea)
            print()

    press_enter_to_continue()


def edit_idea():
    clear_screen()
    print_header("EDIT IDEA")

    data = _load_ideas()
    ideas = data["ideas"]

    if not ideas:
        print("No ideas to edit.")
        press_enter_to_continue()
        return

    for idea in ideas:
        _print_idea_line(idea)

    id_input = get_nonempty_input("\nEnter ID of idea to edit: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    idea = _find_idea_by_id(ideas, int(id_input))
    if idea is None:
        print("⚠ Idea not found.")
        press_enter_to_continue()
        return

    print(f"\nCurrent category: {idea['category']}")
    print(f"Current title: {idea['title']}")
    print(f"Current description: {idea['description']}")

    if get_yes_no("\nChange category too? (y/n): "):
        idea["category"] = _choose_category()

    idea["title"] = get_nonempty_input("New title: ")
    idea["description"] = get_nonempty_input("New description: ")

    _save_ideas(data)
    print("\n✅ Idea updated!")
    press_enter_to_continue()


def delete_idea():
    clear_screen()
    print_header("DELETE IDEA")

    data = _load_ideas()
    ideas = data["ideas"]

    if not ideas:
        print("No ideas to delete.")
        press_enter_to_continue()
        return

    for idea in ideas:
        _print_idea_line(idea)

    id_input = get_nonempty_input("\nEnter ID of idea to delete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    idea = _find_idea_by_id(ideas, int(id_input))
    if idea is None:
        print("⚠ Idea not found.")
        press_enter_to_continue()
        return

    if get_yes_no(f"Delete '{idea['title']}'? (y/n): "):
        data["ideas"].remove(idea)
        _save_ideas(data)
        print("\n🗑️ Idea deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


def research_menu():
    while True:
        clear_screen()
        print_header("RESEARCH MENU")
        print("1. Add Idea")
        print("2. View All Ideas")
        print("3. Search Ideas")
        print("4. Edit Idea")
        print("5. Delete Idea")
        print("6. Back to Main Menu")

        choice = get_menu_choice("Enter choice (1-6): ", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            add_idea()
        elif choice == "2":
            view_all_ideas()
        elif choice == "3":
            search_ideas()
        elif choice == "4":
            edit_idea()
        elif choice == "5":
            delete_idea()
        elif choice == "6":
            break
            