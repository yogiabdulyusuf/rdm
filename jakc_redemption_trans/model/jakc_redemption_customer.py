from odoo import api, fields, models

class rdm_customer(models.Model):
    _name = "rdm.customer"
    _inherit = "rdm.customer"

    trans_ids = fields.One2many('rdm.trans','customer_id','Transaction',readonly=True)
