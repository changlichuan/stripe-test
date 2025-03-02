import os
import stripe
import json
import logging

from dotenv import load_dotenv
from flask import Flask, request, render_template

import random

load_dotenv()

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  title = None
  amount = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    # Included in layout view, feel free to assign error
    error = 'No item selected'

  return render_template('checkout.html', title=title, amount=amount, error=error)

# Success route
@app.route('/success', methods=['GET'])
def success():
  _env = os.environ.get('FLASK_ENV');
  if _env == 'development' :
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY_TEST')
  elif _env == 'production' :
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
  else :
    return "no environment"
  
  payment_intent_id = request.args.get('payment_intent')
  paymentIntent = stripe.PaymentIntent.retrieve(payment_intent_id)  
  
  return render_template('success.html',amount_rcvd=paymentIntent.amount_received, pi_id=paymentIntent.id)

@app.route('/p_key', methods=['GET'])
def p_key() :
  res = {}
  _env = os.environ.get('FLASK_ENV');
  if _env == 'development' :
    res['key'] = os.environ.get('STRIPE_PUBLISHABLE_KEY_TEST')
  elif _env == 'production' :
    res['key'] = os.environ.get('STRIPE_PUBLISHABLE_KEY')
  else : 
    res['key'] = None
  return res

@app.route('/paymentInt', methods=['POST'])
def paymentInt() :
  _env = os.environ.get('FLASK_ENV');
  if _env == 'development' :
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY_TEST')
  elif _env == 'production' :
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
  else :
    return "no environment"
    
    
  try :
    data = request.json
    #_amount = request.args.get('amount')
    _amount = data['amount']
    paymentIntent = stripe.PaymentIntent.create(
      amount=_amount,
      currency='eur',
      payment_method_types=["card"],
    )
    res = {}
    res['clientSecret'] = paymentIntent.client_secret;
    return res
  except Exception as e: 
    print(e.message)
     
  



if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)