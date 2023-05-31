from flask import Flask, redirect, url_for, render_template, request
from user_interface import *

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # we have the user inputted data now stored in the user and region variables
        user = request.form["nm"]
        region = request.form["region"]
        database1 = process_data(user, region)
        user_index = database1.match.userIndex

        if (database1.match.userTeamColor == 'blue'):
            kd = database1.match.blueTeam[user_index].kills / database1.match.blueTeam[user_index].deaths
        else:
            kd = database1.match.redTeam[user_index].kills / database1.match.redTeam[user_index].deaths

        kd = round(kd, 2)
        kdstr = str(kd)

        print("Database set successfully for \'" + user + "\'.\nTo check data use code \'database1.data_print()\'")
        print("================finished processing=================")
        return redirect(url_for("user", usr=user, kd=kdstr))
    else:
        return render_template("login.html")

@app.route("/<usr>/<kd>")
def user(usr, kd):
    return "<h1>" + usr + "\'s most recent match kd: " + kd + "</h1>"

if __name__ == "__main__":
    app.run(debug=True)

