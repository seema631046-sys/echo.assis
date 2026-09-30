# ECHO — Personal AI Assistant

**Developer:** Seema Sahu  
**Platform:** Python 3 · Pydroid 3  
**Mode:** Offline, JSON-based local storage

## Overview

ECHO is a personal, offline-first assistant that runs in the terminal.
It is built with Python's standard library and stores application data
locally as JSON files on the user's device.

## Features

- Dashboard for a quick overview
- Memory manager
- Notes manager
- Task manager
- Reminder manager
- Study planner with progress tracking
- Research / project idea vault
- Settings manager
- Offline JSON-based storage

## Project Structure

```text
ECHO/
├── main.py
├── config.py
├── utils.py
├── memory.py
├── notes.py
├── tasks.py
├── reminders.py
├── study.py
├── research.py
├── settings.py
├── requirements.txt
├── .gitignore
├── README.md
└── CHANGELOG.md
```

The `data/` directory is created automatically when ECHO runs and is
intentionally excluded from the public repository because it contains
local user data.

## Requirements

- Python 3.x
- Pydroid 3 (for running on Android)

ECHO currently uses only Python's standard library, so no third-party
packages are required.

## Run

1. Clone or download this repository.
2. Open the project folder in Pydroid 3 or a Python 3 environment.
3. Run `main.py`.

## Current Limitations

- Text/terminal interface only
- No OS-level notification scheduling yet
- No cloud synchronization
- No encryption for local JSON storage
- Menu-based interaction rather than natural-language commands

## Roadmap

Future versions may add due dates, priorities, notifications, data
backup/import, voice interaction, natural-language commands, and
additional local security features.

## Version

**v0.1 — Initial release**
