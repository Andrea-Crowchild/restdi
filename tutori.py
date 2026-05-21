from tutoricard import TutoriCard
import os
import click
from datetime import date, timezone, timedelta, datetime
from fsrs import Scheduler, Card, Rating, ReviewLog, State
import json

CONFIG_FILE = os.path.expanduser("~/.config/tutori/tutori.json")
RATING_MAP = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy,
}


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # TODO: Add help strings
    # TODO: Add error catching
    if ctx.invoked_subcommand is None:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
        today = date.today()
        width = max(len(name) for name in cards) + 2
        for card in cards.keys():
            if card.card.due.date() == today:
                print(f"{card.nametag.ljust(width)}", ":", f"{card.description}")


@cli.command()
def all():
    """View all items stored by Tutori"""
    # TODO: Improve docstrings
    # TODO: Add error catching
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }
    name_width = max(len(name) for name in cards) + 2
    date_width = max(len(str(card.card.due.date())) for card in cards.keys())
    for card in cards.keys():
        print(
            f"{card.nametag.ljust(name_width)}",
            ":",
            f"{str(card.card.due.date()).ljust(date_width)}",
            ":",
            f"{card.description}",
        )


cli.add_command(all, name="la")


@cli.command()
def new():
    # TODO: Add help strings
    # TODO: add logic to check if user wants to delete their file
    config_dir = os.path.expanduser("~/.config/tutori/")
    os.makedirs(config_dir, exist_ok=True)
    cards = {}
    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command()
@click.argument("nametag")
@click.argument("description")
def add(nametag, description):
    # TODO: Add help text
    # TODO: Add error catching
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }
    cards[nametag] = TutoriCard(nametag, description)
    # cards[nametag].card.due = datetime.now(timezone.utc) + timedelta(days=1)

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command(name="rate")
@click.argument("nametag")
@click.argument("rating", type=int)
def rate(nametag, rating):
    # TODO: Add help text
    # TODO: Add error catching
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }
    scheduler = Scheduler()
    cards[nametag].card, review_log = scheduler.review_card(
        cards[nametag].card, RATING_MAP[rating]
    )
    print(f"Card rated {review_log.rating} on {review_log.review_datetime.date()}")

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


cli.add_command(rate, name="r")


@cli.command()
@click.argument("nametag")
@click.argument("description")
def edit(nametag, description):
    pass


@cli.command()
@click.argument("nametag")
def remove(nametag):
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }

    cards.pop(nametag)

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


# TODO: Decide whether or not we will want this feature
# TODO: Write a function that automatically purges the list of max mastery items.
@cli.command()
def clean():
    pass


# TODO: Write a function that saves the storage file to a specified location.
@cli.command()
@click.argument("location")
def save(location):
    pass


if __name__ == "__main__":
    cli()
