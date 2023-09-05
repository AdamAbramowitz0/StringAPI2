from flask import Flask, session,request,render_template, redirect, url_for, jsonify
import DBEdit
from EmailValidation import sendValidationLink
from random import randint
import stripe
import _thread
import json, os
import reportusage


app = Flask(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(selfself,*args,**kwargs):
            with app.app_context():
                return self.run(*args,**kwargs)
    celery.Task=ContextTask
    return celery

_thread.start_new_thread(reportusage.run())

@app.route("/")
def working():
    return render_template("index.html")
@app.route("/terms")
def thing3():
    return "NOBODY READS THIS!"
@app.route("/successURL")
def thing():
    return render_template("success.html")

@app.route("/failURL")
def thing2():
    return render_template("cancel.html")

@app.route("/create-checkout-session",methods=["POST"])
def createccs():
    print(request.form)
    price_id = request.form['priceId']
    session=stripe.checkout.Session.create(

        success_url= "http://127.0.0.1:5000/successURL",
        cancel_url= "http://127.0.0.1:5000/failURL",
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': price_id,

        }]

    )
    return redirect(session.url, code=303)

@app.route('/webhook', methods=['POST'])
def webhook_received():
    
    request_data = json.loads(request.data)

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

        x=data_object['customer']
        print(x)

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


@app.route("/customer-portal", methods=["POST"])
def ugh():

    session=stripe.billing_portal.Session.create(return_url="http://127.0.0.1:5000",)
    return redirect(session.url,code=303)
if __name__ == "__main__":
    app.run(debug=True)
