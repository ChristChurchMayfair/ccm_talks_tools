import json
import pprint

import click
import yaml
from graphqlclient import GraphQLClient

from lib.graphql_queries import list_sermons
from lib.model.sermon import Sermon


@click.command()
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
@click.option('--count', default=200, help='The number of sermons to show')
def list_graphcool_sermons(graphcoolcredsfile, graphcoolserviceid, count):
    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))
    client.inject_token(graphcool_creds['graphcooltoken'])

    sermon_list_result = json.loads(client.execute(list_sermons(), {"number": count}))

    if sermon_list_result['data']:
        sermon_data = sermon_list_result['data']['allSermons']

        sermons = map(lambda sermon: Sermon.fromGraphCoolData(sermon), sermon_data)

        for sermon in sermons:
            print(sermon.one_line())

    else:
        print("No data returned!")
