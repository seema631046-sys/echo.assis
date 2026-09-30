"""
=========================================================
ECHO v0.1 - study.py
=========================================================
Study Planner module.

Data is organized as subjects, each containing a list of
topics. Structure stored in data/study.json:

{
    "subjects": [
        {
            "id": 1,
            "name": "Mathematics",
            "topics": [
                {
                    "id": 1,
                    "name": "Algebra",
                    "completed": False,
                    "needs_revision": False
                }
            ]
        }
    ]
}

Features: subject management (add/view/delete), add topic,
mark topic complete, view progress percentage per subject,
view completed topics, and a revision tracker.
=========================================================
"""

from config import STUDY_FILE
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

# Default structure used when study.json does not exist yet
DEFAULT_STUDY_DATA = {"subjects": []}


# ---------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------

def _load_study():
    """Reads study.json and returns the data dictionary."""
    return load_json(STUDY_FILE, DEFAULT_STUDY_DATA)


def _save_study(data):
    """Writes the data dictionary back to study.json."""
    save_json(STUDY_FILE, data)


def _find_subject_by_id(subjects, subject_id):
    """Returns the subject dict matching subject_id, or None."""
    for subject in subjects:
        if subject["id"] == subject_id:
            return subject
    return None


def _find_topic_by_id(topics, topic_id):
    """Returns the topic dict matching topic_id, or None."""
    for topic in topics:
        if topic["id"] == topic_id:
            return topic
    return None


def _calculate_progress(subject):
    """
    Returns the completion percentage for a subject as a
    float (0-100). If a subject has no topics yet, returns 0.
    """
    topics = subject["topics"]
    if not topics:
        return 0.0
    completed_count = sum(1 for t in topics if t["completed"])
    return (completed_count / len(topics)) * 100


def _print_subject_line(subject):
    """Prints a subject with its id, name, and progress percentage."""
    progress = _calculate_progress(subject)
    print(f"[{subject['id']}] {subject['name']} - {progress:.0f}% complete")


def _print_topic_line(topic):
    """
    Prints a single topic with a checkbox for completion and
    a marker (R) if it needs revision.
    """
    status = "x" if topic["completed"] else " "
    revision_tag = " (needs revision)" if topic["needs_revision"] else ""
    print(f"    [{topic['id']}] [{status}] {topic['name']}{revision_tag}")


def _select_subject(subjects):
    """
    Displays all subjects and asks the user to pick one by ID.
    Returns the subject dict, or None if invalid/cancelled.
    """
    for subject in subjects:
        _print_subject_line(subject)

    id_input = get_nonempty_input("\nEnter Subject ID: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        return None

    subject = _find_subject_by_id(subjects, int(id_input))
    if subject is None:
        print("⚠ Subject not found.")
        return None

    return subject


# ---------------------------------------------------------
# SUBJECT MANAGEMENT
# ---------------------------------------------------------

def add_subject():
    """Creates a new subject with an empty topic list."""
    clear_screen()
    print_header("ADD SUBJECT")

    name = get_nonempty_input("Subject name: ")

    data = _load_study()
    new_subject = {
        "id": get_next_id(data["subjects"]),
        "name": name,
        "topics": [],
    }
    data["subjects"].append(new_subject)
    _save_study(data)

    print("\n✅ Subject added!")
    press_enter_to_continue()


def view_subjects():
    """Lists all subjects along with their progress percentage."""
    clear_screen()
    print_header("ALL SUBJECTS")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects yet.")
    else:
        for subject in subjects:
            _print_subject_line(subject)

    press_enter_to_continue()


def delete_subject():
    """Deletes a subject and all of its topics, after confirming."""
    clear_screen()
    print_header("DELETE SUBJECT")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects to delete.")
        press_enter_to_continue()
        return

    subject = _select_subject(subjects)
    if subject is None:
        press_enter_to_continue()
        return

    if get_yes_no(f"Delete '{subject['name']}' and all its topics? (y/n): "):
        data["subjects"].remove(subject)
        _save_study(data)
        print("\n🗑️ Subject deleted.")
    else:
        print("\nCancelled.")

    press_enter_to_continue()


# ---------------------------------------------------------
# TOPIC MANAGEMENT
# ---------------------------------------------------------

def add_topic():
    """Adds a new topic to an existing subject."""
    clear_screen()
    print_header("ADD TOPIC")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects yet. Add a subject first.")
        press_enter_to_continue()
        return

    subject = _select_subject(subjects)
    if subject is None:
        press_enter_to_continue()
        return

    topic_name = get_nonempty_input("Topic name: ")
    new_topic = {
        "id": get_next_id(subject["topics"]),
        "name": topic_name,
        "completed": False,
        "needs_revision": False,
    }
    subject["topics"].append(new_topic)
    _save_study(data)

    print("\n✅ Topic added!")
    press_enter_to_continue()


def mark_topic_complete():
    """Marks a topic within a subject as completed."""
    clear_screen()
    print_header("MARK TOPIC COMPLETE")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects yet.")
        press_enter_to_continue()
        return

    subject = _select_subject(subjects)
    if subject is None:
        press_enter_to_continue()
        return

    if not subject["topics"]:
        print("This subject has no topics yet.")
        press_enter_to_continue()
        return

    print()
    for topic in subject["topics"]:
        _print_topic_line(topic)

    id_input = get_nonempty_input("\nEnter Topic ID to mark complete: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    topic = _find_topic_by_id(subject["topics"], int(id_input))
    if topic is None:
        print("⚠ Topic not found.")
        press_enter_to_continue()
        return

    topic["completed"] = True
    _save_study(data)

    print(f"\n✅ '{topic['name']}' marked as complete!")
    press_enter_to_continue()


# ---------------------------------------------------------
# PROGRESS AND COMPLETED TOPICS
# ---------------------------------------------------------

def view_progress():
    """Shows each subject with its topics and progress percentage."""
    clear_screen()
    print_header("STUDY PROGRESS")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects yet.")
    else:
        for subject in subjects:
            _print_subject_line(subject)
            for topic in subject["topics"]:
                _print_topic_line(topic)
            print()

    press_enter_to_continue()


def view_completed_topics():
    """Lists only the topics marked as completed, grouped by subject."""
    clear_screen()
    print_header("COMPLETED TOPICS")

    data = _load_study()
    subjects = data["subjects"]

    found_any = False
    for subject in subjects:
        completed = [t for t in subject["topics"] if t["completed"]]
        if completed:
            found_any = True
            print(f"{subject['name']}:")
            for topic in completed:
                _print_topic_line(topic)
            print()

    if not found_any:
        print("No completed topics yet.")

    press_enter_to_continue()


# ---------------------------------------------------------
# REVISION TRACKER
# ---------------------------------------------------------

def view_revision_list():
    """Lists every topic across all subjects marked as needing revision."""
    clear_screen()
    print_header("REVISION LIST")

    data = _load_study()
    subjects = data["subjects"]

    found_any = False
    for subject in subjects:
        flagged = [t for t in subject["topics"] if t["needs_revision"]]
        if flagged:
            found_any = True
            print(f"{subject['name']}:")
            for topic in flagged:
                _print_topic_line(topic)
            print()

    if not found_any:
        print("No topics marked for revision.")

    press_enter_to_continue()


def toggle_revision_flag():
    """Turns a topic's 'needs_revision' flag on or off."""
    clear_screen()
    print_header("TOGGLE REVISION FLAG")

    data = _load_study()
    subjects = data["subjects"]

    if not subjects:
        print("No subjects yet.")
        press_enter_to_continue()
        return

    subject = _select_subject(subjects)
    if subject is None:
        press_enter_to_continue()
        return

    if not subject["topics"]:
        print("This subject has no topics yet.")
        press_enter_to_continue()
        return

    print()
    for topic in subject["topics"]:
        _print_topic_line(topic)

    id_input = get_nonempty_input("\nEnter Topic ID to toggle revision flag: ")
    if not id_input.isdigit():
        print("⚠ Invalid ID.")
        press_enter_to_continue()
        return

    topic = _find_topic_by_id(subject["topics"], int(id_input))
    if topic is None:
        print("⚠ Topic not found.")
        press_enter_to_continue()
        return

    topic["needs_revision"] = not topic["needs_revision"]
    _save_study(data)

    state = "marked for revision" if topic["needs_revision"] else "unmarked"
    print(f"\n✅ '{topic['name']}' {state}.")
    press_enter_to_continue()


def revision_tracker_menu():
    """Sub-menu for revision tracking, called from the main study menu."""
    while True:
        clear_screen()
        print_header("REVISION TRACKER")
        print("1. View Revision List")
        print("2. Toggle Revision Flag on a Topic")
        print("3. Back to Study Menu")

        choice = get_menu_choice("Enter choice (1-3): ", ["1", "2", "3"])

        if choice == "1":
            view_revision_list()
        elif choice == "2":
            toggle_revision_flag()
        elif choice == "3":
            break


# ---------------------------------------------------------
# STUDY MENU (entry point called from main.py)
# ---------------------------------------------------------

def study_menu():
    """
    Displays the Study Planner menu in a loop until the
    user chooses to go back to the main menu.
    """
    while True:
        clear_screen()
        print_header("STUDY PLANNER MENU")
        print("1. Add Subject")
        print("2. View Subjects")
        print("3. Delete Subject")
        print("4. Add Topic")
        print("5. Mark Topic Complete")
        print("6. View Progress")
        print("7. View Completed Topics")
        print("8. Revision Tracker")
        print("9. Back to Main Menu")

        choice = get_menu_choice(
            "Enter choice (1-9): ",
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        )

        if choice == "1":
            add_subject()
        elif choice == "2":
            view_subjects()
        elif choice == "3":
            delete_subject()
        elif choice == "4":
            add_topic()
        elif choice == "5":
            mark_topic_complete()
        elif choice == "6":
            view_progress()
        elif choice == "7":
            view_completed_topics()
        elif choice == "8":
            revision_tracker_menu()
        elif choice == "9":
            break
            