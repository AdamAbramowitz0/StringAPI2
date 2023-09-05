from flask import Flask, session,request,render_template, redirect, url_for, jsonify
import DBEdit
from EmailValidation import sendValidationLink,makeAdamHappy
from random import randint
import stripe
import json, os,sys,requests

app = Flask(__name__)

host = "stringapi.net"

@app.route("/")
def signUp():
    return render_template('Signinorup.html')


@app.route("/validate", methods = ['POST'])
def validate():
    x = randint(0,1000000)
    session["name"] = request.form['name']
    session["password"] = request.form['password']
    session["email"] = request.form['email']

    session["code"] = repr(x)
    print(session["code"])
    sendValidationLink("https://"+ host+"/addCompany?v=" + repr(x), request.form['email'])
    return "In the same browser, check your email for an email from stringapi134@gmail.com (and check spam)"


@app.route("/login", methods = ['POST'])
def login():

    if DBEdit.checkIfCompany(request.form['email'], request.form['password']):
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for('homepage'))
    else:
        return "sorry"

@app.route("/setupguide", methods = ['GET'])
def guide():
    makeAdamHappy()

    return render_template("guide.html")

@app.route("/customersupport", methods = ['GET'])
def support():
    return render_template("customersupport.html")


@app.route("/addCompany", methods = ['GET']) #change to post
def addComp():
    try:
        if request.args.get("v") == session['code']:
            return render_template("index.html")
        return "yo"
    except Exception as e:
        return e

@app.route("/create-checkout-session", methods=["POST"])
def createccs():
    print(request.form)
    price_id = request.form['priceId']
    referralCode = request.form['code']
    sess = stripe.checkout.Session.create(

        success_url="https://" + host + "/successURL",
        cancel_url="https://" + host + "/failURL",
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': price_id,

        }],
        metadata={'name':session['name'], 'email':session['email'], 'password': session['password'], 'referralCode' : referralCode}

    )
    return redirect(sess.url, code=303)


@app.route("/customer-portal", methods=["GET"])
def ugh():

    print(session['name'] + "NAME")
    ses = stripe.billing_portal.Session.create(return_url="https://" + host, customer=DBEdit.getCustomerID(session["name"]))
    return redirect(ses.url, code=303)


@app.route('/webhook', methods=['POST'])
def webhook_received():
   
    request_data = json.loads(request.data)
    print("HIT")
    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
        # Payment is successful and the subscription is created.
        # You should provision the subscription and save the customer ID to your database.
        x = data_object['customer']
        if DBEdit.checkIfCompany(data_object['metadata']['email'], data_object['metadata']['password']) == False:
            print(data)
            print("_____")
            z = stripe.Subscription.retrieve(data_object["subscription"])['items']['data'][0]['id']
            #data_object["subscription"]['items']['data'][0]['id']

            print("HIT")
            #make sure before all of this we know that this is a unique request

            session['name']=data_object['metadata']['name']
            DBEdit.addCompany(data_object['metadata']['name'], data_object['metadata']['email'], data_object['metadata']['password'],x, z,0)
            url = "https://"+host+"/addUser"
            data2 = {"apiKey": "7850813", "instanceName": "Chirp", "userName": data_object['metadata']['name'],
                    "code": data_object['metadata']['referralCode']}
            z=requests.post(url,data=data2).text

            url2 = "https://"+host+"/getReferrers"
            data3 = {"apiKey": "7850813", "instanceName": "Chirp", "name": data_object['metadata']['name']}
            q = requests.post(url2, data=data3).text
            url20 = "http://" + host + "/getReferrers"
            data30 = {"apiKey": "7850813", "instanceName": "Chirp", "name": q}
            z2 = requests.post(url20, data=data30).text
            name1=q
            name2=z2
            print(name1 + " THATS NAME 1" + name2 + " AND THATS NAME 2")
            DBEdit.giveDaysFree(name1)
            DBEdit.giveDaysFree(name2)
            if name1 != "error":
                DBEdit.giveDaysFree(data_object['metadata']['name'])

    elif event_type == 'invoice.paid':
        # Continue to provision the subscription as payments continue to be made.
        # Store the status in your database and check when a user accesses your service.
        # This approach helps you avoid hitting rate limits.

        print("HIHI")
    elif event_type == 'invoice.payment_failed':
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        print("HI")
    else:
        print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})

@app.route("/getCodes", methods=['GET'])
def headShouldersKeysAndCodes():

    if DBEdit.checkIfCompany(session['email'], session['password']):
        return "Share this code with others for 15 days free: " + str(DBEdit.getCode(DBEdit.getCompName(session['email'], session['password']), "Chirp"))

    else:
        return "You are not logged in"

@app.route("/getKeys", methods=['GET'])
def headShouldersKeys():
    if DBEdit.checkIfCompany(session['email'], session['password']):
        z = DBEdit.getAPIKey(session['email'], session['password'])
        return "Api key" + str(z)

    else:
        return "You are not logged in"

@app.route("/getReferrers", methods = ['POST'])
def getReferrers1():
    if request.form['name']=="error":
        return "error"
    if DBEdit.checkAPIKey(request.form['apiKey'], request.form['instanceName']):
        name1 = DBEdit.getReferrer(request.form['name'], request.form['instanceName'])
        return name1
    else:
        return "error"


@app.route("/terms")
def thing3():
    return "NOBODY READS THIS!"


@app.route("/successURL")
def thing4():
    return render_template("success.html")


@app.route("/failURL")
def thing2():
    return render_template("cancel.html")


@app.route("/addInstance", methods = ['POST'])
def addInstance():
    if DBEdit.checkIfCompany(session['email'], session['password']):
        return DBEdit.addInstance(request.form['companyName'], request.form['instanceName'])
    else:
        return "YOU ARE NOT LOGGED IN>>> PLEASE LOG IN"

@app.route("/addABunchOfUsers", methods = ['POST']) #data4 = {"apiKey": "8158334", "instanceName": "Chirp","users":["bobby","joey","TTimmy"]}
def addUsers():
    request_data = request.get_json()
    if DBEdit.checkAPIKey(request_data['apiKey'], request_data['instanceName']):

        x=request_data['users']
        print(x)
        z=len(x)
        q=0
        while q<z:
            DBEdit.addUser(request_data['instanceName'], x[q], 0)
            print(x[q])
            q+=1
        return "ACTION COMPLETE!"
    else:
        return "faulty apikey or instance name"

@app.route("/addUser", methods = ['POST'])
def addUser():
    if DBEdit.checkAPIKey(request.form['apiKey'], request.form['instanceName']):
        DBEdit.addUser(request.form['instanceName'], request.form['userName'], request.form['code'])
        return "ACTION COMPLETE!"
    else:
        return "faulty apikey or instance name"


@app.route("/getCode", methods = ['POST'])
def getCode():
    if DBEdit.checkAPIKey(request.form['apiKey'], request.form['instanceName']):
        return str(DBEdit.getCode(request.form['userName'], request.form['instanceName']))

    else:
        return "faulty apikey or instance name"

@app.route("/getPoints", methods = ['POST'])
def getPoints():
    if DBEdit.checkAPIKey(request.form['apiKey'], request.form['instanceName']):
        return str(DBEdit.getUserPoints(request.form['instanceName'], request.form['userName'])) #TODO: fix this later
    else:
        return "faulty apikey or instance name"
@app.route("/changePoints", methods = ['POST'])
def changePoints():
     if DBEdit.checkAPIKey(request.form['apiKey'], request.form['instanceName']):
         DBEdit.changeUserPoints(request.form['instanceName'], request.form['userName'], request.form['NumberPoints'])
         return "done"
     else:
         return "faulty apikey or instance name"
@app.route("/homepage")
def homepage():
    if DBEdit.checkIfCompany(session['email'], session['password']):
        return render_template('DOCS.html')
    else:
        return "wrong creditionals"



if __name__ == "__main__":

    app.run()
