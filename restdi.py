# ruff: noqa: F401
import restdi_card
import os
import click
from datetime import datetime
from fsrs import Scheduler, Card, Rating, ReviewLog, State, review_log
import json

CONFIG_FILE = os.path.expanduser("~/Code/python/restdi/restdi.json")


# TODO: Create a secondary file and populate it with the logic that
# TODO: manages dates.
# TODO: Design main function to take an optional nametag and a rating to
# TODO: rate items and remove them from the list.


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    pass


# TODO: Write a command to view all items in the list
# TODO: regardless of date
@cli.command()
def all():
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: restdi_card.RestdiCard.from_dict(data)
            for name, data in json.load(f).items()
        }

    for name, card in cards.items():
        print(f"{card.nametag} : {card.description} : {card.card.due.date()}")


# TODO: Get new files working
@cli.command()
def new():
    cards = {"test_one": restdi_card.RestdiCard("test_one", "description one of many")}
    # cards = {}
    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command()
@click.argument("nametag")
@click.argument("description")
def add(nametag, description):
    with open(CONFIG_FILE, "r") as f:
        cards = {
            name: restdi_card.RestdiCard.from_dict(data)
            for name, data in json.load(f).items()
        }
    cards[nametag] = restdi_card.RestdiCard(nametag, description)

    with open(CONFIG_FILE, "w") as f:
        json.dump({name: card.to_dict() for name, card in cards.items()}, f)


@cli.command()
@click.argument("nametag")
@click.argument("rating")
def rate(nametag, rating):
    pass


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
            name: restdi_card.RestdiCard.from_dict(data)
            for name, data in json.load(f).items()
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
