from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def fetch_available_stock(self, location_id):
        location = self.env['stock.location'].browse(location_id)
        quants = self.env['stock.quant'].search([
            ('location_id', '=', location_id),
            ('quantity', '>', 0)
        ])
        
        return [{
            'product_id': quant.product_id.id,
            'product_name': quant.product_id.name,
            'quantity': quant.quantity,
            'uom_id': quant.product_uom_id.id,
        } for quant in quants]

    def action_fetch_stock_data(self):
        self.ensure_one()
        if self.location_id:
            available_stock = self.fetch_available_stock(self.location_id.id)
            return {
                'type': 'ir.actions.client',
                'tag': 'populate_move_lines',
                'params': {
                    'available_stock': available_stock,
                    'picking_id': self.id,
                }
            }
        return {'type': 'ir.actions.act_window_close'}