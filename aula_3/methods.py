from flask import Flask, request
app = Flask(__name__)
users = ['flavio']

@app.route('/users', methods=['GET'])
def getUsers():
    return users

@app.route('/users', methods=['POST'])
def addUser():
    username = request.form['username']
    users.append(username)
    return 'Deu bom'

@app.route('/users/<int:index>', methods=['DELETE'])
def deleteUser(index):
    del users[index]
    return '1 a menos'

@app.route('/users/<int:index>', methods=['PUT', 'PATCH'])
def updateUser(index):
    username = request.form['username']
    users[index] = username
    return 'esta td ok!'

if __name__ == '__main__':
    app.run(debug=True)