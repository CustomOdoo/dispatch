from odoo import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_shipped = fields.Boolean('Is Shipped')
    weight_total = fields.Float('Weight Total', compute='compute_weight_total', store=True)

    @api.depends('move_ids_without_package','move_ids_without_package.product_weight_subtotal')
    def compute_weight_total(self):
        for record in self:
            weight_ids = tuple(record.move_ids_without_package.ids)
            if weight_ids:
                self.env.cr.execute("SELECT sum(product_weight_subtotal) FROM stock_move WHERE id IN %s", 
                    (weight_ids,))
                record.weight_total = self.env.cr.fetchall()[0][0]
