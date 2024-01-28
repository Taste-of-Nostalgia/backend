
# importing Flask and other modules
from flask import request, render_template, send_file 
from tasteofnostalgia import APP
from flask import jsonify 
from tasteofnostalgia import users
 
# A decorator used to tell the application
# which URL is associated function
@APP.route('/', methods =["GET", "POST"])
def gfg():
   if request.method == "POST":
      foodName = request.form.get("foodName")
      rating = request.form.get("rating") 
      file = request.files.get("file")
      if file:
            file.save("uploads/" + file.filename)
            return "Your food is " + foodName + ". Your rating is " + rating + ". File saved as " + file.filename + "."
      else:
         return "No file uploaded."
   return render_template("form.html")

@APP.route('/create_user')
def create_user():
    users.insert_one({"email": "test@gmail.com", "password":"password"})
    return jsonify({"status":"OK"})

@APP.route('/get_user')
def get_user():
    return users.find_one({"email": "test@gmail.com", "password":"password"})