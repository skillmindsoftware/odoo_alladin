from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    vendor_sku = fields.Char(string="Vendor SKU")


class ProductProduct(models.Model):
    _inherit = "product.product"

    sku = fields.Char(string="SKU", related="product_tmpl_id.default_code", store=True)
