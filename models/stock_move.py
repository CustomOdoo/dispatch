from odoo import fields, models, api, _ 


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_weight = fields.Float(related='product_id.weight', 
        readonly=True, string='Weight', store=True)
    product_weight_subtotal = fields.Float('Weight Subtotal', 
        compute='compute_product_weight_subtotal', readonly=True, store=True)

    @api.depends('product_weight', 'quantity_done')
    def compute_product_weight_subtotal(self):
        for item in self:
            item.product_weight_subtotal = item.quantity_done * item.product_weight