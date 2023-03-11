class Movie():
    _sequence_id = 0

    def __init__(self):
        Movie._sequence_id = Movie._sequence_id + 1
        self.id = Movie._sequence_id
        self.title = ''
        self.summary  = ''
        self.runtime = 0
        self.actors = []
        self.year = 0
        self.gender = ''
        self.rating = 0

    def fromJson(self, json):
        self.title = json['title']
        self.summary = json['summary']
        self.runtime = json['runtime']
        self.actors = json['actors']
        self.year = json['year']
        self.gender = json['gender']
        self.rating = json['rating']

    def toJson(self):
        return self.__dict__