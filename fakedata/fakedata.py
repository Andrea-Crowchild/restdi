import sys
import os

from fsrs import Scheduler, Rating
from tutoricard import load_data

RATING_MAP = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy,
}
CONFIG_FILE = os.path.expanduser("~/.config/tutori/tutori.json")
cards, scheduler = load_data()


if cards is None:
    sys.exit()
if scheduler is None:
    sys.exit()
