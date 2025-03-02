import os
import stripe
import json
import logging

from dotenv import load_dotenv
from flask import Flask, request, render_template

from .config import config

load_dotenv()

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))
config_name = os.getenv('FLASK_ENV') or 'development'
app.config.from_object(config[config_name])

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    print("Instance config file not found.")
    pass

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
  stripe.api_key = app.config['SECRET_KEY']
  payment_intent_id = request.args.get('payment_intent')
  paymentIntent = stripe.PaymentIntent.retrieve(payment_intent_id)  
  
  return render_template('success.html',amount_rcvd=paymentIntent.amount_received, pi_id=paymentIntent.id)

@app.route('/p_key', methods=['GET'])
def p_key() :
  res = {}
  res['key'] = app.config['PUBLISHABLE_KEY']
  return res

@app.route('/paymentInt', methods=['POST'])
def paymentInt() :
  stripe.api_key = app.config['SECRET_KEY']
  try :
    data = request.json
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