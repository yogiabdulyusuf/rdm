from odoo import api, fields, models

class rdm_customer_coupon(models.Model):
    _name = "rdm.customer.coupon"
    _inherit = "rdm.customer.coupon"

    trans_id = fields.Many2one('rdm.trans','Transaction ID',readonly=True)
