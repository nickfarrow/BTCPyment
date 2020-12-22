from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, disconnect
from markupsafe import escape
import time

import main
import config
import invoice
from pay import bitcoind

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

@socket_.on('initialise', namespace='/pay')
def test_message(message):
    emit('payresponse', {'time_left': -1, 'response': message['data']})

@socket_.on('payment', namespace='/pay')
def make_payment(payload):
    print("Requesting payment for {}".format(payload['amount']))

    # Check the amount is a float
    amount = payload['amount']
    try:
        amount = float(amount)
    except:
        # Give response?
        amount = None
        return

    # Validate amount is a positive float
    if not (isinstance(amount, float) and amount >= 0):
        # Give response?
        amount = None
        return

    # Need to check this is safe!
    label = payload['label']

    # Initialise this payment
    payment = create_invoice(amount, "USD", label)

    make_payment(payment)

    if payment.paid:
        payment.status = 'Payment finalised.'
        payment.response = 'Payment finalised.'
        update_status(payment)

        ### DO SOMETHING
        # Depends on config
        # Get redirected?
        # Nothing?
        # Run custom script?

def create_invoice(amount, currency, label):
    payment_invoice = invoice.invoice(amount, currency, label)
    payment = bitcoind.btcd(payment_invoice)
    payment.get_address()
    return payment

def update_status(payment, console_status=True):
    if console_status:
        print(payment.status)

    emit('payresponse', {
        'status' : payment.status,
        'address' : payment.address,
        'amount' : payment.value,
        'time_left' : payment.time_left,
        'response': payment.response})
    return

def make_payment(payment):
    payment.status = 'Awaiting payment.'
    payment.response = 'Awaiting payment.'
    update_status(payment)

    # Track start_time for payment timeouts
    payment.start_time = time.time()
    while (time_left := config.payment_timeout - (time.time() - payment.start_time)) > 0:
        payment.time_left = time_left
        payment.confirmed_paid, payment.unconfirmed_paid = payment.check_payment()

        if payment.confirmed_paid > payment.value:
            payment.paid = True
            payment.status = "Payment successful! {} BTC".format(payment.confirmed_paid)
            payment.response = "Payment successful! {} BTC".format(payment.confirmed_paid)
            update_status(payment)
            break

        elif payment.unconfirmed_paid > 0:
            payment.status = "Discovered {} BTC payment. \
                Waiting for {} confirmations...".format(payment.unconfirmed_paid, config.required_confirmations)
            payment.response = "Discovered {} BTC payment. \
                Waiting for {} confirmations...".format(payment.unconfirmed_paid, config.required_confirmations)
            update_status(payment)
            socket_.sleep(config.pollrate)
        else:
            payment.status = "Awaiting {} BTC payment...".format(payment.value)
            payment.response = "Awaiting {} BTC payment...".format(payment.value)
            update_status(payment)
            socket_.sleep(config.pollrate)
    else:
        payment.status = "Payment expired."
        payment.status = "Payment expired."
        update_status(payment)

    return


if __name__ == '__main__':
    socket_.run(app, debug=True)