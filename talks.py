import click

from lib.commands.create_series import create_series
from lib.commands.delete_series import delete_series
from lib.commands.delete_sermon_from_graphcool import delete_sermon_from_graphcool
from lib.commands.delete_sermon_from_s3 import delete_sermon_from_s3
from lib.commands.list_graphcool_events import list_graphcool_events
from lib.commands.list_graphcool_sermons import list_graphcool_sermons
from lib.commands.list_graphcool_speakers import list_graphcool_speakers
from lib.commands.list_s3_sermons import list_s3_sermons
from lib.commands.list_series import list_graphcool_series
from lib.commands.show_file_info import show_file_info
from lib.commands.upload_sermon import upload_sermon


@click.group()
def cli():
    pass


cli.add_command(show_file_info)
cli.add_command(upload_sermon)
cli.add_command(delete_sermon_from_s3)
cli.add_command(delete_sermon_from_graphcool)
cli.add_command(list_s3_sermons)
cli.add_command(list_graphcool_sermons)
cli.add_command(list_graphcool_series)
cli.add_command(list_graphcool_speakers)
cli.add_command(list_graphcool_events)
cli.add_command(create_series)
cli.add_command(delete_series)

if __name__ == '__main__':
    cli()
