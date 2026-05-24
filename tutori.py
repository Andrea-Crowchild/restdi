#!/usr/bin/env python3
# TODO: Add types to all command
# TODO: Add more error checking

from typing import Required
from tutoricard import TutoriCard, load_data, save_data, backup_data
import os
import click
from datetime import date, timedelta, timezone, datetime
from fsrs import Scheduler, Card, Rating, ReviewLog
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
    """View due items"""
    # TODO: Improve docstrings
    if ctx.invoked_subcommand is not None:
        return

    cards, scheduler = load_data()

    if not cards:
        return
    today = date.today()
    width = max(len(name) for name in cards) + 2
    cards = dict(sorted(cards.items()))
    for card in cards.values():
        if card.card.due.date() <= today:
            print(f"{card.nametag.ljust(width)}", ":", f"{card.description}")


@cli.command()
def all():
    """View all items stored by Tutori"""
    # TODO: Improve docstrings
    cards, scheduler = load_data()
    if not cards:
        return

    name_width = max(len(name) for name in cards) + 2
    date_width = max(len(str(card.card.due.date())) for card in cards.values())
    cards = dict(sorted(cards.items()))
    for card in cards.values():
        print(
            f"{card.nametag.ljust(name_width)}",
            ":",
            f"{str(card.card.due.date()).ljust(date_width)}",
            ":",
            f"{card.description}",
        )


cli.add_command(all, name="la")


# TODO: Add docstrings
@cli.command()
@click.argument("days_in", default=7, required=False, type=int)
def upcoming(days_in):
    cards, scheduler = load_data()

    if not cards:
        return
    days_from_today = date.today() + timedelta(days=days_in)

    name_width = max(len(name) for name in cards) + 2
    date_width = max(len(str(card.card.due.date())) for card in cards.values())
    for card in cards.values():
        if card.card.due.date() <= days_from_today:
            print(
                f"{card.nametag.ljust(name_width)}",
                ":",
                f"{str(card.card.due.date()).ljust(date_width)}",
                ":",
                f"{card.description}",
            )


cli.add_command(upcoming, name="u")


@cli.command()
@click.argument("nametag", type=str)
def show(nametag):
    """Displays the answer of an entry"""
    cards, scheduler = load_data()
    if cards is None:
        return

    print(cards[nametag].answer)


cli.add_command(show, name="s")


@cli.command()
def new():
    """Initialize or clear your save file"""
    # TODO: Improve docstrings
    if os.path.exists(CONFIG_FILE):
        cards, scheduler = load_data()
        print("Are you sure you want to delete your file and start over?")
        print("Y/N to continue")
        choice = input()
        if choice == "Y" or choice == "y":
            cards = {}
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
def reset():
    """Initialize or clear your save file"""
    # TODO: Improve docstrings
    if os.path.exists(CONFIG_FILE):
        cards, scheduler = load_data()
        print("Reset scheduler optimization?")
        print("Y/N to continue")
        choice = input()
        if choice == "Y" or choice == "y":
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
@click.argument("nametag", type=str)
@click.argument("description", type=str)
@click.argument("answer", required=False, type=str)
def add(nametag, description, answer):
    """Add an entry to Tutori"""
    # TODO: Improve docstrings
    cards, scheduler = load_data()
    if cards is None:
        return

    cards[nametag] = TutoriCard(nametag, description, answer or "")
    # cards[nametag].card.due = datetime.now(timezone.utc) + timedelta(days=1)

    save_data(cards, scheduler)


cli.add_command(add, name="a")


@cli.command(name="rate")
@click.argument("nametag", type=str)
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
    if cards[nametag].answer != "":
        print(cards[nametag].answer)
    print(f"Card rated {review_log.rating} on {review_log.review_datetime.date()}")
    print(f"Card next due on {due_date}")
    save_data(cards, scheduler)


cli.add_command(rate, name="r")


@cli.command()
@click.argument("old_name", type=str)
@click.argument("new_name", type=str)
@click.argument("description", required=False, type=str)
@click.argument("answer", required=False, type=str)
def edit(old_name, new_name, description, answer):
    cards, scheduler = load_data()
    if cards is None:
        return
    if old_name not in cards:
        print("That's not an entry")
        return

    temp = cards[old_name]
    cards.pop(old_name)
    cards[new_name] = temp
    cards[new_name].nametag = new_name

    if description is not None:
        cards[new_name].description = description
    if answer is not None:
        cards[new_name].answer = answer

    save_data(cards, scheduler)


cli.add_command(edit, name="e")


@cli.command()
@click.argument("nametag", type=str)
def remove(nametag):
    """Remove an entry from Tutori"""
    # TODO: Improve docstrings
    cards, scheduler = load_data()
    if cards is None:
        return
    if nametag not in cards:
        print("That's not an entry")
        return
    cards.pop(nametag)

    save_data(cards, scheduler)


cli.add_command(remove, name="rm")


# TODO: Improve docstrings
@cli.command()
def clean():
    """Remove entries scheduled further out than one year"""
    cards, scheduler = load_data()

    if not cards:
        return

    print("Clean entries?")
    print("Press Y/N to continue")
    choice = input()
    if choice != "Y" and choice != "y":
        return

    one_year_out = date.today() + timedelta(days=365)
    entries_to_clean = []
    for name, card in cards.items():
        if card.card.due.date() > one_year_out:
            entries_to_clean.append(name)
    for name in entries_to_clean:
        cards.pop(name)

    save_data(cards, scheduler)


# TODO: add docstrings
@cli.command()
@click.argument("location", type=str)
def save(location):
    cards, scheduler = load_data()

    backup_data(cards, scheduler, location)


# TODO: Flesh out function, lazy load optimizer
# TODO: from fsrs import Optimizer
@cli.command()
def optimize():
    from fsrs import Optimizer

    cards, scheduler = load_data()
    if cards is None:
        return
    all_logs = []
    for card in cards.values():
        for log in card.review_logs:
            all_logs.append(ReviewLog.from_json(json.dumps(log)))

    optimizer = Optimizer(all_logs)
    optimal_parameters = optimizer.compute_optimal_parameters()
    optimal_scheduler = Scheduler(optimal_parameters)
    print(optimal_parameters)
    for card in cards.values():
        card.card = optimal_scheduler.reschedule_card(
            card.card,
            [ReviewLog.from_json(json.dumps(log)) for log in card.review_logs],
        )

    save_data(cards, optimal_scheduler)


@cli.command()
def scheduler():
    cards, scheduler = load_data()
    if scheduler is None:
        return
    print(scheduler.parameters)


if __name__ == "__main__":
    cli()
