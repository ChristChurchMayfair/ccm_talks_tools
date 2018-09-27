import json

import click
import yaml
from graphqlclient import GraphQLClient

from lib.graphql_queries import list_speakers
from lib.model.speaker import Speaker


@click.command()
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
@click.option('--count', default=200, help='The number of series to show')
def list_graphcool_speakers(graphcoolcredsfile, graphcoolserviceid, count):

    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))
    client.inject_token(graphcool_creds['graphcooltoken'])

    speaker_list_results = json.loads(client.execute(list_speakers(), {"number": count}))

    if speaker_list_results['data']:
        speakers_data = speaker_list_results['data']['allSpeakers']

        speakers_list = map(lambda speaker: Speaker.fromGraphCoolData(speaker), speakers_data)

        for speaker in speakers_list:
            print(speaker.one_line())

    else:
        print("No data returned!")
