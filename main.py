from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import user_management as dbHandler
from dotenv import load_dotenv
import os

# Loads environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  
# Note: App MUST have an .env file with a set secret key variable 

@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"] # Gets user input
        user = dbHandler.retrieveUsers(username) # Calls function to get user data from database
        
        # Cross checking if user input = database data
        if user and check_password_hash(user['password'], password):
            session["username"] = username  # Stores session data
            return redirect(url_for("add_feedback"))
        else:
            return render_template("index.html")

    return render_template("index.html")
    
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        dob = request.form["dob"]
        hashed_password = generate_password_hash(password) # Hashes the password user inputted 
        dbHandler.insertUser(username, hashed_password, dob) # Calls function to insert data into database
        return redirect(url_for("home"))
    
    return render_template("signup.html")
    
@app.route("/success", methods=["POST", "GET"])
def add_feedback():
    if "username" not in session:
        return redirect(url_for("home")) # Session checking 

    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback) # Calls function to insert data into database
    dbHandler.listFeedback() # Writes feedback from database onto the html 
    return render_template("success.html", state=True, value="Back")
    
@app.route("/logout")
def logout():
    session.clear()  # Clear session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5050)
