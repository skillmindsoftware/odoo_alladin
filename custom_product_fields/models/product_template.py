from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    supplier_code = fields.Char(string="Supplier Code")
    mm_yr = fields.Date(string="MM & YR")
    sku = fields.Char(string="SKU", compute="_compute_sku", store=True)
    custom_description = fields.Char(string="Custom Description")

    @api.depends("supplier_code", "mm_yr", "custom_description")
    def _compute_sku(self):
        for product in self:
            # You can customize this logic based on your specific requirements
            if product.supplier_code and product.mm_yr and product.custom_description:
                product.sku = f"{product.supplier_code[:4]}{product.mm_yr.strftime('%m%y')}{product.custom_description[:4]}"
            else:
                product.sku = False
