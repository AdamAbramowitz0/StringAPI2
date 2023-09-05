#price id = 
import stripe

price_id = ''

session = stripe.checkout.Session.create(
    success_url='',
    cancel_url='',
    payment_method_types=['card'],
    mode='subsciption'





)
