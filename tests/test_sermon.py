import json
import os
import unittest

from lib.model.sermon import Sermon


class TestSermonInit(unittest.TestCase):

    def testCreationFromFile(self):
        path_to_test_mp3 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        "resources/2018_08_05_6PM_John_8v12-59_James_Kight.mp3")
        test_sermon = Sermon.fromFile(path_to_test_mp3)

        self.assertEqual(test_sermon.name, "The Truth that sets you free")
        self.assertEqual(test_sermon.event, "Evening Service")
        self.assertEqual(test_sermon.passage, "John 8:12-59")
        self.assertEqual(test_sermon.speaker_name, "James Kight")

        self.assertEqual(test_sermon.event_id, None)
        self.assertEqual(test_sermon.public_url, None)

    def testCreationFromGraphCoolData(self):
        graphcool_sermon_string = """{
            "duration": 2607,
            "series": {
              "id": "seriesid",
              "name": "All One in Jesus Christ"
            },
            "name": "Safe with him to the praise of his glory",
            "url": "https://s3.eu-west-1.amazonaws.com/media.christchurchmayfair.org/talks/2018_09_16_6PM_Ephesians_1v11-14_Matt_Fuller.mp3",
            "event": {
              "id": "eventid",
              "name": "Evening Service"
            },
            "id": "cjm7nkllx0lxb0195by3z1qkz",
            "passage": "Ephesians 1:11-14",
            "preachedAt": "2018-09-16T18:00:00.000Z",
            "speakers": [
              {
                "id": "speakerid",
                "name": "Matt Fuller"
              }
            ]
        }"""

        asData = json.loads(graphcool_sermon_string)

        test_sermon = Sermon.fromGraphCoolData(asData)

        self.assertEqual(test_sermon.name, "Safe with him to the praise of his glory")
        self.assertEqual(test_sermon.speaker_name, "Matt Fuller")
        self.assertEqual(test_sermon.speaker_ids, ["speakerid"])
        self.assertEqual(test_sermon.public_url, "https://s3.eu-west-1.amazonaws.com/media.christchurchmayfair.org/talks/2018_09_16_6PM_Ephesians_1v11-14_Matt_Fuller.mp3")
        self.assertEqual(test_sermon.file_name, "2018_09_16_6PM_Ephesians_1v11-14_Matt_Fuller.mp3")
        self.assertEqual(test_sermon.event, "Evening Service")
        self.assertEqual(test_sermon.event_id, "eventid")
        self.assertEqual(test_sermon.passage, "Ephesians 1:11-14")
        self.assertEqual(test_sermon.series_name, "All One in Jesus Christ")
        self.assertEqual(test_sermon.series_id, "seriesid")
        self.assertEqual(test_sermon.id, "cjm7nkllx0lxb0195by3z1qkz")
        self.assertEqual(test_sermon.duration_in_seconds, 2607)
