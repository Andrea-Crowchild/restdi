# ruff: noqa: F401
import os
import click
import tomlkit

CONFIG_FILE = os.path.expanduser("~/Code/python/restdi/restdi.toml")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
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


@cli.command()
@click.argument("location")
def save(location):
    pass
