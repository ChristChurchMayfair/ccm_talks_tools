import os
import mutagen
from mutagen.id3 import ID3
from datetime import datetime
import re

REGEX="(\d{4})_(\d{1,2})_(\d{1,2})_(\d?[AP]M).*"

class Sermon:

    public_url = ""

    def __init__(self, audio_file_path):
        self.local_audio_file_path = audio_file_path
        self.file_name = os.path.basename(self.local_audio_file_path)
        id3_data = ID3(audio_file_path)
        file_data = mutagen.File(audio_file_path)

        self.name = id3_data["TIT2"].text[0]
        self.speaker_name = id3_data["TPE1"].text[0]
        self.series_name = id3_data["TALB"].text[0]

        self.duration_in_seconds = int(file_data.info.length)

        matches = re.search(REGEX, self.file_name, re.IGNORECASE)

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
            elif service == "6PM":
                hour = 18
                minute = 0


            self.preachedAt = datetime(year=year,month=month,day=day,hour=hour,minute=minute,tzinfo=None,fold=0).isoformat()



    def as_dict(self):
        return {
            "name": self.name,
            "preachedAt": self.preachedAt,
            "duration": self.duration_in_seconds,
            "passage": self.passage,
            "url": self.public_url
        }


    def __str__(self):
        title = "Filename: {}".format(self.file_name)
        duration = "Duration: {} seconds".format(self.duration_in_seconds)
        speaker = "Speaker: {}".format(self.speaker_name)
        series = "Series: {}".format(self.series_name)
        title = "Title: {}".format(self.name)

        return "\n".join([title, duration, speaker, series])

