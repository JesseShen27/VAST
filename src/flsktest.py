from flask import Flask, redirect, url_for, render_template, request
from user_interface import *

app = Flask(__name__)

@app.route("/")
def home():
    database1 = process_data("clu1#NA1", "na")
    name = request.form.get('name')
    b1_avg_wr = str(win_percentage(database1.b1))
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # we have the user inputted data now stored in the user and id variables
        user = request.form["nm"]
        id = request.form["id"]
        print(user + id)
        return redirect(url_for("user", usr = user, id = id))
    else:
        return render_template("login.html")

@app.route("/<usr><id>")
def user(usr, id):
    return f"<h1>{usr}{id}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

