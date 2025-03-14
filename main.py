from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import user_management as dbHandler
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = dbHandler.retrieveUsers(username)
        
        if user and check_password_hash(user['password'], password):
            session["username"] = username  # Store session data
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
        hashed_password = generate_password_hash(password)
        dbHandler.insertUser(username, hashed_password, dob)
        return redirect(url_for("home"))
    
    return render_template("signup.html")
    
@app.route("/success", methods=["POST", "GET"])
def add_feedback():
    if "username" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
    dbHandler.listFeedback()
    return render_template("success.html", state=True, value="Back")
    
@app.route("/logout")
def logout():
    session.clear()  # Clear session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5050)
