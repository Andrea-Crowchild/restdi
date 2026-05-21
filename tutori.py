#!/usr/bin/env python3

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


# TODO: Move file loading commands into function
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # TODO: Add help strings
    if ctx.invoked_subcommand is not None:
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return

    if len(cards) == 0:
        return
    today = date.today()
    width = max(len(name) for name in cards) + 2
    for card in cards.values():
        if card.card.due.date() == today:
            print(f"{card.nametag.ljust(width)}", ":", f"{card.description}")


@cli.command()
def all():
    """View all items stored by Tutori"""
    # TODO: Improve docstrings
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return

    name_width = max(len(name) for name in cards) + 2
    date_width = max(len(str(card.card.due.date())) for card in cards.values())
    for card in cards.values():
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
    if os.path.exists(CONFIG_FILE):
        print("Are you sure you want to delete your file and start over?")
        print("Y/N to continue")
        choice = input()
        if choice == "Y" or choice == "y":
            cards = {}
            with open(CONFIG_FILE, "w") as f:
                json.dump({name: card.to_dict() for name, card in cards.items()}, f)
                return
        else:
            return

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
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return
    cards[nametag] = TutoriCard(nametag, description)
    # cards[nametag].card.due = datetime.now(timezone.utc) + timedelta(days=1)

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command(name="rate")
@click.argument("nametag")
@click.argument("rating", type=int)
def rate(nametag, rating):
    # TODO: Add help text
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return

    # TODO: Will raise KeyError, handle if nametag doesn't exist.
    scheduler = Scheduler()
    cards[nametag].card, review_log = scheduler.review_card(
        cards[nametag].card, RATING_MAP[rating]
    )
    print(f"Card rated {review_log.rating} on {review_log.review_datetime.date()}")

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


cli.add_command(rate, name="r")


# TODO: This is still a stub
@cli.command()
@click.argument("nametag")
@click.argument("description")
def edit(nametag, description):
    pass


@cli.command()
@click.argument("nametag")
def remove(nametag):
    # TODO: Add error handling
    try:
        with open(CONFIG_FILE, "r") as f:
            cards = {
                name: TutoriCard.from_dict(data) for name, data in json.load(f).items()
            }
    except FileNotFoundError:
        print("File not found, use command 'new' to generate your file")
        return
    except PermissionError:
        print("Permission error, unable to read file")
        return
    except json.JSONDecodeError:
        print("Unable to read file")
        return

    # TODO: Will raise KeyError, handle if nametag doesn't exist.
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
