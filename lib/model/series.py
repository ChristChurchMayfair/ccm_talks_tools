class Series:
    name = None
    subtitle = None
    id = None
    image3x2url = None
    sernons = []

    def __init__(self, data):
        self.name = data['name']
        self.subtitle = data['subtitle']
        self.id = data['id']
        self.image3x2url = data['image3x2Url']
        self.sermons = data['sermons']

    @classmethod
    def fromGraphCoolData(cls, graphcoolSeries):
        data = {
            'name': graphcoolSeries['name'],
            'subtitle': graphcoolSeries['subtitle'],
            'id': graphcoolSeries['id'],
            'image3x2Url': graphcoolSeries['image3x2Url'],
            "sermons" : graphcoolSeries['sermons']
        }
        return cls(data)

    def one_line(self):
        return "{:<50} {:<40} {:>5} sermon(s)   {:<15}".format(self.name, self.subtitle, len(self.sermons), self.id)
