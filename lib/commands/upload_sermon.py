import json
import os
import pprint

import boto3
import click
import yaml
from graphqlclient import GraphQLClient

from lib.aws_creds import get_aws_credentials
from lib.graphql_queries import find_sermon_by_url, find_series_by_name, find_speaker_by_name, find_event_by_name, \
    create_sermon
from lib.model.sermon import Sermon



@click.command()
@click.argument('filename')
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--prefix', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
def upload_sermon(filename, bucket, awscredsfile, graphcoolcredsfile, graphcoolserviceid, prefix):
    sermon = Sermon(filename)

    s3_url = upload_to_s3(sermon.local_audio_file_path, bucket, awscredsfile, prefix)

    sermon.public_url = s3_url

    print("File now available at: {}".format(sermon.public_url))

    sermon_id = upload_to_graphcool(sermon, graphcoolcredsfile, graphcoolserviceid, s3_url)

    sermon.graphcool_id = sermon_id

    print(sermon.graphcool_id)


def upload_to_s3(file_path, bucket, awscredsfile, prefix_dir, force=False):
    print("Checking for {} in S3".format(file_path))

    aws_creds = get_aws_credentials(awscredsfile)

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_creds['AccessKeyId'],
                      aws_secret_access_key=aws_creds['SecretAccessKey'])

    filename = os.path.basename(file_path)

    sermon_bucket_path = "{}/{}".format(prefix_dir, filename)

    list_objects = s3.list_objects(Bucket=bucket, Prefix=sermon_bucket_path)

    if "Contents" in list_objects:
        if len(list_objects['Contents']) == 1:
            print("File {} already exists in the bucket: {}".format(filename, bucket))
        else:
            print("Multiple files starting with: {}".format(sermon_bucket_path))
    else:
        print("File {} not yet in bucket: {}".format(filename, bucket))
        print("Uploading...", end='', flush=True)
        s3.upload_file(file_path, bucket, sermon_bucket_path)
        print("Done")
        print("Making public...", end='', flush=True)
        s3.put_object_acl(Bucket=bucket, Key=sermon_bucket_path, ACL="public-read")
        print("Done")

    return "https://s3.eu-west-1.amazonaws.com/{}/{}".format(bucket, sermon_bucket_path)


def upload_to_graphcool(sermon, graphcoolcredsfile, graphcoolServiceID, s3_url):
    print("Uploading to Graphcool")

    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolServiceID))

    client.inject_token(graphcool_creds['graphcooltoken'])

    # Look up the sermon by it's URL (which is unique in graphcool)
    result = client.execute(find_sermon_by_url(), {"url": sermon.public_url})

    parsed_json = json.loads(result)

    print(parsed_json)

    if parsed_json['data'] == None:
        print("There was a problem talking to graphcool")
        print(parsed_json['errors'])
        exit(1)
    if parsed_json['data']['Sermon'] == None:
        print("Need to upload the data to graphcool")

        click.echo("Please enter the passages for this talk...")
        click.echo("Use the OSIS format: Book.Chapter.Verse - e.g. John.3.16")
        click.echo("Ranges are specified with a minus/hyphen: e.g. Rev.21.1-10")
        click.echo("Multiple passages can be comma separated. e.g. 2Tim.1.1-3,7-9")
        passage = click.prompt("What is the passage?")

        sermon.passage = passage

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(sermon.as_dict())

        series_search_result = json.loads(client.execute(find_series_by_name(), {"name": sermon.series_name}))

        pp.pprint(series_search_result)

        print(type(series_search_result))

        sermon.series_id = series_search_result['data']['Series']['id']

        speaker_search_result = json.loads(client.execute(find_speaker_by_name(), {"name": sermon.speaker_name}))

        pp.pprint(speaker_search_result)

        sermon.speaker_ids = [speaker_search_result['data']['Speaker']['id']]

        event_search_result = json.loads(client.execute(find_event_by_name(), {"name": sermon.event}))

        pp.pprint(event_search_result)

        sermon.event_id = event_search_result['data']['Event']['id']

        create_sermon_result = json.loads(client.execute(create_sermon(), sermon.as_dict()))

        pp.pprint(create_sermon_result)

        return "newid"
    else:
        print("It's already in graphcool")
        print(parsed_json['data']['Sermon'])
        return parsed_json['data']['Sermon']['id']