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
        usercolor = database1.match.userTeamColor

        if (usercolor == 'red'):
            user_index += 5

        redKdAvg = get_red_kd_avg(database1.finalData, user_index)
        blueKdAvg = get_blue_kd_avg(database1.finalData, user_index)

        kd = round(average_KD(database1.finalData[user_index]),2)
        kdstr = str(kd)

        print("Database set successfully for \'" + user + "\'.\nTo check data use code \'database1.data_print()\'")
        database1.data_print()
        print("================finished processing=================")
        return redirect(url_for("user", usr=user,kd=kdstr,red_kd=redKdAvg,blue_kd=blueKdAvg,color=usercolor))
    else:
        return render_template("login.html")

@app.route("/<usr>/<kd>/<red_kd>/<blue_kd>/<color>")
def user(usr, kd, red_kd, blue_kd, color):

    if (usr == "Invalid"):
        return "<h1>Invalid riot ID or region</h1>"

    if (color == 'blue'):
        return "<h1>" + usr + "\'s average kd from prior 4 games: " + kd + "</h1>\n<h1>" + usr + "\'s team's average kd from prior 4 games: " + blue_kd + "</h1>\n<h1>Opposing team's average kd from prior 4 games: " + red_kd + "</h1>"
    else:
        return "<h1>" + usr + "\'s average kd from prior 4 games: " + kd + "</h1>\n<h1>" + usr + "\'s team's average kd from prior 4 games: " + red_kd + "</h1>\n<h1>Opposing team's average kd from prior 4 games: " + blue_kd + "</h1>"

if __name__ == "__main__":
    app.run(debug=True)

