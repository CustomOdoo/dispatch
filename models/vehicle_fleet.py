from odoo import models, fields, api, _ 

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    tonnage = fields.Float('Tonnage')
    is_dispatched = fields.Boolean('Is Dispatched', default=False, readonly=True)
