from flask import Flask, redirect, url_for, render_template, request
from user_interface import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # we have the user inputted data now stored in the user and region variables
        user = request.form["nm"]
        region = request.form["region"]
        database1 = process_data(user, region)
        print("database for \'" + user + "\' set up")
        b1_avg_wr = str(win_percentage(database1.b1))
        return redirect(url_for("user", usr = user, region = region))
    else:
        return render_template("login.html")

@app.route("/<usr><region>")
def user(usr, region):
    return f"<h1>{usr}{region}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

