from odoo import api, fields, models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ("draft","New"),    
    ("active","Active"),
    ("disable", "Disable"),
    ("terminate", "Terminate"),
]

AVAILABLE_PARTICIPANT = [
    ("1","AYC non participant tenant"),
    ("2","AYC participant tenant")
]

class rdm_tenant(models.Model):
    _name = "rdm.tenant"
    _description = "Redemption Tenant"

    @api.one
    def trans_reset(self):
        _logger.info("Reset for ID : " + str(self.id))
        self.state = "active"

    @api.one
    def trans_disable(self):
        _logger.info("Disable for ID : " + str(self.id))
        self.state = "disable"

    @api.one
    def trans_enable(self):
        _logger.info("Enable for ID : " + str(self.id))
        self.state = "active"

    @api.one
    def trans_terminate(self):
        _logger.info("Terminate for ID : " + str(self.id))
        self.state = "terminate"

    # @api.one
    # def _get_trans(self):
    #     return self.trans_id
            

    name = fields.Char(string="Name", size=200, required=True)
    company = fields.Char(string="Company", size=200)
    category =  fields.Many2one(comodel_name="rdm.tenant.category", string="Category", required=True)
    grade =  fields.Many2one(comodel_name="rdm.tenant.grade", string="Grade", required=True)
    participant =  fields.Selection(AVAILABLE_PARTICIPANT,"Participant Type",required=True, default="1")
    location =  fields.Char(string="Location", size=10)
    floor =  fields.Char(string="Floor", size=10)
    number =  fields.Char(string="Number", size=10)
    start_date =  fields.Date(string="Join Date", required=True, readonly=True, default=lambda self: fields.datetime.now())
    end_date =  fields.Date(string="End Date")
    customer_ids = fields.One2many(comodel_name="rdm.customer", inverse_name="tenant_id", string="Contacts", required=False, )
    message_ids = fields.One2many(comodel_name="rdm.tenant.message", inverse_name="tenant_id", string="Messages", required=False, )
    state =  fields.Selection(AVAILABLE_STATES,string="Status",size=16, readonly=False, default="draft")

    @api.model
    def create(self, vals):
        vals['state'] =  "active"
        trans_id = super(rdm_tenant,self).create(vals)
        return trans_id

class rdm_tenant_message(models.Model):
    _name = "rdm.tenant.message"
    _rec_name = 'tenant_id'
    _description = "Redemption Tenant Message"
 
    trans_date =  fields.Date(string="Date", required=True, default=lambda self: fields.datetime.now())
    tenant_id = fields.Many2one(comodel_name="rdm.tenant", string="Tenant", required=True, )
    customer_id = fields.Many2one(comodel_name="rdm.customer", string="Contact", required=True, )
    subject =  fields.Char(string="Subject",size=50,required=True)
    message =  fields.Text(string="Message",required=True)
    state =  fields.Selection([("open","Open"),("reply","Reply"),("done","Close")], string="State", default="open")
