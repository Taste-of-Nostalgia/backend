
# importing Flask and other modules
from flask import Flask, request, jsonify, render_template
from tasteofnostalgia import users, APP
import cohere
from tasteofnostalgia import users
from tasteofnostalgia import food_collection
from tasteofnostalgia.verify import get_user_id
from flask_cors import cross_origin
from bson import Binary
import json


@APP.route('/userid')
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def userid():
    return f'{get_user_id()}'

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
    # results = [result for result in food_collection.find({"userId": get_user_id()})]
    results = [result for result in food_collection.find({"userId": '65b5ae5bcf5539f8e9c1abcb'})]
    food_name = []
    ratings = []
    date = []
    for j in range(len(results)):
        food_name.append((results[j])['name'])
        ratings.append((results[j])['rating'])
        date.append((results[j])['date'])
    
    info = ''
    for i in range(len(food)):
        info += food_name[i] + " - eaten " + date[i] + ": " + str(ratings[i]) + "/5\n"

    prompt1 = "Based on this information, what is the number 1 food similar to food that the user has ranked highly and hasn't eaten recently (answer with the symbol #1 followed by the food name: description):\n" + info
    prompt2 = "Based on this information, what is the number 1 rated food? (answer with the symbol #1 followed by : and a short description)\n" + info
    prompt3 = "Based on this information, what is the number 1 creative food that is not on the list (answer with the symbol #1 followed by the food name: description):\n" + info 
   
    response1 = co.generate(prompt=prompt1).data[0].text
    response2 = co.generate(prompt=prompt2).data[0].text
    response3 = co.generate(prompt=prompt3).data[0].text

    print("Prompt1: " + prompt1 + "\n" + info)
    print("Response1: " + response1)
    print("Prompt2: " + prompt2 + "\n" + info)
    print("Response2: " + response2)
    print("Prompt3: " + prompt3 + "\n" + info)
    print("Response3: " + response3)

    # Find the index of "1."
    index_of_1_v1 = response1.find("#1")
    index_of_1_v2 = response2.find("#1:")
    index_of_1_v3 = response3.find("#1")

    index_of_2_v1 = response1.find("2.")
    index_of_2_v3 = response3.find("2.")

    titles=[]
    descriptions=[]
    
    if index_of_1_v1 != -1:
            # Find the index of ":"
            index_of_colon = response1.find(":", index_of_1_v1)
            if index_of_colon != -1:
               # Extract the substring starting from "1." to ":"
               titles.append(response1[index_of_1_v1+3:index_of_colon].strip())
               descriptions.append(response1[index_of_colon + 3:index_of_2_v1].strip())
   
    if index_of_1_v2 != -1:
            index_of_colon = response1.find(":", index_of_1_v2)
            if index_of_colon != -1:
               # Extract the substring starting from "1." to ":"
               titles.append(response2[index_of_1_v2+3:index_of_colon].strip())
               descriptions.append(response1[index_of_colon + 2:].strip())

    if index_of_1_v3 != -1:
            # Find the index of ":"
            index_of_colon = response1.find(":", index_of_1_v3)
            if index_of_colon != -1:
                # Extract the substring starting from "1." to ":"
                titles.append(response1[index_of_1_v3+3:index_of_colon].strip())
                descriptions.append(response1[index_of_colon + 3:index_of_2_v3].strip())
    
    data_dict = {key: value for key, value in zip(titles, descriptions)}
   
   # Convert the dictionary to a JSON-formatted string
    json_data = json.dumps(data_dict)
    print(response1 + "\n" + response2 + "\n" + response3)
    return json_data
