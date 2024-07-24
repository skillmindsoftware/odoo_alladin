from . import pos_session
from . import products

# from odoo import api, fields, models

# class ProductTemplate(models.Model):
#     _inherit = "product.template"

#     discount_rate = fields.Float(string="Discount Rate (%)", digits=(5, 2), default=0.0)
#     non_discounted_price = fields.Float(
#         string="Non-discounted Price", digits="Product Price"
#     )

#     @api.depends("list_price", "discount_rate")
#     def _compute_prices(self):
#         for product in self:
#             product.non_discounted_price = product.list_price
#             if product.discount_rate:
#                 product.list_price = product.non_discounted_price * (
#                     1 - product.discount_rate / 100
#                 )

#     @api.onchange("list_price", "discount_rate", "non_discounted_price")
#     def _onchange_prices(self):
#         if self.non_discounted_price and self.discount_rate:
#             self.list_price = self.non_discounted_price * (1 - self.discount_rate / 100)
#         elif self.list_price and self.non_discounted_price:
#             self.discount_rate = (1 - self.list_price / self.non_discounted_price) * 100


# class ProductProduct(models.Model):
#     _inherit = "product.product"

#     discount_rate = fields.Float(
#         related="product_tmpl_id.discount_rate", readonly=False
#     )
#     non_discounted_price = fields.Float(
#         related="product_tmpl_id.non_discounted_price", readonly=False
#     )

#     @api.depends("lst_price", "discount_rate")
#     def _compute_prices(self):
#         for product in self:
#             product.non_discounted_price = product.lst_price
#             if product.discount_rate:
#                 product.lst_price = product.non_discounted_price * (
#                     1 - product.discount_rate / 100
#                 )

#     @api.onchange("lst_price", "discount_rate", "non_discounted_price")
#     def _onchange_prices(self):
#         if self.non_discounted_price and self.discount_rate:
#             self.lst_price = self.non_discounted_price * (1 - self.discount_rate / 100)
#         elif self.lst_price and self.non_discounted_price:
#             self.discount_rate = (1 - self.lst_price / self.non_discounted_price) * 100
