"""Command-line util for OS2Phonebook."""
import os
import sys
import click
from os2phonebook import helpers
from os2phonebook.bootstrap import import_from_os2mo, store_cache
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


@cli.command()
@click.option(
    "--cache-only/--not-cache-only", default=False, help="Store cached content"
)
def start_import(cache_only):
    """Import data from the OS2MO service api

    To invoke the import procedure,
    run the following command:

        python cli.py start-import

    Use the "--cache-only" option to import from backup
    or otherwise migrated files directly.

    """

    config = helpers.config_factory()

    cache_root = config["OS2PHONEBOOK_CACHE_ROOT"]
    log_root = config["OS2PHONEBOOK_LOG_ROOT"]

    log = helpers.log_factory()
    helpers.configure_logging(log_root, "import.log", log)

    # Hello
    click.echo("Import procedure invoked")
    click.echo("Please refer to the import log regarding the progress")
    click.echo(f"View the log file: {log_root}/import.log")

    # Output file names
    map_org_units = os.path.join(cache_root, "map_org_units.json")
    map_employees = os.path.join(cache_root, "map_employees.json")

    try:
        # Inelegant conditional
        # but I'm really lazy...
        if not cache_only:
            import_from_os2mo(config, map_employees, map_org_units)

        store_cache(config, map_employees, map_org_units)
    except Exception as error:
        click.echo(f"ERROR - {error}")
        click.echo("Import procedure incomplete - Exiting!")
        sys.exit(1)

    click.echo("Import procedure completed - Exiting!")


if __name__ == "__main__":
    cli()
