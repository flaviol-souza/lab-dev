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
        self.rating = []

    def voteRaing(self, vote):
        self.rating.append(vote)

    def ratingMean(self):
        ratingMean = 0
        if len(self.rating) > 0:
            ratingMean = sum(self.rating) / len(self.rating)
        return ratingMean

    def fromJson(self, json):
        self.title = json['title']
        self.summary = json['summary']
        self.runtime = json['runtime']
        self.actors = json['actors']
        self.year = json['year']
        self.gender = json['gender']

    def toJson(self):
        json = self.__dict__.copy()
        json["rating"] = self.ratingMean()
        return json