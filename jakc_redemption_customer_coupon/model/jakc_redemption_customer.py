from odoo import api, fields, models
from datetime import datetime
import logging


_logger = logging.getLogger(__name__)


class rdm_customer(models.Model):    
    _inherit = "rdm.customer"
        
    def get_coupons(self):
        total = 0
        for datas in self.customer_coupon_ids:
            if datas.state == 'active' and datas.expired_date >= datetime.now():
                total = total + datas.coupon
        self.point = total
        _logger.info('Total Coupon : ' + str(total))

    # coupon = fields.Function(get_coupons, type="integer", string='Coupons')
    coupon = fields.Integer(string="Coupons", compute="get_coupons", required=False, )
    customer_coupon_ids = fields.One2many('rdm.customer.coupon','customer_id','Coupons',readonly=True)