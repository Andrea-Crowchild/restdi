#!/usr/bin/env python3

from tutoricard import TutoriCard, load_data, save_data
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


# TODO: Build functionality to store review logs
# TODO: Investigate building compatibility with the FSRS optimizer


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """View due items"""
    # TODO: Improve docstrings
    if ctx.invoked_subcommand is not None:
        return

    cards, scheduler = load_data()

    if cards is None:
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
    cards, scheduler = load_data()
    if cards is None:
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


# TODO: Alternative name "soon"
# TODO: Write upcoming function
@cli.command()
@click.argument("days", default=7, required=False)
def upcoming(days):
    pass


@cli.command()
def new():
    """Initialize or clear your save file"""
    # TODO: Improve docstrings
    if os.path.exists(CONFIG_FILE):
        print("Are you sure you want to delete your file and start over?")
        print("Y/N to continue")
        choice = input()
        if choice == "Y" or choice == "y":
            cards = {}
            scheduler = Scheduler()
            save_data(cards, scheduler)
            return
        else:
            return

    config_dir = os.path.expanduser("~/.config/tutori/")
    os.makedirs(config_dir, exist_ok=True)

    cards = {}
    scheduler = Scheduler()
    save_data(cards, scheduler)


@cli.command()
@click.argument("nametag")
@click.argument("description")
def add(nametag, description):
    """Add an entry to Tutori"""
    # TODO: Add help text
    cards, scheduler = load_data()
    if cards is None:
        return

    cards[nametag] = TutoriCard(nametag, description)
    # cards[nametag].card.due = datetime.now(timezone.utc) + timedelta(days=1)

    save_data(cards, scheduler)


@cli.command(name="rate")
@click.argument("nametag")
@click.argument("rating", type=int)
def rate(nametag, rating):
    """Rate an entry on a scale of 1 to 4"""
    # TODO: Improve docstrings
    cards, scheduler = load_data()
    if cards is None:
        return
    if scheduler is None:
        return
    if nametag not in cards:
        return

    cards[nametag].card, review_log = scheduler.review_card(
        cards[nametag].card, RATING_MAP[rating]
    )

    due_date = cards[nametag].card.due.date()
    cards[nametag].review_logs.append(json.loads(review_log.to_json()))
    # TODO: Print the next due date for each reviewed card
    print(f"Card rated {review_log.rating} on {review_log.review_datetime.date()}")
    print(f"Card next due on {due_date}")
    save_data(cards, scheduler)


cli.add_command(rate, name="r")


# TODO: This is still a stub
@cli.command()
@click.argument("old_name")
@click.argument("new_name")
@click.argument("description", required=False)
def edit(old_name, new_name, description):
    pass


@cli.command()
@click.argument("nametag")
def remove(nametag):
    """Remove an entry from Tutori"""
    # TODO: Improve docstrings
    cards, scheduler = load_data()
    if cards is None:
        return

    # TODO: Will raise KeyError, handle if nametag doesn't exist.
    cards.pop(nametag)

    save_data(cards, scheduler)


# TODO: Still a stub
# TODO: Decide whether or not we will want this feature
# TODO: Write a function that automatically purges the list of max mastery items.
@cli.command()
def clean():
    pass


# TODO: Still a stub
# TODO: Write a function that saves the storage file to a specified location.
@cli.command()
@click.argument("location")
def save(location):
    pass


if __name__ == "__main__":
    cli()
