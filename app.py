from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash
app = Flask(__name__)
app.secret_key = "secretkuuygkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"
mongo = PyMongo(app)


@app.route('/user/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']
    _phone = _json['phone']
    _gender = _json['gender']

    if _name and _email and _password and _phone and _gender and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert({'name': _name, 'email': _email, 'password': _hashed_password, 'phone': _phone, 'gender': _gender})
        resp = jsonify("User details added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'NOt Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/search/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Particular user details deleted successfully")
    resp.status_code = 200
    return resp


@app.route('/user/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']
    _phone = _json['phone']
    _gender = _json['gender']
    if _name and _email and _password and _phone and _gender and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid'])if'$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'phone': _phone, 'password': _hashed_password, 'gender': _gender}})
        resp = jsonify("Particular user details updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()


if __name__ == "__main__":
    app.run(debug=True)
