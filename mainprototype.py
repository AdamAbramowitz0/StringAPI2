from flask import Flask, redirect, url_for, request, jsonify, render_template, session
from JSONWorker import JSONWorker
import json
import random
import DBEdit
from Validation import Validation
app = Flask(__name__)
#only thing people can get to without signing in, once signed in, they can go to other urls using a key. I also need to use post requests.
#TODO: signup and then use the<> in the url to pass around their username and passcode and then you can easily make an account for them, https://www.youtube.com/watch?v=aDOSQAq8cls this video has the
#answers to my problems (above comment)

#we need to use machine learning. Should be rather simple


@app.route("/")
def returnFirstPage():
    if 'Username' in session:
        return redirect(url_for('homepage'))
    return render_template("Signinorup.html")

@app.route("/LogIn", methods = ['POST'])
def validateCompany():
    if DBEdit.checkIfCompany(request.args.get('Username'), request.args.get('Password')): #check if a company and then find all of their companies
        return redirect(url_for('/'),True)

@app.route("/SignUp", methods = ['GET', 'POST'])
#SWITCH TO POST!
def validateCompanyThroughEmail():
    x=random.randint(100000,999999)
    Validation.checkEmail(x, request.args.get('SignUsername'))
    print("hi")
    return render_template("EnterCode.html", number=request.args.get('SignUsername'), passcode=request.args.get('SignPassword'))
#redirect to login? First add their uname and pscode to a file (add a company) and THEN you can validate them
#password in use
@app.route("/Validate", methods = ['GET', 'POST'])
#SWITCH TO POST!
def validate():

    print(request.args.get("passcode"))
    print(request.args.get('SignUsername'))
    print("hi")
    if Validation.checkResponse(request.args.get("Code"),request.args.get("SignUsername")):
        DBEdit.addCompany("newCompany", request.args.get("SignUsername"), request.args.get("passcode"))
        return redirect(url_for('LogIn'))
    else:
        return "uh oh"


@app.route("/homepage", methods = ['GET','POST'])
def homepage():
    return render_template("Website.html")


@app.route("/addCompany2",methods = ['GET', 'POST'])
#SWITCH TO POST!
def addCompany(Uname, Pswrd):
    print(request.args)
    print(request.args.get('myKey'), "YOOOOOOOOOOOOOOOOO")

 #TODO: CHANGE THE API STUFF
    apiKey = request.args.get('apiKey')
    nameOfCompany = request.args.get('CompanyName')
    pointsRequired = request.args.get('PointsRequired')
    print(request.args)
    x = JSONWorker('info.json')
    y = company(apiKey, nameOfCompany, pointsRequired,0)
    JSONWorker.addnewcompany(y)
    return json.dumps({'stuff you might need': 'http://127.0.0.1:5000/addPT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam, http://127.0.0.1:5000/addUser?CompanyName=String&apiKey=helloYO&NameOfUser=Adam&PersonWhoRefered=Josh  http://127.0.0.1:5000/removePT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam  ,  ,   http://127.0.0.1:5000/getPT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam'})


# SAMPLE GET REQUEST: http://127.0.0.1:5000/addCompany?myKey=436g2kg6hghg3246&apiKey=helloYO&CompanyName=String&PointsRequired=70
#http://127.0.0.1:5000/addUser?CompanyName=String&apiKey=helloYO&NameOfUser=Adam&PersonWhoRefered=Josh
@app.route("/addUser")

def addUser():
    apiKey = request.args.get('apiKey')
    nameOfCompany = request.args.get('CompanyName')
    nameOfUser = request.args.get('NameOfUser')
    nameOfAdvertiser = request.args.get('PersonWhoRefered')
    print(request.args)
    x = JSONWorker('info.json')
    y = company(apiKey, nameOfCompany,0,0)

    JSONWorker.addnewpersonincompany(nameOfUser, y, nameOfAdvertiser)
    return json.dumps({'status':JSONWorker.addnewpersonincompany(nameOfUser, y,nameOfAdvertiser)})


@app.route("/addPT")
def addPT():
    apiKey = request.args.get('apiKey')
    nameOfCompany = request.args.get('CompanyName')
    nameOfUser = request.args.get('NameOfUser')
    x = JSONWorker('info.json')
    y = nameOfCompany
    z = nameOfUser
    return json.dumps({'status': JSONWorker.addPoint(y,z,apiKey)})
#http://127.0.0.1:5000/addPT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam

@app.route("/removePT")
def removePT():
    apiKey = request.args.get('apiKey')
    nameOfCompany = request.args.get('CompanyName')
    nameOfUser = request.args.get('NameOfUser')
    x = JSONWorker('info.json')
    y = nameOfCompany
    z = nameOfUser
    return json.dumps({'status': JSONWorker.removePoint(y,z,apiKey)})
#http://127.0.0.1:5000/removePT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam

@app.route("/getPT")
def getPT():
    apiKey = request.args.get('apiKey')
    nameOfCompany = request.args.get('CompanyName')
    nameOfUser = request.args.get('NameOfUser')
    x = JSONWorker('info.json')
    y = nameOfCompany
    z = nameOfUser
    return json.dumps({'status': JSONWorker.getPoint(y,z,apiKey)})


#http://127.0.0.1:5000/getPT?CompanyName=String&apiKey=helloYO&NameOfUser=Adam

@app.route("/logout")
def logout():
    x=5

if __name__ == "__main__":
    app.run(debug=True)

#TODO: DB, EC2, CLOUDFLARE, ENCRYPTION FOR DATABASE, fake database names, stripe, ML FOR DB ,AUTHFLOWS


#TODO: TODO: TODO: AHHHH, CHNAGE CODE USERNAME PASSWORD EMAIL SIGNUSERNAME AHHH
#TODO: Website (and css)
#TODO: CODES (both for the user side and also sign in side)
#TODO: SECURITY, swithc to post from get requests? Except for actual get requests, also https, bleh. Maybe at start I dont need this
#TODO: stripe
#We recommend accessing URL parameters with get or by catching the KeyError because users might change the URL and presenting them a 400 bad request page in that case is not user friendly.
#do some digging into sessions. Might be useful for storing password and username. Could aslo just pass it along. IDK
#Company signs up and the website sends an email. The email is validated and then the company is added.
#Then a company adds a user and gives them the ability to generate codes
#Then they give the codes to a friend, who signs up, and now, they are also a user, and the person who signed them up
# a) getspoints
# b) the person who they signed up now has the user of who signed them up
