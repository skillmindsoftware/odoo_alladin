from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        result = []
        for product in self:
            # Return only the product name without internal reference (default code)
            name = product.name
            result.append((product.id, name))
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    vendor_sku = fields.Char(
        string="Vendor SKU", compute="_compute_vendor_sku", store=True
    )

    product_template_id = fields.Many2one("product.template", string="Product Template")
    size = fields.Many2one(
        "product.attribute.value",
        string="Size",
        domain="[('attribute_id.name', '=ilike', 'size')]",
    )
    color = fields.Many2one(
        "product.attribute.value",
        string="Color",
        domain="[('attribute_id.name', '=ilike', 'color')]",
    )
    barcode = fields.Char(related="product_id.barcode", string="Barcode", readonly=True)

    @api.depends("product_id")
    def _compute_vendor_sku(self):
        for line in self:
            if line.product_id:
                # Try to get default_code from product.product
                vendor_sku = line.product_id.default_code

                # If not found, try to get from product.template
                if not vendor_sku:
                    vendor_sku = line.product_id.product_tmpl_id.default_code

                line.vendor_sku = vendor_sku or False
            else:
                line.vendor_sku = False

    @api.onchange("product_template_id")
    def _onchange_product_template_id(self):
        self.ensure_one()
        self.product_id = False
        self.size = False
        self.color = False
        if self.product_template_id:
            return {
                "domain": {
                    "size": [("id", "in", self._get_attribute_values("size").ids)],
                    "color": [("id", "in", self._get_attribute_values("color").ids)],
                }
            }

    def _get_attribute_values(self, attribute_name):
        self.ensure_one()
        if self.product_template_id:
            return self.product_template_id.attribute_line_ids.filtered(
                lambda l: l.attribute_id.name.lower() == attribute_name.lower()
            ).value_ids
        return self.env["product.attribute.value"]

    @api.onchange("size", "color")
    def _onchange_variant_attributes(self):
        if self.product_template_id:
            domain = [("product_tmpl_id", "=", self.product_template_id.id)]
            if self.size:
                domain.append(
                    (
                        "product_template_attribute_value_ids.product_attribute_value_id",
                        "=",
                        self.size.id,
                    )
                )
            if self.color:
                domain.append(
                    (
                        "product_template_attribute_value_ids.product_attribute_value_id",
                        "=",
                        self.color.id,
                    )
                )
            variant = self.env["product.product"].search(domain, limit=1)
            if variant:
                self.product_id = variant
            else:
                self.product_id = False

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if not self.product_id:
            self.product_template_id = False
            self.size = False
            self.color = False
            return

        self.product_template_id = self.product_id.product_tmpl_id

        # Update price_unit and product_uom
        if not self.product_id.uom_id:
            self.product_uom = False
        else:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.standard_price

        # Set size and color based on product attributes
        self.size = False
        self.color = False
        for ptav in self.product_id.product_template_attribute_value_ids:
            if ptav.attribute_id.name.lower() == "size":
                self.size = ptav.product_attribute_value_id
            elif ptav.attribute_id.name.lower() == "color":
                self.color = ptav.product_attribute_value_id

        # You may need to add more logic here depending on what the original _onchange_product_id did
        # For example, updating taxes, account analytic, etc.

        return {}


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_line = fields.One2many(
        "purchase.order.line", "order_id", string="Order Lines", copy=True
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    sku = fields.Char(string="SKU", related="product_tmpl_id.default_code", store=True)
