from pymongo import MongoClient
import certifi
from flask import request, render_template, send_file 
from tasteofnostalgia import APP

from tasteofnostalgia import users
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://onlineuser:$k25DsumFLfXEtF@discord-bot-online-judg.7gm4i.mongodb.net/"

# Create a new client and connect to the server
# client = MongoClient(uri)
# db = client['taste-of-nostalgia',]
# users = db['users']

# users.insert_one({"name": "Alisa"})

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

client = MongoClient("mongodb+srv://onlineuser:$k25DsumFLfXEtF@discord-bot-online-judg.7gm4i.mongodb.net/", tlsCAFile=certifi.where())['taste-of-nostalgia']

#users = client['users']
#users.find_one({"name": "Alisa", "age": 18})