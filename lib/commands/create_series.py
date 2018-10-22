import click
import yaml
import json

from graphqlclient import GraphQLClient

from lib.commands.upload_sermon import upload_to_s3
from lib.graphql_queries import find_series_by_name, create_series_query
from lib.model.series import Series


@click.command()
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--prefix', default="series-images", help='The name of the S3 bucket to upload to.')
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolcredsfile', default=".graphcoolcreds.yml", help='A file containing AWS credentials.')
@click.option('--graphcoolserviceid', default="cjkqvvoxy2pyy0175cdmdy1mz", help='The service ID for graphcool')
@click.option('--default-image', 'image_file', flag_value='__default__')
@click.option('--image-file', help='A file containing the image for the series.')
@click.option('--series-name', required=True, help='The name of the series.')
@click.option('--series-subtitle', required=True, help='The series subtitle - typically the book or passage')
def create_series(series_name, series_subtitle, image_file, bucket, prefix, awscredsfile, graphcoolcredsfile,
                  graphcoolserviceid):
    series = Series.fromBasic(series_name, series_subtitle)

    if image_file is None:
        print("You need to specify an image file or set the default-image flag")
        exit(1)

    s3_url = None
    if image_file != "__default__":
        s3_url = upload_to_s3(image_file, bucket, awscredsfile, prefix)

    series.image3x2url = s3_url

    graphcool_creds = yaml.load(open(graphcoolcredsfile))

    client = GraphQLClient('https://api.graph.cool/simple/v1/{}'.format(graphcoolserviceid))

    client.inject_token("Bearer " + graphcool_creds['graphcooltoken'])

    # Look up the series by it's name (which is unique in graphcool)
    result = client.execute(find_series_by_name(), {"name": series.name})

    parsed_json = json.loads(result)

    if parsed_json['data']['Series'] is None:

        creation_result = client.execute(create_series_query(), series.asDict())
        print(json.loads(creation_result))
    else:
        print("Series by this name already exists.")
