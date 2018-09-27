import boto3
import click

from lib.aws_creds import get_aws_credentials


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