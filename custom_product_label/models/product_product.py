import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.template'

    discounted_price = fields.Float(compute='_compute_discounted_price', string='Discounted Price')

    @api.depends('list_price')
    def _compute_discounted_price(self):
        pricelist = self.env['product.pricelist'].search([], limit=1)  # Get the first available pricelist
        for product in self:
            if pricelist:
                # Compute the discounted price using the pricelist
                product.discounted_price = pricelist.get_product_price(product, 1.0, False)
                _logger.info(f"Computed discounted price for product {product.name}: {product.discounted_price}")
            else:
                product.discounted_price = product.list_price  # Fallback to list price if no pricelist
                _logger.warning(f"No pricelist found for product {product.name}, using list price.")
