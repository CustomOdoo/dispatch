from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_weight = fields.Float('Invoice Weight', compute='compute_invoice_weight', store=True)
    is_shipped = fields.Boolean('Is Shipped')

    @api.depends('invoice_line_ids.weight_subtotal')
    def compute_invoice_weight(self):
        for record in self:
            record.invoice_weight = sum(record.mapped('invoice_line_ids.weight_subtotal'))


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    weight = fields.Float(related='product_id.weight', string='Weight')
    weight_subtotal = fields.Float('Weight Subtotal', compute='compute_weight_subtotal', store=True)

    @api.onchange('quantity')
    @api.depends('product_id', 'weight', 'quantity')
    def compute_weight_subtotal(self):
        for record in self:
            record.weight_subtotal = record.quantity * record.weight