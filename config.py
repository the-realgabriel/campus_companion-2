import os

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

FILES = {
    "events": os.path.join(DATA_DIR, "events.json"),
    "timetable": os.path.join(DATA_DIR, "timetable.json"),
    "assignments": os.path.join(DATA_DIR, "assignments.json"),
    "streaks": os.path.join(DATA_DIR, "streaks.json"),
    "budget": os.path.join(DATA_DIR, "budget.json"),
}
