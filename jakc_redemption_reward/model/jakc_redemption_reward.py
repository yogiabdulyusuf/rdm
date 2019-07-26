from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

AVAILABLE_STATES = [
    ('draft','New'),
    ('open','Open'),    
    ('done', 'Closed'),
    ('expired','Expired'),
    ('deleted','Deleted'),
]

AVAILABLE_TYPE = [
    ('goods','Goods'),
    ('coupon','Coupon'),
]

AVAILABLE_VOUCHER_STATES = [
    ('open','Open'),
    ('done','Closed'),
    ('disable','Disable'),
]

reportserver = '172.16.0.3'
reportserverport = '8080'

class rdm_reward(models.Model):
    _name = "rdm.reward"
    _description = "Redemption Reward"
    

    # def get_trans(self, cr, uid, ids, context=None):
    #     trans_id = ids[0]
    #     return self.browse(cr, uid, trans_id, context=context)
    
    @api.one
    def trans_close(self):
        self.state = 'done'
    
    @api.one
    def trans_re_open(self):
        self.state = 'draft'
    
    @api.one
    def get_stocks(self):
        _logger.info('Start Get Stocks')
        reward_id = self.id
        total = 0
        res = {}
        for trans in self:
            if trans.type == 'goods':
                total_stock = self.env['rdm.reward.goods'].get_stock(reward_id)
                total_booking = self.env['rdm.reward.trans'].get_reward_booking(reward_id)
                total_usage = self.env['rdm.reward.trans'].get_reward_usage(reward_id)
            if trans.type == 'coupon':
                total_stock = self.env['rdm.reward.coupon'].get_stock(reward_id)
                total_booking = self.env['rdm.reward.trans'].get_reward_booking(reward_id)
                total_usage = self.env['rdm.reward.trans'].get_reward_usage(reward_id)
            total = total_stock - total_booking - total_usage
        self.stock = total
        _logger.info('End Get Stocks')
    
    @api.one
    def get_bookings(self):
        _logger.info('Start Get Booking')
        reward_id = self.id
        total = self.env['rdm.reward.trans'].get_reward_booking(reward_id)
        self.booking = total
        _logger.info('End Get Booking')
        return res
    
    @api.one
    def get_usages(self):
        _logger.info('Start Get Usage')
        reward_id = self.id
        total = self.env['rdm.reward.trans'].get_reward_usage(reward_id)
        self.usage = total
        _logger.info('End Get Usages')
    
    @api.one
    def trans_reward_expired(self):
        _logger.info('Start Trans Reward Expired')
        today = datetime.now()
        for trans in self:
            if trans.is_booking:
                if datetime.strptime(trans.booking_expired,'%Y-%m-%d') <= today:
                    self.state = 'expired'

            _logger.info('End Trans Reward Expired')
            return True
    
    def process_reward_expired(self):
        _logger.info('Start Process Reward Expired')
        today = datetime.now()
        args = [('is_booking','=',True),('booking_expired','<=', today.strftime('%Y-%m-%d'),('state','=','open'))]
        reward_trans_ids = self.search(args)
        vals = {}
        vals.update({'state':'expired'})
        reward_trans_ids.write(vals)
        _logger.info('End Process Reward Expired')
        return True
                    
    name = fields.Char(string='Name', size=100, required=True)
    type = fields.Selection(AVAILABLE_TYPE,'Type', size=16, required=True, default='goods')
    iface_instant = fields.Boolean('Is Instant', default=False)
    point = fields.Integer('Point #', default=1)
    coupon_number = fields.Integer('Coupon #')
    limit_count = fields.Integer(string='Limit Count Per User',required=True, default=-1)
    stock = fields.Integer(string='Stock', compute="get_stocks",)
    booking = fields.Integer(string='Booking', compute="get_bookings",)
    usage = fields.Integer(string='Usage', compute="get_usages",)
    image1 = fields.Binary(string='Image')
    reward_trans_ids = fields.One2many('rdm.reward.trans', 'reward_id', string='Transaction')
    goods_ids = fields.One2many('rdm.reward.goods', 'reward_id', string='Goods')
    coupon_ids = fields.One2many('rdm.reward.coupon', 'reward_id', string='Coupon')
    voucher_ids = fields.One2many('rdm.reward.voucher', 'reward_id', string='Voucher')
    state = fields.Selection(AVAILABLE_STATES, string='Status',size=16,readonly=True)


class rdm_reward_goods(models.Model):
    _name = "rdm.reward.goods"
    _rec_name = 'reward_id'
    _description = "Redemption Reward Goods"
    
    @api.one
    def get_stock(self, reward_id):
        _logger.info('Start Get Goods Stocks')
        total_stock = 0
        sql_req= "SELECT sum(stock) as total FROM rdm_reward_goods WHERE reward_id=" + str(reward_id) + " AND state='open'"
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()
        if sql_res is not None:
        	if sql_res['total'] is not None:
        		total_stock = sql_res['total']
        	else:
          		total_stock = 0
        _logger.info('End Get Goods Stocks')
        return total_stock
                                
    
    reward_id = fields.Many2one('rdm.reward','Reward', readonly=True)
    trans_date = fields.Date('Transaction Date', default=fields.Date.today())
    stock = fields.Integer(string='Stock')
    state = fields.Selection(AVAILABLE_STATES,string='Status', size=16, readonly=True, default='open')


class rdm_reward_coupon(models.Model):
    _name = "rdm.reward.coupon"
    _rec_name = 'reward_id'
    _description = "Redemption Reward Coupon"
    
    @api.one
    def get_stock(self, reward_id):
        _logger.info('Start Get Coupon Stocks')
        total_stock = 0
        sql_req= "SELECT sum(stock) as total FROM rdm_reward_coupon WHERE reward_id=" + str(reward_id)
        self.env.cr.execute(sql_req)
        sql_res = self.env.cr.dictfetchone()

        if sql_res:
            total_stock = sql_res['total']
        _logger.info('End Get Coupon Stocks')
        return total_stock
        
    
    reward_id = fields.Many2one('rdm.reward',string='Reward', readonly=True)
    trans_date = fields.Date('Transaction Date', default=fields.Date.today())
    stock = fields.Integer(string='Stock')


class rdm_reward_voucher(models.Model):
    _name = "rdm.reward.voucher"
    _rec_name = 'reward_id'
    _description = "Redemption Reward Voucher"
    
    def get_stock(self, cr, uid, reward_id, context=None):
        _logger.info('Start Get Voucher Stocks')
        total_stock = 0
        # sql_req= "SELECT count(*) as total FROM rdm_reward_voucher WHERE reward_id=" + str(reward_id) + " AND state='open'"
        # cr.execute(sql_req)
        # sql_res = cr.dictfetchone()

        datas_count = self.env['rdm.reward.voucher'].search_count(args, count=True)
        if datas_count:
            total_stock = datas_count
        _logger.info('End Get Voucher Stocks')
        return total_stock
    
    
    
    reward_id = fields.Many2one('rdm.reward','Reward', readonly=True)
    trans_date = fields.Date('Transaction Date', default=fields.Date.today())
    voucher_no = fields.Char('Voucher #', size=15)
    state = fields.Selection(AVAILABLE_VOUCHER_STATES,'Status',size=16, readonly=True, default='open')


class rdm_reward_trans(models.Model):
    _name = "rdm.reward.trans"
    _rec_name = 'reward_id'
    _description = "Redemption Reward Transaction"
    
    @api.one
    def trans_reward_expired(self):
        _logger.info('Start Reward Expired')
        for trans in self:
            booking_expired_date = datetime.strptime(trans.booking_expired,'%Y-%m-%d')
            if trans.is_booking == True and booking_expired_date <= datetime.now():
                vals = {}
                vals.update({'state':'expired'})
                self.write(vals)
                _logger.info('End Reward Expired')
                return True
            else:
                raise ValidationError('Transaction still active')
    
    
    @api.one
    def check_reward_limit_count(self, customer_id, reward_id):
        reward = self.env['rdm.reward'].search([('id', '=', reward_id),])
        if reward.limit_count  == -1:
            return True
        else:
            args = [('customer_id','=',str(customer_id)), ('reward_id','=',str(reward_id)), ('state','=','done')]
            datas_count = self.env['rdm.reward.trans'].search_count(args, count=True)
            if datas_count:
                total = datas_count
                if total >= reward.limit_count:
                    return False
                else:
                    return True
            else:
                return False

    @api.one
    def check_reward_stock(self, reward_id):
        reward = self.env['rdm.reward'].search([('id', '=', reward_id),])
        if reward.stock > 0:
            return True
        else:
            return False

    @api.one
    def allow_redeem_reward(self, customer_id, reward_id):

        reward_limit_count_config_ids = self.env.user.company_id.reward_limit_count
        reward_limit_config_ids = self.env.user.company_id.reward_limit

        if not reward_limit_count_config_ids:
            raise ValidationError("reward_limit_count please define on company information!")
        if not reward_limit_config_ids:
            raise ValidationError("reward_limit please define on company information!")

        if reward_limit_count_config_ids  == -1:
            return True
        else:
            limit_total = reward_limit_count_config_ids
    
            if reward_limit_config_ids:
                # sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.trans_date='" + datetime.today().strftime('%Y-%m-%d') + "' AND c.state='done'"
                # cr.execute(sql_req)
                # sql_res = cr.dictfetchone()

                args = [('customer_id','=', str(customer_id)), ('trans_date','=', datetime.today().strftime('%Y-%m-%d')), ('state','=','done')]
                datas = self.env['rdm.reward.trans'].search_count(args, count=True)
                if datas:
                    current_total = datas
                else:
                    current_total = 0
                _logger.info('Total Reward Trans : ' + str(current_total) )
    
                if current_total >= limit_total:
                    return False
                else:
                    return True
    
            if reward_config.reward_limit_product:
                # sql_req= "SELECT count(*) as total FROM rdm_reward_trans c WHERE c.customer_id=" + str(customer_id) + " AND c.reward_id=" + str(reward_id) + " AND c.trans_date='" + datetime.today().strftime('%Y-%m-%d') + "' AND c.state='done'"
                # cr.execute(sql_req)
                # sql_res = cr.dictfetchone()

                args = [('customer_id','=', str(customer_id)), ('reward_id','=', str(reward_id)), ('trans_date','=',datetime.today().strftime('%Y-%m-%d')), ('state','=','done')]
                datas = self.env['rdm.reward.trans'].search_count(args, count=True)
                if datas:
                    current_total = datas
                else:
                    current_total = 0
                _logger.info('Total Reward Trans For Product : ' + str(current_total) )
    
                if current_total >= limit_total:
                    return False
                else:
                    return True
    
    
    
    # def _reward_config(self, cr, uid, context=None):
    #     return self.env('rdm.reward.config').get_config(cr, uid, context=context)
    
    @api.one
    def trans_close(self):
        # _logger.info("Close Transaction for ID : " + str(ids))
        #Close Transaction
        self.state= 'done'
        self._send_notification_to_customer()
        return True
    
    @api.one
    def _update_print_status(self):
        # _logger.info("Start Update Print Status for ID : " + str(ids))
        values = {}
        values.update({'bypass':True})
        values.update({'method':'_update_print_status'})
        values.update({'printed':True})
        self.write(values)
        
        # _logger.info("End Update Print Status for ID : " + str(ids))
    
    @api.one
    def trans_print_receipt(self):
        # _logger.info("Print Receipt for ID : " + str(ids))
        trans_id = self.id
        
        config = self.env.user.company_id

        for rdm_config in config:
            serverUrl = 'http://' + rdm_config.report_server + ':' + rdm_config.report_server_port +'/jasperserver'
            j_username = rdm_config.report_user
            j_password = rdm_config.report_password
            ParentFolderUri = '/rdm'
            reportUnit = '/rdm/trans_receipt'
            url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(trans_id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
            return {
                'type':'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'
            }
    
    # def trans_re_print(self):
    #     _logger.info("Re-Print Receipt for ID : " + str(ids))
    #     trans_id = ids[0]
    #     trans = self._get_trans(cr, uid, trans_id, context)
    #     return True
    
    @api.one
    def trans_reset(self):

        _logger.info("Start Reset for ID : " + str(self.id))
        values = {}
        values.update({'bypass':True})
        values.update({'method':'trans_reset'})
        values.update({'state':'open'})
        res = self.write(values)
        _logger.info("End Reset for ID : " + str(self.id))
    
    @api.one
    def onchange_reward_id(self, reward_id):
        res = {}
        if reward_id:
            reward = self.env['rdm.reward'].browse(reward_id)
            res['point'] = reward.point
        return {'value':res}
    
    @api.one
    def onchange_is_booking(self, is_booking):

        reward_booking_expired_day_config = self.env.user.company_id.reward_booking_expired_day
        if not reward_booking_expired_day_config:
            raise ValidationError("reward_booking_expired_day_config please define on company information!")

        res = {}
        if is_booking == True:
            expired_date = datetime.today() + timedelta(days=reward_booking_expired_day_config.reward_booking_expired_day)
            res['booking_expired'] = expired_date.strftime('%Y-%m-%d')
        else:
            res['booking_expired'] = None
        return {'value':res}
    #
    # def get_trans(self, cr, uid, trans_id , context=None):
    #     return self.browse(cr, uid, trans_id, context=context);

    @api.one
    def _get_reward(self, reward_id):
        reward = self.env['rdm.reward'].browse(reward_id)
        return reward

    @api.one
    def get_reward_usage(self, reward_id):
        _logger.info('Start Get Reward Usage')
        total = 0

        args = [("reward_id","=",str(reward_id)),("state","=",'open')]
        datas_count = self.env["rdm.reward.trans"].search_count(args, count=True)
        if datas_count is not None:
            total = datas_count
        else:
            total = 0
        _logger.info('End Get Reward Usage')
        return total
    
    @api.one
    def get_reward_booking(self, reward_id):
        _logger.info('Start Get Reward Booking')
        total = 0

        args = [("is_booking","=",True),("reward_id","=",str(reward_id)),("state","=",'open')]
        datas = self.env["rdm.reward.trans"].search(args)
        if datas is not None:
            if datas.total is not None:
                total = datas.total
            else:
                total = 0
        _logger.info('End Get Reward Booking')
        return total

    @api.one
    def process_reward_expired(self):
        _logger.info('Start Process Reward Expired')
        today = datetime.now()
        args = [('is_booking','=',True),('booking_expired','<=', today.strftime('%Y-%m-%d'),('state','=','open'))]
        reward_trans_ids = self.search(args)
        vals = {}
        vals.update({'state':'expired'})
        reward_trans_ids.write(vals)
        _logger.info('End Process Reward Expired')
        return True
    #
    # def _send_notification_to_customer(self, cr, uid, ids, context=None):
    #     _logger.info("Start Notification Process")
    #     trans_id = ids[0]
    #     trans = self.get_trans(cr, uid, trans_id, context)
    #     customer_id = trans.customer_id
    #     rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
    #     rdm_reward_config = self.env('rdm.reward.config').get_config(cr, uid, context=context)
    #     if rdm_config.enable_email and customer_id.receive_email:
    #         #Send Email
    #         _logger.info('Send Reward Transaction Notification')
    #         email_obj = self.env('email.template')
    #         template_ids = rdm_reward_config.reward_trans_email_tmpl
    #         email = email_obj.browse(cr, uid, template_ids)
    #         email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
    #                                                 'email_to': email.email_to,
    #                                                 'subject': email.subject,
    #                                                 'body_html': email.body_html,
    #                                                 'email_recipients': email.email_recipients})
    #         email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)
    #     return True
    #
    # def _send_booking_notitication_to_customer(self, cr, uid, ids, context=None):
    #     _logger.info("Start Booking Notification Process")
    #     trans_id = ids[0]
    #     trans = self.get_trans(cr, uid, trans_id, context)
    #     customer_id = trans.customer_id
    #     rdm_config = self.env('rdm.config').get_config(cr, uid, context=context)
    #     rdm_reward_config = self.env('rdm.reward.config').get_config(cr, uid, context=context)
    #     if rdm_config.enable_email and customer_id.receive_email:
    #         #Send Email
    #         _logger.info('Send Reward Booking Notification')
    #         email_obj = self.env('email.template')
    #         template_ids = rdm_reward_config.reward_booking_email_tmpl
    #         email = email_obj.browse(cr, uid, template_ids)
    #         email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
    #                                                 'email_to': email.email_to,
    #                                                 'subject': email.subject,
    #                                                 'body_html': email.body_html,
    #                                                 'email_recipients': email.email_recipients})
    #         email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)
    #     _logger.info("End Booking Notification Process")
    #     return True

    @api.one
    def _generate_coupon(self):
        _logger.info('Start Generate Coupon')

        for trans in self:
            _logger.info('Reward Total Coupon :' + str(trans.reward_id.coupon_number))
            coupon_data = {}
            coupon_data.update({'customer_id':trans.customer_id.id})
            coupon_data.update({'reward_trans_id':trans.id})
            coupon_data.update({'trans_type':'reward'})
            coupon_data.update({'coupon':trans.reward_id.coupon_number})
            coupon_data.update({'expired_date': datetime.now()})
            self.env('rdm.customer.coupon').create(coupon_data)
            _logger.info('End Generate Coupon')
    
    @api.one
    def trans_print(self):
        # _logger.info("Print Receipt for ID : " + str(ids))

        self._update_print_status()

        config = self.env.user.company_id

        for rdm_config in config:

            serverUrl = 'http://' + rdm_config.report_server + ':' + rdm_config.report_server_port +'/jasperserver'
            j_username = rdm_config.report_user
            j_password = rdm_config.report_password
            ParentFolderUri = '/rdm'
            reportUnit = '/rdm/reward_receipt'
            url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(self.id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
            return {
                'type':'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'
            }


    trans_date = fields.Date('Transaction Date', required=True, readonly=True, default=fields.Date.today())
    customer_id = fields.Many2one('rdm.customer','Customer', required=True)
    reward_id = fields.Many2one('rdm.reward','Reward', required=True)
    point = fields.Integer('Point # Deduct', readonly=True)
    customer_coupon_ids = fields.One2many('rdm.customer.coupon','reward_trans_id','Coupons')
    remarks = fields.Text('Remarks')
    is_booking = fields.Boolean('Is Booking ?', default=False)
    booking_expired = fields.Date('Booking Expired')
    printed = fields.Boolean('Printed', readonly=True, default=False)
    re_print = fields.Integer('Re-Print')
    re_print_remarks = fields.Text('Re-print Remarks')
    state = fields.Selection(AVAILABLE_STATES, 'Status', size=16, readonly=True, default='draft')

    @api.model
    def create(self, vals):
        customer_id = vals.get('customer_id')
        reward_id = vals.get('reward_id')
    
        reward_stock = self.check_reward_stock(reward_id)
        _logger.info("Reward Stock : " + str(reward_stock))
        if not reward_stock:
            raise ValidationError('Reward has no stock'))
    
        check_reward_limit_count  = self.check_reward_limit_count(customer_id, reward_id)
        if not check_reward_limit_count:
            raise ValidationError('Reward Limit Count Applied')
    
        allow_redeem_reward = self.allow_redeem_reward(customer_id, reward_id)
        if not allow_redeem_reward:
            raise ValidationError('Redeem Limit Applied')
    
        customer_id = self.env['rdm.customer'].browse(customer_id)
        reward = self._get_reward(reward_id)

        if customer_id.point < reward.point:
            raise ValidationError('Point not enough')
    
        vals.update({'point':reward.point})
        vals.update({'state':'open'})
        trans_id = super(rdm_reward_trans,self).create(vals)
        if vals.get('is_booking') == True:
            self.env['rdm.customer.point'].deduct_point(trans_id, customer_id.id, vals.get('point'))
            self._send_booking_notitication_to_customer(trans_id)
        return trans_id
    
    @api.multi
    def write(self, values):
        for trans in self:
            if trans['state'] == 'done':
                #Modify Closed Transaction
                if values.get('bypass') == True:
                    trans_data = {}
                    if values.get('method') == 'trans_reset':
                        trans_data.update({'state': values.get('state')})
                    if values.get('method') == 'trans_print_receipt':
                        trans_data.update({'printed': values.get('printed')})
                    result = super(rdm_reward_trans,self).write(trans_data)
                else:
                    raise ValidationError('Edit not allowed, Transaction already closed!')
            else:
                #Close Transaction
                if values.get('state') == 'done':
                    #Check Stock
                    if not trans.is_booking:
                        reward_id = trans.reward_id.id
                        reward_stock = self.check_reward_stock(reward_id)
                        if not reward_stock:
                            raise ValidationError('Reward has no stock')
        
                    #Close Transaction
                    result = super(rdm_reward_trans,self).write(values)
        
                    #Deduct Point
                    customer_id = trans.customer_id.id
        
                    #Deduct point if not booking transaction
                    if not trans.is_booking:
                        self.env['rdm.customer.point'].deduct_point(trans_id, customer_id, trans.point)
                        if trans.reward_id.type == 'coupon':
                            _logger.info("Generate Coupon " + str(trans.reward_id.coupon_number))
                            self._generate_coupon(trans_id)
        
                #Expired Booking Transaction
                elif values.get('state') == 'expired':
                    result = super(rdm_reward_trans,self).write(values)
                #Other State
                else:
                    if 'customer_id' in values.keys():
                        customer_id = values.get('customer_id')
                    else:
                        customer_id = trans.customer_id.id
                    if 'reward_id' in values.keys():
                        reward_id = values.get('reward_id')
                    else:
                        reward_id = trans.reward_id.id
        
                    allow_redeem_reward = self.allow_redeem_reward(customer_id, reward_id)
                    if allow_redeem_reward:
                        customer = self.env['rdm.customer'].browse(customer_id)
                        reward = self._get_reward(reward_id)
                        if customer['point'] >= reward.point:
                            values.update({'point':reward.point})
                            values.update({'state':'open'})
                            result = super(rdm_reward_trans,self).write(values)
                        else:
                            raise ValidationError('Point not enough')
                    else:
                        raise ValidationError('Redeem Limit Applied')
        return result