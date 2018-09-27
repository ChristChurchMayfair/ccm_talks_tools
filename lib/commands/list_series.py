import json

import click
import yaml
from graphqlclient import GraphQLClient

from lib.graphql_queries import list_series
from lib.model.series import Series


@click.command()
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
@click.option('--count', default=200, help='The number of series to show')
def list_graphcool_series(graphcoolcredsfile, graphcoolserviceid, count):

    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))
    client.inject_token(graphcool_creds['graphcooltoken'])

    series_list_result = json.loads(client.execute(list_series(), {"number": count}))

    if series_list_result['data']:
        series_data = series_list_result['data']['allSeries']

        series_list = map(lambda series: Series.fromGraphCoolData(series), series_data)

        for series in series_list:
            print(series.one_line())

    else:
        print("No data returned!")
