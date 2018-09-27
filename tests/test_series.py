import json
import os
import unittest

from lib.model.series import Series


class TestSeriesInit(unittest.TestCase):


    def testCreationFromGraphCoolData(self):
        graphcool_series_string = """{
            "subtitle": "2 Kings 1-8",
            "name": "The Chariots and Horsemen of Israel",
            "sermons": [
                {
                    "preachedAt": "2018-09-09T10:15:11.000Z"
                },
                {
                    "preachedAt": "2018-09-16T10:15:00.000Z"
                }
            ],
            "id": "cjlyd0apo0bqp0102e5yakwhm",
            "image3x2Url": "https://s3.eu-west-1.amazonaws.com/media.christchurchmayfair.org/series-images/2kings-600x400.png"
        }"""

        as_data = json.loads(graphcool_series_string)

        test_series = Series.fromGraphCoolData(as_data)

        self.assertEqual(test_series.name, "The Chariots and Horsemen of Israel")
        self.assertEqual(test_series.subtitle, "2 Kings 1-8")
        self.assertEqual(test_series.id, "cjlyd0apo0bqp0102e5yakwhm")
        self.assertEqual(test_series.image3x2url, "https://s3.eu-west-1.amazonaws.com/media.christchurchmayfair.org/series-images/2kings-600x400.png")
        self.assertEqual(len(test_series.sermons), 2)
