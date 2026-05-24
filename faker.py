import random
import sys
from tutoricard import TutoriCard, load_data, save_data, backup_data
import os
from datetime import date, timedelta, datetime, timezone
from fsrs import Scheduler, Card, Rating, ReviewLog
import json

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

ratings = [1, 2, 3, 4]
weights = [10, 20, 50, 20]


review_time = datetime.now(timezone.utc)
next_time = max(card.card.due for card in cards.values())
max_advance = review_time + timedelta(days=30)
review_time = min(next_time, max_advance)
for i in range(1, 75):
    for card in cards.values():
        result = random.choices(ratings, weights=weights, k=1)[0]
        card.card, review_log = scheduler.review_card(
            card.card, RATING_MAP[result], review_time
        )
        card.review_logs.append(json.loads(review_log.to_json()))
    review_time = max(card.card.due for card in cards.values())

output_file = os.path.expanduser("~/code/tutori/fake_tutori.json")
data = {
    "cards": {name: card.to_dict() for name, card in cards.items()},
    "scheduler": scheduler.to_dict(),
}
with open(output_file, "w") as f:
    json.dump(data, f)
