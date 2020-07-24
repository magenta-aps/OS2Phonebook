"""Command-line util for OS2Phonebook."""
import click
from os2phonebook import helpers
from os2phonebook.bootstrap import ping_datastore


@click.group()
def cli():
    """OS2Phonebook CLI."""
    pass


@cli.command()
@click.option(
    "--max-attempts", default=120, help="Maximum connection attempts"
)
@click.option(
    "--interval", default=5, help="Interval between connects (in seconds)"
)
def pingdb(max_attempts, interval):
    """Test the datastore connection

    Continously ping the datastore until either a connection is established
    or max attempts have been reached.

    """

    config = helpers.config_factory()

    click.echo("Setting up a connection to the datastore")

    for attempt in ping_datastore(config, interval, max_attempts):

        click.echo(attempt)


if __name__ == "__main__":
    cli()
