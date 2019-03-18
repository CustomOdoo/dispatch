# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetDispatch(models.Model):
    _name = 'fleet.dispatch'
    _description = 'Fleet Dispatch'
    _inherit = 'mail.thread'

    fleet = fields.Many2one('fleet.vehicle', string='Fleet', 
        domain=[('is_dispatched','=',False)])
    tonnage = fields.Float(related='fleet.tonnage', string='Tonnage', readonly=True)
    driver = fields.Many2one('res.partner', related='fleet.driver_id', string='Driver')
    stock_picking = fields.Many2many('stock.picking', string='Stock Transfer',
        domain=[('state','=','done')])
    state = fields.Selection([('draft', 'Draft'), ('dispatched', 'Dispatched')], 'Status')
    total_weight = fields.Float('Total Weight', compute='compute_total_weight')

    @api.depends('tonnage', 'stock_picking')
    def compute_total_weight(self):
        for record in self:
            total_weight_ids = tuple(record.stock_picking.ids)
            if total_weight_ids:
                self.env.cr.execute("SELECT sum(weight_total) FROM stock_picking WHERE id IN %s", 
                    (total_weight_ids,))
                weight = self.env.cr.fetchall()[0][0]
                if weight > record.tonnage:
                    raise ValidationError("Picking weight has exceeded truck tonnage!")
                else:
                    record.total_weight = weight

    @api.depends('stock_picking', 'fleet')
    def dispatch(self):
        picking_ids = tuple(self.stock_picking.ids)
        self.env.cr.execute("UPDATE stock_picking SET is_shipped = True WHERE id IN %s", 
            (picking_ids,))
        self.env.cr.execute("UPDATE fleet_vehicle SET is_dispatched = True WHERE id = %s", 
            (self.fleet.id,))
        self.state = 'dispatched'
        
