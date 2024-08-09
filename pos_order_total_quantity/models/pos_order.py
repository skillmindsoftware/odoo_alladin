from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_quantity = fields.Float(string='Total Quantity', compute='_compute_total_quantity', store=True)

    @api.depends('lines.qty')
    def _compute_total_quantity(self):
        for order in self:
            order.total_quantity = sum(order.lines.mapped('qty'))