from fsrs import Card
import json
import os


class TutoriCard:
    def __init__(self, nametag, description):
        self.nametag = nametag
        self.description = description
        self.card = Card()

    def to_dict(self):
        return {
            "nametag": self.nametag,
            "description": self.description,
            "card": self.card.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        restdi_card = cls(data["nametag"], data["description"])
        restdi_card.card = Card.from_dict(data["card"])
        return restdi_card


CONFIG_FILE = os.path.expanduser("~/.config/tutori/tutori.json")


def load_data():
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
            return cards
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return
