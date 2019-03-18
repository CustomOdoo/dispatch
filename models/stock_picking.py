from odoo import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_shipped = fields.Boolean('Is Shipped', readonly=True)