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


        if (database1 == None):
            return redirect(url_for("user", usr="Invalid", kd="Error"))

        user_index = database1.match.userIndex

        if (database1.match.userTeamColor == 'blue'):
            kd = average_KD(database1.finalData[user_index])
        else:
            kd = average_KD(database1.finalData[user_index + 5])

        kdstr = str(kd)

        print("Database set successfully for \'" + user + "\'.\nTo check data use code \'database1.data_print()\'")
        database1.data_print()
        print("================finished processing=================")
        return redirect(url_for("user", usr=user, kd=kdstr))
    else:
        return render_template("login.html")

@app.route("/<usr>/<kd>")
def user(usr, kd):

    if (usr == "Invalid"):
        return "<h1>Invalid riot ID or region</h1>"

    return "<h1>" + usr + "\'s past 4 game avg kd: " + kd + "</h1>"

if __name__ == "__main__":
    app.run(debug=True)

