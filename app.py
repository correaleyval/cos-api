from getdata import *

from flask import Flask, jsonify

from flask_cors import CORS

from flask_pymongo import PyMongo
mongo = PyMongo()

app = Flask(__name__)

config_object = 'settings'
app.config.from_object(config_object)

CORS(app)

mongo.init_app(app)

@app.route('/')
def index():
    return jsonify(getdata())

def get_user_api(name):
    return "https://api.github.com/users/{}?client_id={}&client_secret={}".format(
        name,
        app.config['CLIENT_ID'],
        app.config['CLIENT_SECRET']
    )

def get_repo_api(user, repo):
    return "https://api.github.com/repos/{}/{}?client_id={}&client_secret={}".format(
        user,
        repo,
        app.config['CLIENT_ID'],
        app.config['CLIENT_SECRET']
    )

import requests

@app.route('/sync')
def sync():
    user_collection = mongo.db.users
    user_collection.drop()

    repo_collection = mongo.db.repos
    repo_collection.drop()

    data = getdata()

    user_list = list()
    repo_list = list()

    for user in data:
        res = requests.get(get_user_api(user['name']))
        user_list.append(res.json())

        for repo in user['repos']:
            res = requests.get(get_repo_api(user['name'], repo))

            print(res.json())
            repo_list.append(res.json())

    user_collection.insert_many(user_list)
    repo_collection.insert_many(repo_list)

    return jsonify({
        'message': 'sync ok'
    })

from bson.json_util import dumps

@app.route('/users')
def users():
    collection = mongo.db.users

    users = dumps( collection.find({}) )

    return jsonify({
        'users': json.loads(users)
    })

@app.route('/repos')
def repos():
    collection = mongo.db.repos

    repos = dumps( collection.find({}) )

    return jsonify({
        'repos': json.loads(repos)
    })

if __name__ == '__main__':
    app.run(debug=True)
