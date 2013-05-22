from bson.objectid import ObjectId
from flask import Flask, request
from flask.ext.restful import Resource, Api
from jsonschema import validate, ValidationError
from pymongo import MongoClient


def convert(docs):
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        yield doc


def generate_resource(collection, schema, db):
    class CollectionResource(Resource):
        def get(self, doc_id):
            doc_id = ObjectId(doc_id)
            doc = db[collection].find_one({'_id': doc_id})
            if doc is not None:
                doc['_id'] = str(doc['_id'])
                return doc, 200
            return '', 204

        def put(self, doc_id):
            try:
                validate(request.json, schema)
                doc = request.json
                doc['_id'] = ObjectId(doc_id)
                db[collection].save(doc)
            except ValidationError, ve:
                return str(ve), 400
            return '', 200

    return CollectionResource


def generate_list(collection, db):
    class CollectionList(Resource):
        def get(self):
            docs = db[collection].find()
            return list(convert(docs)), 200
    return CollectionList


class Server(Api):
    def __init__(self, database, host='127.0.0.1', port=27017):
        self.app = Flask(__name__)
        super(Server, self).__init__(self.app)
        self.client = MongoClient(host, port)
        self.db = self.client[database]

    def register_collection(self, collection, schema):
        collection_resource = generate_resource(collection, schema, self.db)
        collection_list = generate_list(collection, self.db)
        self.add_resource(collection_resource, '/%s/<string:doc_id>' % collection)
        self.add_resource(collection_list, '/%s' % collection)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)
