from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku = fields.Char("SKU", compute="_compute_sku", store=True)
    name = fields.Char("Name", index="trigram", required=True, translate=True)

   @api.depends("name", "vendor_sku", "attribute_line_ids", "create_date")
    def _compute_sku(self):
        for product in self:
            name_prefix = product.name[:4].upper() if product.name else ''
            vendor_sku = product.vendor_sku[:4].upper() if product.vendor_sku else ''
            color_code = ''
            size_code = ''

            for attr_line in product.attribute_line_ids:
                if attr_line.attribute_id.name.lower() == 'color':
                    color_value = attr_line.value_ids[0] if attr_line.value_ids else None
                    if color_value:
                        color_code = color_value.name[:2].upper()
                elif attr_line.attribute_id.name.lower() == 'size':
                    size_value = attr_line.value_ids[0] if attr_line.value_ids else None
                    if size_value:
                        size_code = size_value.name.upper()

            date_code = product.create_date.strftime('%y%m') if product.create_date else ''

            product.sku = f"{name_prefix}{vendor_sku}{color_code}{size_code}{date_code}".strip()

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        record._compute_sku()
        return record

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        self._compute_sku()
        return result
