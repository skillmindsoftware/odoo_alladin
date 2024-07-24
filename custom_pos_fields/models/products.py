# from odoo import fields, models


# class ProductTemplate(models.Model):
#     _inherit = "product.template"

#     discount_rate = fields.Float(string="Discount Rate (%)", digits=(5, 2), default=0.0)


# class ProductProduct(models.Model):
#     _inherit = "product.product"

#     discount_rate = fields.Float(
#         related="product_tmpl_id.discount_rate", readonly=False
#     )
