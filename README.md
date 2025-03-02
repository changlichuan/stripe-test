# Instruction to run this locally
To get started, clone the repository and run pip3 to install dependencies:

MacOS

```
git clone https://github.com/marko-stripe/sa-takehome-project-python && cd sa-takehome-project-python
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Rename `sample.env` to `.env` and populate it with your Stripe account's test API keys.
populate STRIPE_SECRET_KEY_TEST with your test secret key, starting with **sk_test**
populate STRIPE_PUBLISHABLE_KEY_TEST with your test publishable-key, starting with **pk_test**

STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY are for illustration only
These are meant for production keys which will process actual payments, and not recommended in such demo setup

Then run the application locally for development:
```
source start_dev.sh
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.


# Stripe API used and Architecture
Application Flow: 

![alt text](http://url/to/img.png)

- Users will be directed to checkout page when clicking on any of the book at the Home page, selected item is passed via url parameters so expected payment amount can be rendered on the checkout page.
- On loading of the checkout page: 
  - Publishable key will be obtained from the shop backend, to re-initiate a stripe instance in the shop frontend. [Stripe JS SDK]
  - A paymentIntent will be created by the Stripe backend, returning received client_secret from Stripe Backend, corresponding to this paymentintent, to the frontend [Stripe Python SDK]
  - A paymentElements associated with the client_secret, thus paymentIntent, will be rendered onto payment-form DOM object, allowing user to complete the payment [Stripe JS SDK]
- Upon completion of the payment, users will be redirected to success page per return_url specified in the earlier call, appended with parameters such as paymentIntent id, payment_intent_client_secret, redirect_status [Stripe JS SDK]
- On the Success page, the shop backend will retrieve the details using quoted paymentintent, displaying the amount_received and paymentIntent_id for users' reference, till this point completing the purchase+payment flow [Stripe Python SDK]

Architecture
- As no database is used, essential parameters are passed between frontend and backend via parameter or POST request body
- Frontend is responsible to take in user inputs, and rendering payment elements to facilitate payment actions between user and Stripe Backend
- Backend is responsible to register PaymentIntent and verify payment status when presented with paymentIntent_ID again.



