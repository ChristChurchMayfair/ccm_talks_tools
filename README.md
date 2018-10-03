# ccm_talks_tools
Tools for managing CCM sermons

## Setup

(NB this package uses Python3. Depending on you system you may need to use python3 and pip3 instead of python and pip respectively)

Create a virtualenv: `python3 -m venv venv`

Activate the virtualenv: `source venv/bin/activate`

Install requirements: `pip install -r requirements.txt`

## Usage

Run the tool to show commands: `python talks.py`

You can see the way it will interpret the metadata of an `mp3` file using: `python talks.py show_file_info <mp3 file>`

You can upload this file using: `python talks.py upload <mp3 file>`

Files go into an S3 bucket, meta data goes into graphcool. There are commands to list the contents of S3 and GraphCool.

## Credentials

You will need credentials for AWS and GraphCool.

It will automatically look for files called: `.awscreds.yml`

Format:
```
AccessKeyId: "XXXXXXXXXXXXXXXXXXX"
SecretAccessKey: "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
```

and `.graphcoolcreds.yml`

Format:
```
graphcooltoken:  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Credentials can be obtained from the owner of this repo.
