# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetDispatch(models.Model):
    _name = 'fleet.dispatch'
    _description = 'Fleet Dispatch'
    _inherit = 'mail.thread'

    fleet = fields.Many2one('fleet.vehicle', string='Fleet', 
        domain=[('is_dispatched','=',False)])
    tonnage = fields.Float(related='fleet.tonnage', string='Tonnage', readonly=True)
    driver = fields.Many2one('res.partner', related='fleet.driver_id', string='Driver')
    stock_picking = fields.Many2many('stock.picking', string='Stock Transfer',
        domain=[('state','=','done'), ('is_shipped','=',False)])
    state = fields.Selection([('draft', 'Draft'), ('dispatched', 'Dispatched')], 'Status')

    @api.depends('stock_picking', 'fleet')
    def dispatch(self):
        picking_ids = tuple(self.stock_picking.ids)
        self.env.cr.execute("UPDATE stock_picking SET is_shipped = True WHERE id IN %s", 
            (picking_ids,))
        self.env.cr.execute("UPDATE fleet_vehicle SET is_dispatched = True WHERE id = %s", 
            (self.fleet.id,))
        self.state = 'dispatched'
        
