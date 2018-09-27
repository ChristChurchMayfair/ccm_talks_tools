import json

import click
import yaml
from graphqlclient import GraphQLClient

from lib.graphql_queries import find_sermons_with_url_ending, delete_sermon


@click.command()
@click.argument('filename')
@click.option('--prefix', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
def delete_from_graphcool(filename, graphcoolcredsfile, graphcoolserviceid, prefix):
    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))

    client.inject_token(graphcool_creds['graphcooltoken'])

    parsed_json = json.loads(client.execute(find_sermons_with_url_ending(), {"url_ends_with": filename}))

    if parsed_json and parsed_json['data']:
        sermons_to_delete = parsed_json['data']['allSermons']

        print("Found {} sermons that match: {}".format(len(sermons_to_delete),filename))

        for sermon in sermons_to_delete:
            delete_result = json.loads(client.execute(delete_sermon(), {'id': sermon['id']}))
            print(delete_result)
