import uuid
import qrcode

import config
from .price_feed import get_btc_value

class invoice:
    def __init__(self, dollar_value, currency, label):
        self.dollar_value = dollar_value
        self.currency = currency
        self.value = round(get_btc_value(dollar_value, currency), 8)
        self.label = label
        self.uuid = str(uuid.uuid4())
        self.status = 'Payment initialised.'
        self.response = ''
        self.time_left = config.payment_timeout
        self.confirmed_paid = 0
        self.unconfirmed_paid = 0
        self.paid = False


    def create_qr(self):
        img = qrcode.make(self.address)
        img.save('static/qr_codes/{}.png'.format(self.uuid))
        return

    