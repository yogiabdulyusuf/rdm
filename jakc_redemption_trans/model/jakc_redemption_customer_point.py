from odoo import api, fields, models

class rdm_customer_point(models.Model):
    _name = "rdm.customer.point"
    _inherit = "rdm.customer.point"

    trans_id = fields.Many2one('rdm.trans','Transaction ID',readonly=True)
