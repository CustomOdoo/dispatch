# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetDispatch(models.Model):
    _name = 'fleet.dispatch'
    _description = 'Fleet Dispatch'
    _inherit = 'mail.thread'

    fleet = fields.Many2one('fleet.vehicle', string='Fleet', 
        domain=[('is_dispatched','=',False)], required=True)
    tonnage = fields.Float(related='fleet.tonnage', string='Tonnage (Kgs)', readonly=True)
    driver = fields.Many2one('res.partner', related='fleet.driver_id', string='Driver')
    state = fields.Selection([('draft', 'Draft'), ('dispatched', 'Dispatched')], 'Status')
    total_weight = fields.Float('Total Weight', compute='compute_total_weight')
    weight_difference = fields.Float('Weight Difference', compute='compute_weight_difference')
    invoices = fields.Many2many('account.invoice', string='Invoices', 
        domain=[('state','=','paid'),])

    @api.depends('tonnage', 'invoices.invoice_weight')
    def compute_total_weight(self):
        for record in self:
            weight = sum(record.mapped('invoices.invoice_weight'))
            if weight > record.tonnage:
                raise ValidationError("Picking weight has exceeded truck tonnage!")
            else:
                record.total_weight = weight
    
    @api.depends('total_weight', 'tonnage')
    def compute_weight_difference(self):
        for record in self:
            record.weight_difference = record.tonnage - record.total_weight

    @api.depends('invoices', 'fleet')
    def dispatch(self):
        picking_ids = tuple(self.invoices.ids)
        self.env.cr.execute("UPDATE account_invoice SET is_shipped = True WHERE id IN %s", 
            (picking_ids,))
        self.env.cr.execute("UPDATE fleet_vehicle SET is_dispatched = True WHERE id = %s", 
            (self.fleet.id,))
        self.state = 'dispatched'

    @api.depends('invoices')
    def get_picking_list_for_truck(self):
        recs = []
        prods = []
        for record in self.invoices:
            recs.append(record.invoice_line_ids.ids)
            for rec in record.invoice_line_ids:
                prods.append(rec[0].product_id.ids)
                print("******************", rec[0].product_id.id, rec[0].product_id.name, rec[0].quantity)
        flat_list = [item for sublist in prods for item in sublist]
        print(flat_list)
        print(set(flat_list))