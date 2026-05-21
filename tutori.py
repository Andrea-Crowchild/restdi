# ruff: noqa: F401
from tutoricard import TutoriCard
import os
import click
from datetime import date, timezone, timedelta, datetime
from fsrs import Scheduler, Card, Rating, ReviewLog, State, review_log, scheduler
import json

CONFIG_FILE = os.path.expanduser("~/.config/tutori/tutori.json")
RATING_MAP = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy,
}


# TODO: Create a secondary file and populate it with the logic that
# TODO: manages dates.
# TODO: Design main function to take an optional nametag and a rating to
# TODO: rate items and remove them from the list.


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
        today = date.today()
        for _name, card in cards.items():
            if card.card.due.date() == today:
                print(f"{card.nametag} : {card.description}")


# TODO: Write a command to view all items in the list
# TODO: regardless of date
@cli.command()
def all():
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }

    for name, card in cards.items():
        print(f"{card.nametag} : {card.description} : {card.card.due.date()}")


cli.add_command(all, name="la")


# TODO: Get new files working
@cli.command()
def new():
    # cards = {"test_one": restdi_card.RestdiCard("test_one", "description one of many")}
    cards = {}
    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command()
@click.argument("nametag")
@click.argument("description")
def add(nametag, description):
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
        }
    cards[nametag] = TutoriCard(nametag, description)
    # cards[nametag].card.due = datetime.now(timezone.utc) + timedelta(days=1)

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


cli.add_command(add, name="a")


@cli.command(name="rate")
@click.argument("nametag")
@click.argument("rating", type=int)
def rate(nametag, rating):
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
