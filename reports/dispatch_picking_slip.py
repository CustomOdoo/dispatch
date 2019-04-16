from odoo import models, fields, api, tools


class DispatchPickingSlip(models.Model):
    _name = 'dispatch.picking.slip'
    _description = 'Dispatch Picking Slip Report'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', 
        related='product_id.product_tmpl_id', readonly=True)
    quantity = fields.Float(string='Quantity')

    # @api.model_cr
    # def init(self):
    #     tools.drop_view_if_exists(self._cr, 'dispatch_picking_slip')
    #     self._cr.execute("""
    #                         CREATE or REPLACE VIEW dispatch_picking_slip AS (SELECT
    #                         product_id as product_id,
    #                         name as product_tmpl_id,
    #                         product_qty as quantity
    #                         FROM stock_move
    #                     """)