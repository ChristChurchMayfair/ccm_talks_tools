import click
import yaml
import json
from graphqlclient import GraphQLClient

from lib.graphql_queries import find_series_by_id, delete_series_by_id


@click.command()
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='The service ID for graphcool')
@click.option('--series-id', required=True, help='The id of the series to delete.')
def delete_series(series_id, graphcoolcredsfile, graphcoolserviceid):
    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))

    client.inject_token("Bearer " + graphcool_creds['graphcooltoken'])

    search_result = json.loads(client.execute(find_series_by_id(), {"id": series_id}))

    if search_result['data']['Series'] is None:
        print("No series found with the id: {}".format(series_id))
        exit(1)

    series = search_result['data']['Series']
    sermon_count = len(series['sermons'])

    if sermon_count > 0:
        print("Series \"{}\" contains {} sermons - cascading deleting has not been implemented. Sorry.".format(
            series['name'], sermon_count))
        exit(1)

    deletion_result = json.loads(client.execute(delete_series_by_id(), {"id": series_id}))

    if deletion_result['data']['deleteSeries']:
        print("Deleted series \"{}\"".format(deletion_result['data']['deleteSeries']['name']))
