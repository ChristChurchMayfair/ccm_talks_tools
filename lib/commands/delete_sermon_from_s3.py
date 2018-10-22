import boto3
import click

from lib.aws_creds import get_aws_credentials


@click.command()
@click.argument('filename')
@click.option('--bucket', default="media.christchurchmayfair.org", help='The name of the S3 bucket to upload to.')
@click.option('--prefix', default="talks", help='The name of the S3 bucket to upload to.')
@click.option('--awscredsfile', default=".awscreds.yml", help='A file containing AWS credentials.')
def delete_sermon_from_s3(filename, awscredsfile, bucket, prefix):
    aws_creds = get_aws_credentials(awscredsfile)

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_creds['AccessKeyId'],
                      aws_secret_access_key=aws_creds['SecretAccessKey'])

    object_path = "{}/{}".format(prefix, filename)

    print("Deleting {} from {}".format(object_path, bucket))
    print("Deleting...", end='', flush=True)
    s3.delete_object(Bucket=bucket, Key=object_path)
    print("Done")
