from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/home/')
def home():
    return 'Home'

@app.route('/home/subpath')
def subPath():
    return 'Sub Path Home'

@app.route('/login')
def login():
    page = request.args.get('page', default = 1, type = int)
    return str(page)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/<name>')
def register(name):
    option = ''
    lastname = request.args.get('lastname', default='')
    old = request.args.get('old', default=-1, type=int)
    if(lastname):
        option = f'Sobrenome: {lastname}'

    if(old >= 0):
        option += f' Idade: {old}'
    
    return f'Nome: {name} {option}' 

if __name__ == '__main__':
    app.run()
    #app.run(debug=True, host='0.0.0.0')