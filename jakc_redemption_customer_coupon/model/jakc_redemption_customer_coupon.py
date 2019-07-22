from odoo import api, fields, models
from datetime import datetime
import time
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),
    ('active','Active'),
    ('expired','Expired'),
    ('claimed','Claimed'),    
    ('req_delete','Request For Delete'),
    ('delete','Deleted')
]


AVAILABLE_TRANS_TYPE = [
    ('promo','Promotion'),
    ('point','Point'),
    ('reward','Reward'),
    ('reference','Reference'),
    ('member','New Member'),
]


class rdm_customer_coupon(models.Model):
    _name = 'rdm.customer.coupon'
    _description = 'Redemption Customer Coupon'
                
    # def get_trans(self):
    #     trans_id = self.id
    #     return self.browse(trans_id)
    #
    # def process_expired(self, cr, uid, context=None):
    #     _logger.info('Start Customer Coupon Process Expired')
    #     _logger.info('End Customer Coupon Process Expired')
    #     return True
    #
    #
    # def delete_coupon(self):
    #     _logger.info('Start Delete Coupon')
    #     trans = self.get_trans()
    #     customer_coupon_detail_ids = trans.customer_coupon_detail_ids
    #     for customer_coupon_detail_id in customer_coupon_detail_ids:
    #         self.env('rdm.customer.coupon.detail').trans_delete(customer_coupon_detail_id.id)
    #     _logger.info('End Delete Coupon')
    #
    # def undelete_coupon(self):
    #     _logger.info('Start UnDelete Coupon')
    #     trans = self.get_trans()
    #     customer_coupon_detail_ids = trans.customer_coupon_detail_ids
    #     for customer_coupon_detail_id in customer_coupon_detail_ids:
    #         self.env('rdm.customer.coupon.detail').trans_close(customer_coupon_detail_id.id)
    #     _logger.info('End UnDelete Coupon')
    #
    # def generate_coupon(self):
    #     _logger.info('Start Generate Coupon')
    #     trans = self.get_trans()
    #     coupon = trans.coupon
    #     for i in range (0,coupon):
    #         values = {}
    #         values.update({'customer_coupon_id' :  trans.id})
    #         values.update({'expired_date' : trans.expired_date})
    #         self.env('rdm.customer.coupon.detail').create(values)
	#     time.sleep(0.1)
    #     _logger.info('End Generate Coupon')
            

    customer_id =  fields.Many2one('rdm.customer','Customer', required=True)        
    trans_type =  fields.Selection(AVAILABLE_TRANS_TYPE, 'Transaction Type', size=16)       
    coupon =  fields.Integer('Coupon #', required=True, default=0)  
    expired_date =  fields.Date('Expired Date', required=True)
    customer_coupon_detail_ids =  fields.One2many('rdm.customer.coupon.detail','customer_coupon_id','Coupon Codes')
    state =  fields.Selection(AVAILABLE_STATES,'Status',size=16,readonly=True, default='active')
       
    
    # def create(self, values):
    #     id = super(rdm_customer_coupon, self).create(values)
    #     id.generate_coupon()
    #     return id

    

class rdm_customer_coupon_detail(models.Model):
    _name = 'rdm.customer.coupon.detail'
    _description = 'Redemption Customer Coupon Detail'
        
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         res.append((record.id, record.coupon_code))
    #     return res
    #
    # def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     if not context:
    #         context = {}
    #     if name:
    #         ids = self.search(cr, uid, [('coupon_code', operator, name)] + args, limit=limit)
    #     else:
    #         ids = self.search(cr, uid, args, limit=limit)
    #
    #     return self.name_get()
    #
    # def get_trans(self):
    #     trans_id = self.id
    #     return self.browse(trans_id)
    #
    # def trans_delete(self):
    #     _logger.info('Start Trans Delete')
    #     values = {}
    #     values.update({'state' : 'delete'})
    #     self.write(values)
    #     _logger.info('End Trans Delete')
    #
    # def trans_close(self):
    #     _logger.info('Start Trans Close')
    #     values = {}
    #     values.update({'state' : 'done'})
    #     self.write(values)
    #     _logger.info('End Trans Close')
    #
    # def trans_expired(self):
    #     _logger.info('Start Trans Expired')
    #     values = {}
    #     values.update({'state' : 'expired'})
    #     self.write(values)
    #     _logger.info('End Trans Expired')
    #
    # def trans_claimed(self):
    #     _logger.info('Start Customer Coupon Detail Process Claimed')
    #     values = {}
    #     values.update({'state' : 'claimed'})
    #     super(rdm_customer_coupon_detail,self).write(values)
    #     _logger.info('End Customer Coupon Detail Process Claimed')
    #     return True
    #
    # def trans_re_open(self):
    #     _logger.info('Start Customer Coupon Detail Process Re-open')
    #     values = {}
    #     values.update({'state' : 'active'})
    #     super(rdm_customer_coupon_detail,self).write(values)
    #     _logger.info('End Customer Coupon Detail Process Re-open')
    #     return True
    #
    # def expired_coupon(self, cr, uid, customer_coupon_id, context=None):
    #     _logger.info('Start Expired Coupon')
    #     args = {('customer_coupon_id','=',customer_coupon_id)}
    #     ids = self.search(cr, uid, args)
    #     values = {}
    #     values.update({'state' : 'expired'})
    #     self.write(values)
    #     _logger.info('End Expired Coupon')
        

    customer_coupon_id =  fields.Many2one('rdm.customer.coupon','Customer Coupon', readonly=True)
    coupon_code =  fields.Char('Coupon Code', size=10, required=True, readonly=True)
    expired_date =  fields.Date('Expired Date', required=True, readonly=True)
    state =  fields.Selection(AVAILABLE_STATES,'Status',size=16,readonly=True, default='active')


    # def create(self):
    #     coupon_code = self.env('ir.sequence').get('rdm.customer.coupon.sequence')
    #     values = {}
    #     values.update({'coupon_code' :  coupon_code})
    #     id =  super(rdm_customer_coupon_detail,self).create(values)
    #     _logger.info("Generate Coupon : " + coupon_code)
    #     return id
    #
    # def write(self, cr, uid, ids, values, context=None):
    #     trans = self.get_trans(cr, uid, ids)
    #     if 'state' in values.keys():
    #         if values.get('state') == 'claimed':
    #             return self.process_claimed(cr, uid, ids)
    #
    #     return super(rdm_customer_coupon_detail, self).write(cr, uid, ids, values)
