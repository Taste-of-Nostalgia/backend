
# importing Flask and other modules
from flask import Flask, request, jsonify, render_template
from tasteofnostalgia import users, APP
import cohere
from tasteofnostalgia import users
from tasteofnostalgia import food_collection
from tasteofnostalgia.verify import get_user_id
from flask_cors import cross_origin
from bson import Binary

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
            }

            # Insert data into MongoDB
            result = food_collection.insert_one(data)

            # Return a response with the inserted document ID
            return jsonify({"status": "success", 'name': food_name, 'rating': rating, 'photo_path': file_path})
        else:
            return jsonify({"status": "error", "message": "No file uploaded."})
    return render_template("form.html")

@APP.route('/create_user')
def create_user():
    users.insert_one({"email": "test@gmail.com", "password":"password"})
    return jsonify({"status":"OK"})

@APP.route('/get_user')
def get_user():
    return users.find_one({"email": "test@gmail.com", "password":"password"})

@APP.route("/recommendations")
def recommendation():
    co = cohere.Client('BSnGEJ95ZX7mMUasrq7Au6iFXtfz0VkGXrUOxiD2')
    food = ['Spicy Wontons', 'Subway Sandwich', 'Big Mac', 'Pizza Pizza']
    ratings = [1, 4, 3, 4, 5]
    date = ['Jan 25, 2024', 'Jan 20, 2024', 'Jan 15, 2024', 'Jan 10, 2024', 'Jan 5, 2024']
    prompt = "Based on this information, suggest a food similar to one that the user has ranked highly and hasn't eaten recently: "
    for i in range(len(food)):
        prompt+="\n" + food[i] + " - eaten " + date[i] + ": " + ratings[i] + "/5 "
    print("Prompt: " + prompt)
    response = co.generate(prompt=prompt,)
    print("Cohere:" + response)