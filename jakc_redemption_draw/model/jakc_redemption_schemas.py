from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)

class rdm_schemas(models.Model):
    _name = "rdm.schemas"
    _inherit = "rdm.schemas"

    @api.one
    def trans_generate_draw_detail(self):
        _logger.info("Start Generate Draw Detail")
        # trans = self.get_trans(cr, uid, ids, context=None)
        for trans in self:
            _logger.info("Transaction Found")
            draw_ids = trans.draw_ids
            for draw_id in draw_ids:
                for i in range(0, draw_id.quantity):
                    vals = {}
                    vals.update({'draw_id': draw_id.id})
                    vals.update({'schemas_id': trans.id})
                    vals.update({'sequence': i + 1})
                    result_id = self.env['rdm.draw.detail'].create(vals)
                    if not result_id:
                        raise ValidationError('Create generate_draw_detail failed !!')
        else:
            _logger.info("Transaction not found")
        _logger.info("End Generate Draw Detail")


    @api.one
    def trans_clear_draw_detail(self):
        _logger.info("Start Clear Draw Detail")
        args = [('schemas_id','=', self.id)]
        detail_ids = self.env['rdm.draw.detail'].search(args)
        detail_ids.unlink()
        _logger.info("End Clear Draw Detail")
    

    draw_ids        = fields.One2many(comodel_name="rdm.draw", inverse_name="schemas_id", string="Draws", required=False, )
    draw_detail_ids = fields.One2many(comodel_name="rdm.draw.detail", inverse_name="schemas_id", string="Draw Detail", required=False, )
