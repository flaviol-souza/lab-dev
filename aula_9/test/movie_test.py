import random
from app import app
from flask import json

__CONTENT_TYPE_JSON = 'application/json'

def test_first_test():
    assert True

def test_get_all_movies():
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert len(data) > 0

def test_create_movie():
    payload = {
        "title": "Top Gun",
        "gender": "Action",
        "runtime": 130,
        "year": 2022,
        "summary": "Filme do Tom Cruise"
    }

    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))

    response_post = app.test_client().post('movies/save', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get('/movies')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_post.status_code == 200
    assert len(data) + 1 == len(data_after)

def test_vote_movie():
    #Context
    payload = {
        "title": "Top Gun",
        "gender": "Action",
        "runtime": 130,
        "year": 2022,
        "summary": "Filme do Tom Cruise"
    }
    response = app.test_client().post('movies/save', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))

    print(f'data:{data}')
    print(f'last movie:{data[-1]}')
    print(f'movie id:{data[-1]["id"]}')
    movie_id = data[-1]['id']

    response = app.test_client().get(f'/movies/{movie_id}/rating')
    data_votes = json.loads(response.data)
    response = app.test_client().patch(f'/movies/{movie_id}/rating/{random.uniform(0.0, 10.0)}')
    response = app.test_client().get(f'/movies/{movie_id}/rating')
    data_new_votes = json.loads(response.data)

    assert len(data_votes) + 1 == len(data_new_votes)