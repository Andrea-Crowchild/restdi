import json
import os

from fsrs import Card, Scheduler


class TutoriCard:
    def __init__(self, nametag, description, answer=""):
        self.nametag = nametag
        self.description = description
        self.answer = answer
        self.card = Card()
        self.review_logs = []

    def to_dict(self):
        return {
            "nametag": self.nametag,
            "description": self.description,
            "answer": self.answer,
            "card": self.card.to_dict(),
            "review_logs": self.review_logs,
        }

    @classmethod
    def from_dict(cls, data):
        tutori_card = cls(data["nametag"], data["description"], data["answer"])
        tutori_card.review_logs = data["review_logs"]
        tutori_card.card = Card.from_dict(data["card"])
        return tutori_card


CONFIG_FILE = os.path.expanduser("~/.config/tutori/tutori.json")


def load_data():
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        cards = {
            name: TutoriCard.from_dict(elements)
            for name, elements in data["cards"].items()
        }

        scheduler = Scheduler.from_json(json.dumps(data["scheduler"]))

        return cards, scheduler

    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return None, None
    except PermissionError:
        print("Permission error, unable to read file")
        return None, None
    except json.JSONDecodeError:
        print("Unable to read file")
        return None, None


def save_data(cards, scheduler):
    data = {
        "cards": {name: card.to_dict() for name, card in cards.items()},
        "scheduler": scheduler.to_dict(),
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


def backup_data(cards, scheduler, location):
    data = {
        "cards": {name: card.to_dict() for name, card in cards.items()},
        "scheduler": scheduler.to_dict(),
    }

    parsed_location = os.path.expanduser(location)

    with open(parsed_location, "w") as f:
        json.dump(data, f)
