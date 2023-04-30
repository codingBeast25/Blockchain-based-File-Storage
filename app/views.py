import json
import os
from base64 import encode

import requests
from flask import render_template, redirect, request, send_file, url_for, render_template_string
import bcrypt
from werkzeug.utils import secure_filename
from app import app
from timeit import default_timer as timer
import mysql.connector
from flask import Flask, session

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="saravana"
)
# Stores all the post transaction in the node
request_tx = []
#store filename
files = {}
#destiantion for upload files
UPLOAD_FOLDER = "app/static/Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# store  address
ADDR = "http://127.0.0.1:8800"
app.secret_key = 'SECRET_KEY'

#create a list of requests that peers has send to upload files
def get_tx_req():
    global request_tx
    chain_addr = "{0}/chain".format(ADDR)
    resp = requests.get(chain_addr)
    if resp.status_code == 200:
        content = []
        chain = json.loads(resp.content.decode())
        for block in chain["chain"]:
            for trans in block["transactions"]:
                trans["index"] = block["index"]
                trans["hash"] = block["prev_hash"]
                content.append(trans)
        request_tx = sorted(content, key=lambda k: k["hash"], reverse=True)
# Function to query database for user
def query_user(name):
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE user=%s", (name,))
    user = cursor.fetchone()
    cursor.close()
    return user

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Query the database to check if username exists
        user = query_user(name)
        # If username exists, check if password is correct
        if user:
            hashed_password = user[0]  # retrieve hashed password from database
            # Hash user input password using bcrypt
            # Compare the two hashed passwords
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Passwords match - login successful
                # Redirect to the protected page
                session['name'] = name
                return redirect('/index')
                # Invalid login credentials - show error message
    return render_template("login.html")

@app.route("/index")
def index():
    get_tx_req()
    return render_template("index.html", title="FileStorage", subtitle="A Decentralized Network for File Storage/Sharing", node_address=ADDR, request_tx=request_tx)
# @app.route("/signup")
# def signup():
#     return render_template("Signup.html")

# Define the route that handles the form submission
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # Get the form data
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the user input password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Create a connection to the MySQL database
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (user, password, email) VALUES (%s, %s, %s)", (name, hashed_password, email))
        db.commit()
        cursor.close()

        # Redirect to the login page after successful signup
        return redirect('/login')
    # If the request method is GET, render the signup page
    return render_template('signup.html')

# Loads and runs the home page
# @app.route("/")
# def index():
#     get_tx_req()
#     return render_template("index.html",title="FileStorage",subtitle = "A Decentralized Network for File Storage/Sharing",node_address = ADDR,request_tx = request_tx)

@app.route("/submit", methods=["POST"])
# When new transaction is created it is processed and added to transaction
def submit():
    if 'name' in session:
        start = timer()
        user = request.form["user"]
        up_file = request.files["v_file"]

        #save the uploaded file in destination
        up_file.save(os.path.join("app/static/Uploads/",secure_filename(up_file.filename)))
        #add the file to the list to create a download link
        files[up_file.filename] = os.path.join(app.root_path, "static", "Uploads", up_file.filename)
        #determines the size of the file uploaded in bytes
        file_states = os.stat(files[up_file.filename]).st_size
        #create a transaction object
        post_object = {
            "user": user, #user name
            "v_file" : up_file.filename, #filename
            "file_data" : str(up_file.stream.read()), #file data
            "file_size" : file_states   #file size
        }
        # Submit a new transaction
        address = "{0}/new_transaction".format(ADDR)
        requests.post(address, json=post_object)
        end = timer()
        print(end - start)
        return redirect("/index")
    else:
        return render_template_string('''
               <script>alert('You are not logged in.');</script>
               <p>You are not logged in.</p>
           ''')

#creates a download link for the file
@app.route("/submit/<string:variable>",methods = ["GET"])
def download(variable):
    if 'name' in session:
        p = files[variable]
        return send_file(p,as_attachment=True)
    else:
        return render_template_string('''
               <script>alert('You are not logged in.');</script>
               <p>You are not logged in.</p>
           ''')