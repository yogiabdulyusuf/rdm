from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class rdm_customer(models.Model):
    _inherit = "rdm.customer"

    @api.one
    def get_points(self):

        total_point = self.env['rdm.customer.point'].get_customer_total_point(self.id)
        _logger.info('Total Point : ' + str(total_point))

        if total_point is None:
            total_point = 0

        self.point = total_point

    # point = fields.function(get_points, type="integer", string='Points')
    point = fields.Integer(string="Points", compute="get_points", required=False,  )
    customer_point_ids = fields.One2many(comodel_name="rdm.customer.point", inverse_name="customer_id", string="Points", required=False, )
