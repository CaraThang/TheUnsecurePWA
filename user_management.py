import sqlite3 as sql
import time
import random


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, password, DoB),
    )
    con.commit()
    con.close()

def retrieveUsers(username):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    user = cur.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    con.close()
    # Plain text log of visitor count as requested by Unsecure PWA management 
    with open("visitor_log.txt", "r") as file:
        number = int(file.read().strip())
        number += 1
    with open("visitor_log.txt", "w") as file:
        file.write(str(number))

    if user:
        return {"password": user[0]}  # Return hashed password
    return None # Return None if user doesn't exist

def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
