from flask import Flask, request
app = Flask(__name__)

@app.route('/index')
def index():
    return 'Index'

@app.route('/home')
def home():
    return 'Home'

@app.route('/home/subpath')
def subPath():
    return 'Sub-Path'

@app.route('/user/<name>')
def helloUser(name):
    return 'Hello %s.' % name

@app.route('/uid/<int:uid>')
def uid(uid):
    return str(uid)

@app.route('/dic/<newpath>/<int:uid>')
def dic(newpath, uid):
    return newpath + str(uid)

@app.route('/cal')
def cal():
    var1 = request.args.get('var1', default=0, type=int)
    var2 = request.args.get('var2', default=0, type=int)
    r = var1 + var2
    return str(r)

@app.route('/<name>')
def fullName(name):
    option = ''
    lastname = request.args.get('lastname', default='')
    if(lastname):
        option = f' Sobrenome: {lastname}'

    old = request.args.get('old', default=-1, type=int)
    if(old > 0):
        option += f' Idade: {old}'

    return f'Nome: {name} {option}'


if __name__ == '__main__':
    app.run(debug=True)