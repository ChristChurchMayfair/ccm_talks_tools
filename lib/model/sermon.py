import os
import mutagen
from mutagen.id3 import ID3
from datetime import datetime
import re

REGEX = "(\d{4})_(\d{1,2})_(\d{1,2})_(\d?[AP]M).*"


class Sermon:
    id = None
    public_url = None
    speaker_ids = []
    event_id = ""
    series_id = ""
    passage = None
    preachedAt = None
    duration_in_seconds = 0;

    def __init__(self, data):

        self.duration_in_seconds = data['duration_in_seconds']
        self.id = data['id']
        self.name = data['name']

        self.event = data['event']
        self.event_id = data['event_id']

        self.passage = data['passage']

        self.series_name = data['series_name']
        self.series_id = data['series_id']
        self.preachedAt = data['preachedAt']

        self.speaker_name = data['speaker_name']
        self.speaker_ids = data['speaker_ids']

        self.public_url = data['public_url']
        self.file_name = data['file_name']
        self.local_audio_file_path = data['local_audio_file_path']

    @classmethod
    def fromFile(cls, filename):
        data = {}

        ##Things that will be none because we're not coming from graphcool or S3
        data['event_id'] = None
        data['speaker_ids'] = None
        data['series_id'] = None
        data['public_url'] = None

        data['local_audio_file_path'] = filename
        data['file_name'] = os.path.basename(data['local_audio_file_path'])
        id3_data = ID3(filename)
        file_data = mutagen.File(filename)

        data['name'] = id3_data["TIT2"].text[0]
        data['speaker_name'] = id3_data["TPE1"].text[0]
        data['series_name'] = id3_data["TALB"].text[0]

        data['duration_in_seconds'] = int(file_data.info.length)

        title_parts = data['name'].split(" - ")

        if len(title_parts) == 2:
            data['name'] = title_parts[1]
            data['passage'] = title_parts[0]

        matches = re.search(REGEX, data['file_name'], re.IGNORECASE)

        if matches:
            year = int(matches.group(1))
            month = int(matches.group(2))
            day = int(matches.group(3))
            service = matches.group(4)
            hour = 0
            minute = 0

            if service == "AM":
                hour = 10
                minute = 15
                data['event'] = "Morning Service"
            elif service == "6PM":
                hour = 18
                minute = 0
                data['event'] = "Evening Service"

            data['preachedAt'] = datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=None,
                                          fold=0).isoformat()
        return cls(data)

    @classmethod
    def fromGraphCoolData(cls, graphcoolSermon):
        data = {}
        data['id'] = graphcoolSermon['id']
        data['name'] = graphcoolSermon['name']
        data['event'] = graphcoolSermon['event']['name']
        data['event_id'] = graphcoolSermon['event']['id']
        data['series_name'] = graphcoolSermon['series']['name']
        data['series_id'] = graphcoolSermon['series']['id']
        data['duration_in_seconds'] = graphcoolSermon['duration']
        data['passage'] = graphcoolSermon['passage']
        data['preachedAt'] = graphcoolSermon['preachedAt']
        data['speaker_name'] = graphcoolSermon['speakers'][0]['name']
        data['speaker_ids'] = list(map(lambda speaker: speaker['id'], graphcoolSermon['speakers']))
        data['public_url'] = graphcoolSermon['url']
        data['file_name'] = os.path.basename(graphcoolSermon['url'])
        data['local_audio_file_path'] = None
        return cls(data)

    def as_dict(self):
        return {
            "name": self.name,
            "preachedAt": self.preachedAt,
            "duration": self.duration_in_seconds,
            "passage": self.passage,
            "url": self.public_url,
            "speaker_ids": self.speaker_ids,
            "series_id": self.series_id,
            "event_id": self.event_id
        }

    def __str__(self):
        title = "Filename: {}".format(self.file_name)
        duration = "Duration: {} seconds".format(self.duration_in_seconds)
        speaker = "Speaker: {}".format(self.speaker_name)
        series = "Series: {}".format(self.series_name)
        title = "Title: {}".format(self.name)
        passage = "Passage: {}".format(self.passage)
        url = "URL: {}".format(self.public_url)

        return "\n".join([title, duration, speaker, series, passage, url])

    def one_line(self):
        return "{:<50} {:<40} {:<23} {:<15} {:<20} {:<20}".format(self.name, self.series_name, self.passage, self.speaker_name, self.id, self.preachedAt)

