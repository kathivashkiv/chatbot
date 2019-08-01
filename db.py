"MongoDB initioalisation"
import pymongo
from pymongo import MongoClient

mongo = MongoClient()
db = mongo['chatbot']
requests_col = db['requests']
merchants_col = db['merchants']
admins_col = db['admins']
