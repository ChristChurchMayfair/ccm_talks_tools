from mutagen.id3 import ID3
import click
import mutagen
import boto3
import yaml
import json
from sermon import Sermon
import datetime
from graphql_queries import *

from graphqlclient import GraphQLClient


@click.group()
def cli():
    pass


def upload_to_s3(filename, bucket, awscredsfile, prefix_dir, force=False):
    print("Checking for {} in S3".format(filename))

    aws_creds = get_aws_credentials(awscredsfile)

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_creds['AccessKeyId'],
                      aws_secret_access_key=aws_creds['SecretAccessKey'])

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
        s3.upload_file(filename, bucket, sermon_bucket_path)
        print("Done")
        print("Making public...", end='', flush=True)
        s3.put_object_acl(Bucket=bucket, Key=sermon_bucket_path, ACL="public-read")
        print("Done")

    return "https://s3.eu-west-1.amazonaws.com/{}/{}".format(bucket, sermon_bucket_path)


def get_aws_credentials(awscredsfile):
    aws_creds = yaml.load(open(awscredsfile))
    if ('AccessKeyId' not in aws_creds) or ('SecretAccessKey' not in aws_creds):
        exit(1)
    return aws_creds


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

        print(sermon.as_dict())

        create_sermon_result = client.execute(create_sermon(), sermon.as_dict())

        print(create_sermon_result)

        return "newid"
    else:
        print("It's already in graphcool")
        print(parsed_json['data']['Sermon'])
        return parsed_json['data']['Sermon']['id']


@click.command()
@click.argument('filename')
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--prefix', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='A file containing AWS credentials.')
def upload(filename, bucket, awscredsfile, graphcoolcredsfile, graphcoolserviceid, prefix):
    sermon = Sermon(filename)

    s3_url = upload_to_s3(sermon.file_name, bucket, awscredsfile, prefix)

    sermon.public_url = s3_url

    print("File now available at: {}".format(sermon.public_url))

    sermon_id = upload_to_graphcool(sermon, graphcoolcredsfile, graphcoolserviceid, s3_url)

    sermon.graphcool_id = sermon_id

    print(sermon.graphcool_id)


@click.command()
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--directory', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--searchprefix', default="")
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
def list_s3_sermons(awscredsfile, bucket, directory, searchprefix):
    print("Listing files in S3 in {} under {} matching {}".format(bucket, directory, searchprefix))

    aws_creds = get_aws_credentials(awscredsfile)

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_creds['AccessKeyId'],
                      aws_secret_access_key=aws_creds['SecretAccessKey'])

    sermon_bucket_path = "{}/{}".format(directory, searchprefix)

    list_objects = s3.list_objects(Bucket=bucket, Prefix=sermon_bucket_path)

    if "Contents" in list_objects:
        for object in list_objects['Contents']:
            print(object['Key'])

    else:
        print("There was a problem")


@click.command()
@click.argument('filename')
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--prefix', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
def delete_from_s3(filename, awscredsfile, bucket, prefix):
    aws_creds = get_aws_credentials(awscredsfile)

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_creds['AccessKeyId'],
                      aws_secret_access_key=aws_creds['SecretAccessKey'])

    object_path = "{}/{}".format(prefix, filename)

    print("Deleting {} from {}".format(object_path, bucket))
    print("Deleting...", end='', flush=True)
    s3.delete_object(Bucket=bucket, Key=object_path)
    print("Done")


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


@click.command()
@click.argument('filename')
def showtags(filename):
    print(filename)
    print()

    from mutagen.easyid3 import EasyID3
    print(EasyID3.valid_keys.keys())

    file_data = mutagen.File(filename)

    print("Technical Data")
    print("--------------")
    print(file_data.info.pprint())
    id3_data = ID3(filename)

    non_printable_tags = ['APIC:']

    print()
    print("Raw ID3 Tags")
    print("------------")
    printable_id3_tags = [key for key in id3_data.keys() if key not in non_printable_tags]

    for printable_tag in printable_id3_tags:
        print("{} : \"{}\"".format(printable_tag, id3_data[printable_tag]))

    for non_printable_tag in non_printable_tags:
        if non_printable_tag in list(id3_data.keys()):
            print("{}: NOT PRINTABLE".format(non_printable_tag))

    sermon = Sermon(filename)
    print()
    print("Sermon Mapping")
    print("--------------")
    print(sermon)
    print()


cli.add_command(showtags)
cli.add_command(upload)
cli.add_command(delete_from_s3)
cli.add_command(delete_from_graphcool)
cli.add_command(list_s3_sermons)

if __name__ == '__main__':
    cli()
