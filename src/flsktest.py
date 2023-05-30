from flask import Flask, redirect, url_for, render_template
from user_interface import *

app = Flask(__name__)

@app.route("/")
def home():
    database1 = process_data("clu1#NA1", "na")
    b1_avg_wr = str(win_percentage(database1.b1))
    return "<center><h1>VAST</h1></center>\n<center><h1>" + b1_avg_wr + "</h1></center>"

if __name__ == "__main__":
    app.run()

