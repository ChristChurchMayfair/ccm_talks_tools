class Speaker:
    name = None
    id = None
    sernons = []

    def __init__(self, data):
        self.name = data['name']
        self.id = data['id']
        self.sermons = data['sermons']

    @classmethod
    def fromGraphCoolData(cls, graphcoolSeries):
        data = {
            'name': graphcoolSeries['name'],
            'id': graphcoolSeries['id'],
            "sermons": graphcoolSeries['sermons']
        }
        return cls(data)

    def one_line(self):
        return "{:<40} {:>5} sermon(s)   {:<15}".format(self.name, len(self.sermons), self.id)
