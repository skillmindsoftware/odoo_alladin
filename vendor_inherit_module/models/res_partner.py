from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    email = fields.Char(required=True)
    vendor_sku = fields.Char(string="Vendor SKU", required=True)
