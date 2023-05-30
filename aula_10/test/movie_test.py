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

def test_get_movie_by_id():
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))

    movie_id = data[-1]['id']
    response = app.test_client().get(f'/movies/{movie_id}')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert data['id'] == movie_id

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

def test_update_movie():
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))
    movie = data[-1]

    payload = {
        "title": movie["title"] + " TEST",
        "gender": movie["gender"] + " TEST",
        "runtime": movie["runtime"] + 60,
        "year": movie["year"]+1,
        "summary": movie["summary"] + " TEST"
    }

    response_put = app.test_client().put(f'movies/{movie["id"]}', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get(f'/movies/{movie["id"]}')
    data = json.loads(response.data.decode('utf-8'))

    assert response_put.status_code == 200
    assert data['id'] == movie['id']
    assert data['title'] != movie['title']
    assert data['gender'] != movie['gender']
    assert data['runtime'] != movie['runtime']
    assert data['year'] != movie['year']
    assert data['summary'] != movie['summary']

def test_vote_movie():
    #Context
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))
    movie_id = data[-1]['id']

    response = app.test_client().get(f'/movies/{movie_id}/rating')
    data_votes = json.loads(response.data)
    response = app.test_client().patch(f'/movies/{movie_id}/rating/{random.uniform(0.0, 10.0)}')
    response = app.test_client().get(f'/movies/{movie_id}/rating')
    data_new_votes = json.loads(response.data)

    assert len(data_votes) + 1 == len(data_new_votes)

def test_delete_movie():
    response = app.test_client().get('/movies')
    data = json.loads(response.data.decode('utf-8'))
    
    response_del = app.test_client().delete(f'movies/{data[-1]["id"]}')

    response = app.test_client().get('/movies')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_del.status_code == 200
    assert len(data) - 1 == len(data_after)
