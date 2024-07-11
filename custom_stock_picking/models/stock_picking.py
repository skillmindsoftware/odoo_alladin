import logging
from odoo import models, fields,api

_logger = logging.getLogger(__name__)

class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'
   
    custom_field = fields.Char(string='Custom Field')
    purchase_order_id = fields.Many2one('purchase.order', string='Source Document')
    purchase_order_name = fields.Char(string='Purchase Order Name', related='purchase_order_id.name', store=True, readonly=True)


    def fetch_purchase_order_data(self):
        if self.purchase_order_id:
            purchase_order = self._fetch_purchase_order(self.purchase_order_id.id)
            if purchase_order:
                self._populate_fields_from_purchase_order(purchase_order)

    def _fetch_purchase_order(self, purchase_order_id):
        purchase_order = self.env['purchase.order'].browse(purchase_order_id)
        if purchase_order.exists():
            return purchase_order
        return None

    def _populate_fields_from_purchase_order(self, purchase_order):
        self.move_ids_without_package = [(5, 0, 0)]  # Clear existing moves
        #warehouse = self.env['stock.warehouse'].browse(8)
        warehouse_location_id = 8#warehouse.location_id.id

            # Calculate the available quantity
        
        moves = []
        for line in purchase_order.order_line:
            #available_qty = self.env['stock.quant']._get_available_quantity(self.env['product.product'].browse(line.product_id), warehouse_location_id)
            stock_quants = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id', '=', 8)])
            available_qty = sum(quant.quantity for quant in stock_quants)
            move = {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'product_uom': line.product_uom.id,
                'name': line.name,
                'available_qty': available_qty,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_type_id': self.picking_type_id.id,
                'company_id': self.company_id.id,
            }
            moves.append((0, 0, move))
        self.move_ids_without_package = moves
    

   