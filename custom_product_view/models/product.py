from odoo import api, fields, models, _
from odoo.tools.misc import format_amount


class ProductTemplate(models.Model):
    _inherit = "product.template"

    discount_rate = fields.Float(string="Discount %", default=0.0)
    sales_price = fields.Float(
        string="Discounted Price", compute="_compute_sales_price", store=True
    )
    tax_string = fields.Char(compute="_compute_tax_string")
    cost_tax_string = fields.Char(compute="_compute_cost_tax_string")

    @api.depends("list_price", "discount_rate")
    def _compute_sales_price(self):
        for product in self:
            product.sales_price = product.list_price * (
                1 - (product.discount_rate / 100)
            )

    @api.depends("taxes_id", "list_price")
    def _compute_tax_string(self):
        for record in self:
            record.tax_string = record._construct_tax_string(
                record.list_price, record.taxes_id
            )

    @api.depends("supplier_taxes_id", "standard_price")
    def _compute_cost_tax_string(self):
        for record in self:
            record.cost_tax_string = record._construct_tax_string(
                record.standard_price, record.supplier_taxes_id
            )

    def _construct_tax_string(self, price, taxes):
        currency = self.currency_id
        res = taxes.compute_all(price, product=self, partner=self.env["res.partner"])
        joined = []
        included = res["total_included"]
        if currency.compare_amounts(included, price):
            joined.append(
                _("%s Incl. Taxes") % format_amount(self.env, included, currency)
            )
        excluded = res["total_excluded"]
        if currency.compare_amounts(excluded, price):
            joined.append(
                _("%s Excl. Taxes") % format_amount(self.env, excluded, currency)
            )
        tax_string = f"(= {', '.join(joined)})" if joined else " "
        return tax_string


class ProductProduct(models.Model):
    _inherit = "product.product"

    discount_rate = fields.Float(string="Discount %", default=0.0)
    sales_price = fields.Float(
        string="Discounted Price", compute="_compute_sales_price", store=True
    )

    @api.depends("lst_price", "discount_rate")
    def _compute_sales_price(self):
        for product in self:
            product.sales_price = product.lst_price * (
                1 - (product.discount_rate / 100)
            )

    @api.depends("taxes_id", "lst_price")
    def _compute_tax_string(self):
        for record in self:
            record.tax_string = record.product_tmpl_id._construct_tax_string(
                record.lst_price, record.taxes_id
            )

    @api.depends("supplier_taxes_id", "standard_price")
    def _compute_cost_tax_string(self):
        for record in self:
            record.cost_tax_string = record.product_tmpl_id._construct_tax_string(
                record.standard_price, record.supplier_taxes_id
            )
