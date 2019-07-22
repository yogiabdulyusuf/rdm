from odoo import api, fields, models
from datetime import datetime
import logging
from decimal import Context

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ("draft","Draft"),
    ("waiting","Waiting"),
    ("review","Review"),
    ("open","Open"),    
    ("pause","Pause"),                    
    ("done","Close"),    
]

AVAILABLE_BLAST_STATES = [
    ("draft","Draft"),
    ("ready","Ready"),
    ("process","Process"),                        
    ("done","Close"),    
    ("failed","Failed"),
]

AVAILABLE_EMAIL_STATES = [
    ("draft","Draft"),
    ("ready","Ready"),
    ("sent","Sent"),                        
    ("failed","Failed"),
]

AVAILABLE_TYPE_STATES = [
    ("email","Email"),
    ("sms","SMS"),
]

AVAILABLE_CALCULATION = [
    ("ditotal","Ditotal"),
    ("terbesar","Terbesar"),                         
]

AVAILABLE_SEARCH_TYPE_STATES = [
    ("all","All"),
    ("customer","Customer"),
    ("gender","Gender"),
    ("ethnic","Ethnic"),
    ("religion","Religion"),
    ("marital","Marital"),
    ("interest","Interest"),
    ("occupation","Occupation"),
    ("zone","Zone"),    
]


class rdm_schemas_segment(models.Model):
    _name = "rdm.schemas.segment"
    _description = "Redemption Trans Segment"
    
    schemas_id =  fields.Many2one("rdm.schemas","Schemas", readonly=True, default=False)
    age_segment =  fields.Many2one("rdm.age.segment","Age Segment")

class rdm_schemas_gender(models.Model):
    _name = "rdm.schemas.gender"
    _description = "Redemption Schemas gender"
    
    schemas_id =  fields.Many2one("rdm.schemas","Schemas", readonly=True, default=False)
    gender_id =  fields.Many2one("rdm.customer.gender","Gender")

class rdm_schemas_ayc_participant(models.Model):
    _name = "rdm.schemas.ayc.participant"
    _description = "Redemption Trans AYC Participant"
    
    schemas_id =  fields.Many2one("rdm.schemas","Schemas", readonly=True, default=False)
    participant_id =  fields.Selection([("1","AYC non participant tenant"),("2","AYC participant tenant")],"Participant Type",required=True)

class rdm_schemas_religion(models.Model):
    _name = "rdm.schemas.religion"
    _description = "Redemption Schemas Religion"
    
    schemas_id =  fields.Many2one("rdm.schemas","Schemas", readonly=True, default=False)
    religion_id =  fields.Many2one("rdm.customer.religion","Religion")

class rdm_schemas_ethnic(models.Model):
    _name = "rdm.schemas.ethnic"
    _description = "Redemption Schemas Ethnic"
    
    schemas_id =  fields.Many2one("rdm.schemas","Schemas", readonly=True, default=False)
    ethnic_id =  fields.Many2one("rdm.customer.ethnic","Ethnic")

class rdm_schemas_tenant(models.Model):
    _name = "rdm.schemas.tenant"
    _description = "Redemption schemas Tenant"
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    tenant_id =  fields.Many2one("rdm.tenant","Tenant")

class rdm_schemas_marital(models.Model):
    _name = "rdm.schemas.marital"
    _description = "Redemption schemas Marital"
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    marital_id =  fields.Many2one("rdm.customer.marital","Marital")

class rdm_schemas_interest(models.Model):
    _name = "rdm.schemas.interest"
    _description = "Redemption schemas Interest"
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    interest_id =  fields.Many2one("rdm.customer.interest","Interest")   

class rdm_schemas_card_type(models.Model):
    _name = "rdm.schemas.card.type"
    _description = "Redemption schemas Card Type"
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    card_type_id =  fields.Many2one("rdm.card.type","Card Type") 

class rdm_schemas_tenant_category(models.Model):
    _name = "rdm.schemas.tenant.category"
    _description = "Redemption schemas Tenant Category"
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    tenant_category_id =  fields.Many2one("rdm.tenant.category","Tenant Category")  

class rdm_schemas_rules(models.Model):
    _name = "rdm.schemas.rules"
    _description = "Redemption schemas Rules"
    
    
    # def trans_set_global(self):
    #     schema = "spending"
    #     trans = self.id
    #     if trans:
    #         if not trans.is_global:
    #             rules_id = trans.rules_id
    #             rules_detail_ids = rules_id.rules_detail_ids
    #             status = False
    #             for rules_detail_id in rules_detail_ids:
    #                 rule_schema = rules_detail_id.rule_schema
    #                 if rule_schema  == schema:
    #                     status = True
    #             if status:
    #                 values = {}
    #                 values.update({"is_global" : True})
    #                 self.write(values)
    #             else:
    #                 raise osv.except_osv(("Warning"), ("Please Provide <b>Spending Rule Schema!</b>"))
    #         else:
    #             raise osv.except_osv(("Warning"), ("Already Set Global!"))
    #
    # def trans_unset_global(self):
    #     trans = self.id
    #     if trans:
    #         if trans.is_global:
    #             values = {}
    #             values.update({"is_global" : False})
    #             self.write( values)
    #         else:
    #             raise osv.except_osv(("Warning"), ("Rules is not Global"))
        
    
    schemas_id =  fields.Many2one("rdm.schemas","schemas", readonly=True, default=False)
    rules_id =  fields.Many2one("rdm.rules","Rules")
    is_global =  fields.Boolean("Is Global", readonly=True, default=False)
    schemas =  fields.Selection([("ditotal","Ditotal"),("terbesar","Terbesar")],"Schemas")


class rdm_schemas_blast(models.Model):
    _name = "rdm.schemas.blast"
    _description = "Redemption Schemas Blast"

    @api.one
    def trans_ready(self):        
        self.state = "ready"
        return True

    @api.one
    def trans_process(self):        
        self.state = "process"
        return True

    @api.one
    def trans_done(self):        
        self.state = "done"
        return True

    @api.one
    def trans_failed(self):        
        self.state = "failed"
        return True

    @api.one
    def blast_customer(self):
        return {
               "type" :  "ir.actions.act_window",
               "name" : "Blast Customer",
               "view_mode" :  "form",
               "view_type" :  "form",                              
               "res_model" : "rdm.schemas.blast.customer",
               "nodestroy" :  True,
               "target" : "new",
               "context" :  {"blast_id" : self.id},
        } 
            
    
    schemas_id =  fields.Many2one("rdm.schemas", "Schemas", readonly=True)
    description =  fields.Text("Description")
    customer_schemas_blast_ids =  fields.Many2many(
                                     "rdm.customer",
                                     "customer_schemas_blast_rel",
                                     "rdm_customer_id",
                                     "rdm_schemas_blast_id",
                                     string = "Customers")
    schedule =  fields.Datetime("Schedule",required=True) 
    type =  fields.Selection(AVAILABLE_TYPE_STATES,"Type", size=16, required=True)
    blast_detail_ids =  fields.One2many("rdm.schemas.blast.detail","blast_id", readonly=True)
    state =  fields.Selection(AVAILABLE_BLAST_STATES, "Status", size=16, readonly=True, default="draft")

    
    
class rdm_schemas_blast_detail(models.Model):
    _name = "rdm.schemas.blast.detail"
    _description = "Redemption Schemas Blast Detail"

    @api.one
    def trans_ready(self):        
        self.state = "ready"
        return True

    @api.one
    def trans_sent(self):        
        self.state = "sent"
        return True

    @api.one
    def trans_failed(self):        
        self.state = "failed"
        return True
    
    
    blast_id =  fields.Many2one("rdm.schemas.blast", "Schemas Blast", readonly=True,  ondelete="cascade")          
    customer_id =  fields.Many2one("rdm.customer", "Customer", required=True)
    state =  fields.Selection(AVAILABLE_EMAIL_STATES, "Status", size=16, readonly=True, default="draft")
    

class rdm_schemas_blast_customer(models.Model):
    _name = "rdm.schemas.blast.customer"
    _description = "Redemption Schema Blast Customer"
    
    # def _check_customer(self):
    #     detail_ids = self.env("rdm.schemas.blast.detail").search([("blast_id","=", blast_id),("customer_id","=", customer_id)] )
    #     if len(detail_ids) > 0:
    #         return True
    #     else:
    #         return False
    #
    # def add_customer(self):
    #     _logger.info("Start Add Customer")
    #
    #     blast_id = self.blast_id
    #     if self.search_type == "all":
    #         customer_ids = self.env("rdm.customer").search([("state","=","active"),])
    #         for i in range(len(customer_ids)):
    #             if not self._check_customer():
    #                 data = {}
    #                 data.update({"blast_id" : blast_id})
    #                 data.update({"customer_id" :  customer_ids[i]})
    #                 self.env("rdm.schemas.blast.detail").create(data)
    #
    #     if self.search_type == "customer":
    #         customer_id = self.customer_id.id
    #         if not self._check_customer():
    #             data = {}
    #             data.update({"blast_id" : blast_id})
    #             data.update({"customer_id" : customer_id})
    #             self.env("rdm.schemas.blast.detail").create(data)
    #
    #     if self.search_type == "gender":
    #         gender_id = self.gender_id.id
    #         customer_ids = self.env("rdm.customer").search([("gender","=",gender_id),("state","=","active")])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "ethnic":
    #         ethnic_id = self.enthic_id.id
    #         customer_ids = self.env("rdm.customer").search([("ethnic","=",ethnic_id),("state","=","active")])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "religion":
    #         religion_id = self.religion_id.id
    #         customer_ids = self.env("rdm.customer").search([("religion","=",religion_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "marital":
    #         marital_id = self.marital_id.id
    #         customer_ids = self.env("rdm.customer").search([("marital","=",marital_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "education":
    #         education_id = self.education_id.id
    #         customer_ids = self.env("rdm.customer").search([("education","=",education_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "interest":
    #         interest_id = self.interest_id.id
    #         customer_ids = self.env("rdm.customer").search([("interest_id","=",interest_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     if self.search_type == "occupation":
    #         occupation_id = self.occupation_id.id
    #         customer_ids = self.env("rdm.customer").search([("occupation","=",occupation_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #
    #     if self.search_type == "zone":
    #         zone_id = self.zone_id.id
    #         customer_ids = self.env("rdm.customer").search([("zone","=",zone_id)])
    #         if len(customer_ids) > 0:
    #             for i in range(len(customer_ids)):
    #                 if not self._check_customer():
    #                     data = {}
    #                     data.update({"blast_id" : blast_id})
    #                     data.update({"customer_id" :  customer_ids[i]})
    #                     self.env("rdm.schemas.blast.detail").create(data)
    #         else:
    #             raise osv.except_osv(("Warning"), ("No Customer Found!"))
    #
    #     _logger.info("End Add Customer")
    #
    #     return False
        
    
    search_type =  fields.Selection(AVAILABLE_SEARCH_TYPE_STATES,"Search Type", size=16, required=True)
    customer_id =  fields.Many2one("rdm.customer","Customer")
    gender_id =  fields.Many2one("rdm.customer.gender","Customer Gender")
    ethnic_id =  fields.Many2one("rdm.customer.ethnic","Customer Ethnic")
    religion_id =  fields.Many2one("rdm.customer.religion","Customer Religion")
    marital_id =  fields.Many2one("rdm.customer.marital","Customer Marital")
    education_id =  fields.Many2one("rdm.customer.education","Customer Education")
    interest_id =  fields.Many2one("rdm.customer.education","Customer Interest")
    occupation_id =  fields.Many2one("rdm.customer.occupation","Customer Occupation")
    zone_id =  fields.Many2one("rdm.customer.zone","Customer Zone")
    
class rdm_schemas(models.Model):
    _name = "rdm.schemas"
    _description = "Redemption schemas"

    @api.one
    def trans_review(self):
        self.state = "review"
        #Send Email To Manager  
        return True

    @api.one
    def trans_start(self):
        self.state = "open"
        return True

    @api.one
    def trans_pause(self):
        self.state = "pause"
        return True

    @api.one
    def trans_close(self):
        self.state = "done"
        return True

    @api.one
    def trans_reset(self):
        self.state = "open"
        return True

    @api.one
    def trans_waiting(self):
        self.state = "waiting"
        return True
    
    # def id(self):
    #     return self.id
    #
    # def active_schemas(self):
    #     ids = self.env("rdm.schemas").search([("state","=","open"),("type","=","promo"),])
    #     return self.env("rdm.schemas").browse(ids)
    #
    # def promo_to_close(self):
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     args = [("state","=","open"),("end_date","<",today)]
    #     ids = self.search(cr, uid, args)
    #     values = {}
    #     values.update({"state" : "done"})
    #     self.write( values)
    #     return True
    #
    # def active_promo_schemas(self):
    #     ids = {}
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     ids = self.env("rdm.schemas").search([("state","=","open"),("type","=","promo"),("start_date","<=",today),("end_date",">=", today)])
    #     return self.env("rdm.schemas").browse(ids)
    #
    # def active_point_schemas(self):
    #     ids = {}
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     ids = self.env("rdm.schemas").search([("state","=","open"),("type","=","point"),("start_date","<=",today),("end_date",">=", today)])
    #     return self.env("rdm.schemas").browse(ids)
    #
    #
    # def start_blast(self):
    #     _logger.info("Start Schemas Blast")
    #     active_schemas = self.env("rdm.schemas").active_schemas(cr, uid)
    #     for schemas in active_schemas:
    #         blast_ids = schemas.blast_ids
    #         for blast in blast_ids:
    #             if blast.state == "ready":
    #                 blast_schedule  = datetime.strptime(blast.schedule, "%Y-%m-%d %H:%M:%S")
    #                 if blast_schedule <= datetime.now():
    #                     _logger.info("Email Blast for " + schemas.name + " executed")
    #                     self.env("rdm.schemas.blast").trans_process([blast.id])
    #                     email_from = "info@taman-anggrek-mall.com"
    #                     subject = schemas.name
    #                     body_html = schemas.desc_email
    #                     blast_customer_schemas_blast_ids = blast.customer_schemas_blast_ids
    #                     #blast_detail_ids = blast.blast_detail_ids
    #                     for customer_id in blast_customer_schemas_blast_ids:
    #                         if customer_id.receive_email:
    #                             _logger.info("Send Email to " + customer_id.name)
    #                             email_to = customer_id.email
    #                             message = {}
    #                             message.update({"email_from" : email_from})
    #                             message.update({"email_to" : email_to})
    #                             message.update({"subject" : subject})
    #                             message.update({"body_html" : body_html})
    #                             self._send_email_notification(message)
    #                         else:
    #                             _logger.info("Send Email to " + customer_id.name + " not allowed!")
    #                     self.env("rdm.schemas.blast").trans_done(blast.id)
    #     _logger.info("End Schemas Blast")
    #
    # def close_schemas_scheduler(self):
    #     _logger.info("Start Close Schemas Scheduler")
    #     result = self.promo_to_close()
    #     return result
    #     _logger.info("End Close Schemas Scheduler")
    #
    # def _get_open_schemas(self):
    #     trans = self._id(cr, uid, trans_id, conText)
    #     ids = None
    #     if trans.type == "promo":
    #         ids = self.env("rdm.schemas").search([("type","=","promo"),("state","=","open"),])
    #     if trans.type == "point":
    #         ids = self.env("rdm.schemas").search([("type","=","point"),("state","=","open"),])
    #     if ids:
    #         return True
    #     else:
    #         return False
    #
    # def _send_email_notification(self):
    #     _logger.info("Start Send Email Notification")
    #     mail_mail = self.env("mail.mail")
    #     mail_ids = []
    #     mail_ids.append(mail_mail.create( {
    #         "email_from" :  values["email_from"],
    #         "email_to" :  values["email_to"],
    #         "subject" :  values["subject"],
    #         "body_html" :  values["body_html"],
    #         }))
    #     result_id = mail_mail.send(mail_ids)
    #     _logger.info("Mail ID : " + str(result_id))
    #     _logger.info("End Send Email Notification")
    
    
    name =  fields.Char("Name", size=200, required=True)
    type =  fields.Selection([("promo","Promo"),("point","Point")],"Type",readonly=True)
    calculation =  fields.Selection(AVAILABLE_CALCULATION,"Calculation",size=16,required=True)
    description =  fields.Text("Description",required=True)
    desc_email =  fields.Text("Description For Email",required=True)
    desc_sms =  fields.Char("Description For SMS", size=140,required=True)

    #Periode
    start_date =  fields.Date("Start Date",required=True)
    end_date =  fields.Date("End Date",required=True)
    last_redeem =  fields.Date("Last Redeem",required=True)
    draw_date =  fields.Date("Draw Date",required=True, default=fields.Datetime.now)
        
        #Spend, coupon , point and reward
    max_spend_amount =  fields.Float("Maximum Spend Amount", required=True, help="-1 for No Limit", default=-1)
    max_spend_amount_global =  fields.Boolean("Global")
    max_coupon =  fields.Integer("Maximum Coupon")
    max_coupon_global =  fields.Boolean("Maximum Coupon Global")
    max_point =  fields.Integer("Maximum Point")
    max_point_global =  fields.Boolean("Maximum Point Global")
    min_spend_amount =  fields.Float("Minimum Spend Amount", required=True, help="-1 for No Limit")
    coupon_spend_amount =  fields.Float("Coupon Spend Amount",required=True)
    point_spend_amount =  fields.Float("Point Spend Amount",required=True)
    reward_spend_amount =  fields.Float("Reward Spend Amount", required=True, default=-1)
    limit_coupon =  fields.Integer("Coupon Limit",help="-1 for No Limit",required=True, default=-1)
    limit_coupon_per_periode =  fields.Integer("Coupon Limit Per Periode", help="-1 for No Limit",required=True, default=-1)
    min_coupon =  fields.Integer("Minimum Coupon")
    limit_point =  fields.Integer("Point Limit",help="-1 for No Limit",required=True, default=-1)
    limit_point_per_periode =  fields.Integer("Point Limit Per Periode", help="-1 for No Limit", required=True, default=-1)
    min_point =  fields.Integer("Minimum Point")
    limit_reward =  fields.Integer("Reward Limit",help="-1 for No Limit",required=True, default=-1)
    point_expired_date =  fields.Date("Point Expired Date")


    segment_ids =  fields.One2many("rdm.schemas.segment","schemas_id","Segment")
    image1 =  fields.Binary("schemas Image")

    #Bank Promo
    bank_id =  fields.Many2one("rdm.bank","Bank Promo")

    #Customer Filter
    gender_ids =  fields.One2many("rdm.schemas.gender","schemas_id","schemas Gender")
    religion_ids =  fields.One2many("rdm.schemas.religion","schemas_id","schemas Religion")
    ethnic_ids =  fields.One2many("rdm.schemas.ethnic","schemas_id","schemas Ethnic")
    marital_ids =  fields.One2many("rdm.schemas.marital","schemas_id","schemas Marital")
    interest_ids =  fields.One2many("rdm.schemas.interest","schemas_id","schemas Interest")
    card_type_ids =  fields.One2many("rdm.schemas.card.type","schemas_id","schemas AYC Card Type")

    #Tenant Filter
    tenant_ids =  fields.One2many("rdm.schemas.tenant","schemas_id","schemas Tenant")
    tenant_category_ids =  fields.One2many("rdm.schemas.tenant.category","schemas_id","Tenant Category")
    ayc_participant_ids =  fields.One2many("rdm.schemas.ayc.participant","schemas_id","AYC Participant")

    #Rules List
    rules_ids =  fields.One2many("rdm.schemas.rules","schemas_id","Rules")

    #Blast List
    blast_ids =  fields.One2many("rdm.schemas.blast","schemas_id","Blast")

    #Receipt Header and Footer
    receipt_header =  fields.Char("Receipt Header", size=50)
    receipt_footer =  fields.Text("Receipt Footer")
    state =   fields.Selection(AVAILABLE_STATES, "Status", size=16, readonly=True,  default="draft")
        
    # def create(self):
    #     if "point_spend_amount" in values.keys():
    #         if self.point_spend_amount > 0:
    #             if not self.point_expired_date:
    #                 raise osv.except_osv(("Warning"), ("Point Expired Date Required!"))
    #
    #     id =  super(rdm_schemas, self).create(values)
    #     self.trans_waiting()
    #     return id
    #
    # def write(self):
    #     if "point_spend_amount" in values.keys():
    #         if self.point_spend_amount > 0:
    #             if not self.point_expired_date:
    #                 raise osv.except_osv(("Warning"), ("Point Expired Date Required!"))
    #
    #     result =  super(rdm_schemas, self).write(values)
    #     return result
