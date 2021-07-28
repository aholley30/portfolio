import os
from flask import Flask, render_template, send_from_directory, request, redirect
import csv

app = Flask(__name__) #run a flask app on main file. __name__ = main

#source bin/activate
#export FLASK_ENV=development -> for debugging, changes automatically become active
#export FLASK_APP=server.py
#flask run


@app.route("/") #abstraction at work
def my_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as f:
        email = data["email"]
        message = data["message"]
        subject = data["subject"]
        f.write(f"\n{email},{subject},{message}")

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as f:
        email = data["email"]
        message = data["message"]
        subject = data["subject"]
        csvwriter = csv.writer(f, delimiter=',',quotechar='\'',quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thanks.html')
        except:
            return 'Did not save submission'
    else:
        return "something went wrong"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')