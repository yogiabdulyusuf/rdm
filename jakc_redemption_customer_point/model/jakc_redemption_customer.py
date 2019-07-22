from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class rdm_customer(models.Model):
    _inherit = "rdm.customer"
    
    def get_points(self):
        total = 0
        for datas in self.customer_point_ids:
            total = total + datas.point
        self.point = total
        _logger.info('Total Point : ' + str(total))

    # point = fields.function(get_points, type="integer", string='Points')
    point = fields.Integer(string="Points", compute="get_points", required=False,  )
    customer_point_ids = fields.One2many(comodel_name="rdm.customer.point", inverse_name="customer_id", string="Points", required=False, )
