# ruff: noqa: F401
import os
import click
from datetime import datetime
from fsrs import Scheduler, Card, Rating, ReviewLog, State, review_log
import json

CONFIG_FILE = os.path.expanduser("~/Code/python/restdi/restdi.toml")


# TODO: Create a secondary file and populate it with the logic that
# TODO: manages dates.
# TODO: Design main function to take an optional nametag and a rating to
# TODO: rate items and remove them from the list.


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument("nametag", required=False, default=None)
@click.argument("rating", required=False, default=None, type=int)
def cli(ctx):
    pass


# TODO: Write a command to view all items in the list
# TODO: regardless of date
@cli.command()
def all():
    pass


@cli.command()
def new():
    pass


@cli.command()
@click.argument("nametag")
@click.argument("description")
def add(nametag, description):
    pass


@cli.command()
@click.argument("nametag")
@click.argument("description")
def edit(nametag, description):
    pass


@cli.command()
@click.argument("nametag")
def remove(nametag):
    pass


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
