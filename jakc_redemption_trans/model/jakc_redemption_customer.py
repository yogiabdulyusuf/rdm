from odoo import api, fields, models

class rdm_customer(models.Model):
    _name = "rdm.customer"
    _inherit = "rdm.customer"

    trans_ids = fields.One2many(comodel_name="rdm.trans", inverse_name="customer_id", string="Transaction", required=False, readonly=True)
