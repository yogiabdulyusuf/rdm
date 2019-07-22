from odoo import api, fields, models

class rdm_customer(models.Model):
    _inherit = "rdm.customer"

    tenant_id = fields.Many2one('rdm.tenant','Tenant', default=False)
