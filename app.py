import smtplib
from flask import Flask, Response, make_response, redirect, render_template, json, jsonify, request, session 
from flask_mail import Mail, Message
from random import *
from itsdangerous import BadTimeSignature, Serializer, URLSafeSerializer, URLSafeTimedSerializer, BadSignature, SignatureExpired
import mysql.connector
from flask_cors import CORS
import static.sql.queries as queries

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'grocery',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'otpgenerator'
CORS(app)
serealizer = URLSafeTimedSerializer('SecretKey')

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'tejaswtest@gmail.com'          
app.config['MAIL_PASSWORD'] = 'ijpjdsnuiolluutt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def render_home():
    return render_template('home.html')

@app.route("/signup")
def render_signup():
    return render_template('signup.html')

@app.route('/verifyOtp', methods=["POST"])
def verify():
    req = request.get_json()
    token = req['otp']
    email_from = req['email']
    print(token, email_from)
    try:
        email = serealizer.loads(token, max_age = 120)
        if email!=email_from:
            return make_response(jsonify({"message": "We could not verify your email address with this token"}), 401)
    except SignatureExpired:
        return make_response(jsonify({"message": "The token has expired. Request for a new token"}), 410)
    except BadSignature:
        return make_response(jsonify({"message":"We could not verify your email address with this token"}), 401)
    return make_response(jsonify({"message": "Verification Successful"}), 200)


@app.route("/createAccount", methods=['POST'])
def addUser():
    query = queries.addUser.format(**request.form)
    cursor.execute(query)
    cnx.commit()
    return redirect('/login')

@app.route("/addAddress", methods=['GET', 'POST'])
def addAddress():
    if request.method == 'GET':
        return render_template('address.html')
    else:
        pass
       

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print(request)
        return render_template("login.html")
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        if str(json.loads(checkIfPwdIsForEmail(pwd, email))[0]['matched'])=='0':
            return render_template('login.html', error="Invalid Credentials")
        else:
            session['user_id'] = int(json.loads(getId(email))[0]['id'])
            return redirect('shop.html')

@app.route("/shop", methods=['GET'])
def shop():
    if 'user_id' in session:
        return render_template("shop.html")
    else:
        return redirect("/login")


@app.route("/sendOtp/<email>", methods=['GET'])
def check(email):
    found = json.loads(doesExist(email))[0]['found']
    if found==0:
        token = serealizer.dumps(email)
        msg = Message(subject='OTP For Email Verification', sender='tejaswtest@gmail.com', recipients=[email])
        msg.body= f"Dear FRESCO customer, please enter the following OTP to verify your email address {token}"
        msg.html = render_template("mail.html", otp = token)
        try:
            mail.send(msg)
        except smtplib.SMTPRecipientsRefused:
            return make_response(jsonify({"message": "Email address not found"}), 510)
    else:
            return make_response(jsonify({"message": "An account is already registered with this email id"}), 422)
    return make_response(jsonify({"message": "An OTP has been sent to the email address"}), 200)

def executeQuery(query):
    cursor.execute(query)
    result = cursor.fetchall()
    sequence = cursor.column_names
    result_list = []
    for row in result:
        temp_dict = dict()
        for count in range(len(sequence)):
            temp_dict[sequence[count]] = row[count]
        result_list.append(temp_dict)
    return json.dumps(result_list)

@app.route("/getStates", methods=['GET'])
def getStates():
    return executeQuery(queries.getStates)

@app.route("/getCities/<state>", methods=['GET'])
def getCities(state):
    return executeQuery(queries.getCities.format(state))

@app.route("/doesExist/<email>", methods=['GET'])
def doesExist(email):
    return executeQuery(queries.doesExist.format(email))

@app.route("/checkIf/<pwd>/IsFor/<email>")
def checkIfPwdIsForEmail(pwd, email):
    return executeQuery(queries.checkIfPwdIsForEmail.format(pwd = pwd, email = email))

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.route("/getProducts", methods=['GET'])
def getProducts():
    return executeQuery(queries.getProducts)

@app.route("/getId/<email>", methods=['GET'])
def getId(email):
    return executeQuery(queries.getId.format(email=email))
if __name__ == '__main__':
    app.run(debug=True)

cnx.close()