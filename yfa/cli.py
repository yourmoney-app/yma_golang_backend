import os
import sys
import click
import subprocess

from yfa import __version__


@click.group()
@click.version_option(version=__version__)
def yfa_cli():
    """Command-line interface to YFA."""
    from yfa.logging import configure_logging

    configure_logging()


@yfa_cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option("--db", type=click.Choice(["core", "user"]))
@click.pass_context
def alembic(ctx, db: str):
    print(f"Type: {db}")
    exec_args = [
        sys.executable,
        "-m", "alembic",
        "--name", db,
        "-c", os.path.join(os.path.dirname(__file__), "alembic.ini"),
        *ctx.args,
    ]
    print(" ".join(exec_args))
    subprocess.run(exec_args)


# @alembic.command()
# def migrate_all_tenants():
#     pass


# @alembic.command()
# @click.option("--user-id")
# def migrate_tenant(user_id):
#     pass


def entrypoint():
    """The entry that the CLI is executed from"""
    from yfa.exceptions import YFAException

    try:
        yfa_cli()
    except YFAException as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
