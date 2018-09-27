import json

import click
import yaml
from graphqlclient import GraphQLClient

from lib.graphql_queries import list_speakers, list_events
from lib.model.event import Event
from lib.model.speaker import Speaker

@click.command()
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
@click.option('--count', default=200, help='The number of series to show')
def list_graphcool_events(graphcoolcredsfile, graphcoolserviceid, count):

    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))
    client.inject_token(graphcool_creds['graphcooltoken'])

    event_list_results = json.loads(client.execute(list_events(), {"number": count}))

    if event_list_results['data']:
        event_data = event_list_results['data']['allEvents']

        events_list = map(lambda event: Event.fromGraphCoolData(event), event_data)

        for event in events_list:
            print(event.one_line())

    else:
        print("No data returned!")
