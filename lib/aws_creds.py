import yaml


def get_aws_credentials(awscredsfile):
    aws_creds = yaml.load(open(awscredsfile))
    if ('AccessKeyId' not in aws_creds) or ('SecretAccessKey' not in aws_creds):
        exit(1)
    return aws_creds