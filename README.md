# Instruction to run this locally
To get started, clone the repository and run pip3 to install dependencies:

## MacOS

```
git clone https://github.com/changlichuan/stripe-test.git && cd stripe-test
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Rename `sample.env` to `.env` and populate it with your Stripe account's test API keys.
populate STRIPE_SECRET_KEY_TEST with your test secret key, starting with **sk_test**
populate STRIPE_PUBLISHABLE_KEY_TEST with your test publishable-key, starting with **pk_test**

*STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY are illustrative placeholder only*
*These are meant for production keys which will process actual payments, and not recommended in such demo setup*

Then run the application locally for development:
```
source start_dev.sh
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.


# Stripe API used and Architecture
## Application Flow: 

![Swimlane](https://static.swimlanes.io/21cdd598f44d963658ab2d07e027078e.png)

- Users will be directed to checkout page when clicking on any of the book at the Home page, selected item is passed via url parameters.
- On loading of the checkout page: 
  - Publishable key will be obtained from the shop backend; shop frontend can then use it to re-initiate a stripe instance. [Stripe JS SDK]
  - Shop backend will request creation of a paymentIntent with Stripe backend, receiving a client_secret corresponding to this paymentintent. The client_secret will then be passed to the frontend [Stripe Python SDK]
  - A paymentElements associated with the client_secret, thus paymentIntent, will be rendered onto payment-form DOM object. This will allow user to complete the payment with interacting directly with Stripe backend. This will minimize the PCI DSS scope.  [Stripe JS SDK]
- Monitoring the submit event, users will be redirected to success page per return_url upon successful confirmPayment, appended with parameters such as paymentIntent id, payment_intent_client_secret, redirect_status [Stripe JS SDK]
- On the Success page, the shop backend will retrieve the details using quoted paymentintent, displaying the amount_received and paymentIntent_id for users' reference, till this point completing the purchase+payment flow [Stripe Python SDK]

## Architecture
- As no database is used, essential parameters are passed between frontend and backend via parameter or POST request body
- Frontend is responsible to handle user interactions, and rendering payment elements to facilitate payment actions between user and Stripe Backend
- Backend is responsible to create PaymentIntent and verify payment status when presented with paymentIntent_ID again.

## References
* [Stripe Architect course videos](https://www.stripe.training/page/architect) for Stripe features and general payment information
* [How to integrate Stripe's Payment Element](https://www.youtube.com/watch?v=MfFCg7kYCa4) for overall approach
* [Stripe Python SDK doc - PaymentIntent](https://docs.stripe.com/api/payment_intents/)

## Recommended extension
*This demo is designed to be run locally, without a hosted webhook endpoint nor a DB thus limiting the supported workflows*
Extensions:
* Cart module that allows users to bundle serveral items into a single order
* Order module that allows users to cancel or request refund, minimizing dispute
* Order module would also enable users to re-initiate payment, if prior payment flow was interrupted for any reason
* WebHook endpoints to better support Async operations and act upon pushed events from Stripe backend, such as Actual Capture, Dispute, Refund or Subscription.  
* Deploy Shop backend as serverless function or containerized modules allow better scalability. 
* Leverage hosted payment page Checkout would minimize coding and maintenance effort, if customization is not a strong business need.
