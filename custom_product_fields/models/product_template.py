from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku = fields.Char(string="SKU", compute="_compute_sku", store=True)
    vendor_sku = fields.Char("Vendor SKU", store=True)
    barcode = fields.Char(string="Barcode", store=True)

    @api.depends(
        "attribute_line_ids",
        "attribute_line_ids.value_ids",
        "create_date",
        "vendor_sku",
    )
    def _compute_sku(self):
        for product in self:
            style_code = ""
            color_code = ""
            size_code = ""
            vendor_prefix = (product.vendor_sku or "")[:3].upper()

            for attr_line in product.attribute_line_ids:
                if (
                    attr_line.attribute_id.name.lower() == "style"
                    and attr_line.value_ids
                ):
                    style_code = attr_line.value_ids[0].name[:4].upper()
                elif (
                    attr_line.attribute_id.name.lower() == "color"
                    and attr_line.value_ids
                ):
                    color_code = attr_line.value_ids[0].name[:2].upper()
                elif (
                    attr_line.attribute_id.name.lower() == "size"
                    and attr_line.value_ids
                ):
                    size_code = attr_line.value_ids[0].name[:2].upper()

            date_code = (
                product.create_date.strftime("%y%m") if product.create_date else ""
            )

            sku_components = [
                vendor_prefix,
                style_code,
                color_code,
                size_code,
                date_code,
            ]
            product.sku = "".join(filter(None, sku_components))

            if not product.barcode:
                product.barcode = product.sku

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        record._compute_sku()
        return record

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if any(field in vals for field in ["attribute_line_ids", "vendor_sku"]):
            self._compute_sku()
        return result
