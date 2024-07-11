import logging
from odoo import models
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def get_product_price(self, product, quantity=1.0, partner=False):
        # Find the price for the given product and quantity
        price = product.list_price
        _logger.info(f"details {product.name}: {price} : {product.id} : {self.id}")
        items = self.env['product.pricelist.item'].search([
            ('pricelist_id', '=', self.id),
            ('product_tmpl_id', '=', product.id)
        ], limit=1)
        _logger.info(f"Items {items}")
        if items:
            item = items[0]
            price = item.fixed_price
            _logger.info(f"Computed discounted price for product {product.name}: {price}")
        return price

    
