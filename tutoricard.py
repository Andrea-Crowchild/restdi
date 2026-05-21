from fsrs import Card


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
