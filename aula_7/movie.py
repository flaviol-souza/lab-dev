from datetime import datetime 

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

    def _is_list_empty_validation(self, json, att_name):
        if not att_name in json or json[att_name] is None \
            or not isinstance(json[att_name], list) \
            or len(json[att_name]) == 0 or '' in json[att_name]:
            raise ValueError(f"The attribute {att_name} is empty")
        
        return json[att_name]

    def _is_runtime_validation(self, json, att_name):
        if not att_name in json or json[att_name] is None \
            or not isinstance(json[att_name], int) or json[att_name] <= 0:
            raise ValueError(f"The attribute {att_name} is invalid!")
        return json[att_name]

    def _is_text_empty_validation(self, json, att_name):
        if not att_name in json or json[att_name] is None \
            or not json[att_name].strip():
            raise ValueError(f"The attribute {att_name} is invalid!")
        return json[att_name]
    
    def _is_year_validation(self, json, att_name):
        current_year = datetime.now().year
        if not att_name in json or json[att_name] is None \
            or not isinstance(json[att_name], int) \
            or json[att_name] < 1900 or json[att_name] > current_year:
            raise ValueError(f"The attribute {att_name} is invalid!")
        return json[att_name]
    
    def ratingMean(self):
        rating = 0.0
        if len(self.rating) > 0:
            rating = sum(self.rating) / len(self.rating)
        return rating

    def fromJson(self, json): 
        self.title = self._is_text_empty_validation(json, 'title')
        self.summary = self._is_text_empty_validation(json, 'summary')
        self.runtime = self._is_runtime_validation(json, 'runtime')
        self.actors = self._is_list_empty_validation(json, 'actors')
        self.year = self._is_year_validation(json, 'year')
        self.gender = self._is_text_empty_validation(json, 'gender')

    def fromModel(self, movie): 
        self.title = movie.title
        self.summary = movie.summary
        self.runtime = movie.runtime
        self.actors = movie.actors
        self.year = movie.year
        self.gender = movie.gender

    def toJson(self):
        json = self.__dict__.copy()
        json['rating'] = self.ratingMean()
        return json