
# importing Flask and other modules
from flask import Flask, request, jsonify, render_template
from tasteofnostalgia import users, APP
import cohere
from tasteofnostalgia import users
from tasteofnostalgia import food_collection
from tasteofnostalgia.verify import get_user_id
from flask_cors import cross_origin
from bson import Binary
from datetime import datetime
import time

@APP.route('/userid')
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def userid():
    return f'{get_user_id()}'

def time_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%B %d, %Y")

# A decorator used to tell the application
# which URL is associated function
@APP.route('/input_food', methods=["GET", "POST"])
def input_food():
    if request.method == "POST":
        food_name = request.form.get("foodName")
        rating = int(request.form.get("rating"))  # Convert to integer if needed

        # Save the file to the 'uploads' directory
        file = request.files.get("file")
        if file:
            file_path = "uploads/" + file.filename
            file.save(file_path)

            # Prepare the data to be inserted into MongoDB
            data = {
                'name': food_name,
                'rating': rating,
                'photo': file_path,  # Convert file content to BSON Binary
                'time': int(time.time()),
                'userId': get_user_id()
            }

            # Insert data into MongoDB
            result = food_collection.insert_one(data)

            # Return a response with the inserted document ID
            return jsonify({"status": "success", 'name': food_name, 'rating': rating, 'photo_path': file_path, 'userId': get_user_id()})
        else:
            return jsonify({"status": "error", "message": "No file uploaded.", 'userId': get_user_id()})
    return render_template("form.html")

@APP.route('/create_user')
def create_user():
    users.insert_one({"email": "test@gmail.com", "password":"password"})
    return jsonify({"status":"OK"})

@APP.route('/get_user')
def get_user():
    return users.find_one({"email": "test@gmail.com", "password":"password"})

@APP.route("/recommendations", methods=["GET"])
def recommendation():
    co = cohere.Client('BSnGEJ95ZX7mMUasrq7Au6iFXtfz0VkGXrUOxiD2')
    food = ['Spicy Wontons', 'Subway Sandwich', 'Big Mac', 'Pizza Pizza', 'Ramen Noodles']
    results = [result for result in food_collection.find({"userId": get_user_id()})]
    results[0].name 
    ratings = [1, 4, 3, 4, 5]
    for i in range(len(ratings)):
         if (ratings[i] == 1):
            ratings[i] = "very bad"
         elif (ratings[i] == 2):
            ratings[i] = "bad"
         elif (ratings[i] == 3):
            ratings[i] = "ok"
         elif (ratings[i] == 4):
            ratings[i] = "good"
         else:
            ratings[i] = "very good"
    date = ['Jan 25, 2024', 'Jan 20, 2024', 'Jan 15, 2024', 'Jan 10, 2024', 'Jan 5, 2024']
    prompt = "Based on this information, suggest the top 3 foods similar to one that the user has ranked highly and hasn't eaten recently: "
    info = ''
    for i in range(len(food)):
        info += food[i] + " - eaten " + date[i] + ": " + ratings[i] + "\n"
    print("Prompt: " + prompt + "\n" + info)
    prompt += "\n" + info
    response = co.generate(prompt=prompt).data[0].text
    prompt = "Based on this information, describe the highest rated food? \n" + info
    response2 = co.generate(prompt=prompt).data[0].text

    print("Response 1:" + (response))
    print("Response 2:" + (response))
    return response2