from odoo import models, fields, api


class PosOrderInherit(models.Model):
    _inherit = "pos.order"

    total_without_tax = fields.Float(
        string="Total Without Tax", compute="_compute_totals", store=True
    )
    total_discount = fields.Float(
        string="Total Discount", compute="_compute_totals", store=True
    )

    @api.depends("lines.price_subtotal_incl", "lines.discount")
    def _compute_totals(self):
        for order in self:
            order.total_without_tax = sum(line.price_subtotal for line in order.lines)
            order.total_discount = sum(
                (line.price_unit * line.qty * line.discount) / 100
                for line in order.lines
            )


class PosOrderLineInherit(models.Model):
    _inherit = "pos.order.line"

    @api.depends("price_unit", "tax_ids", "qty", "discount", "product_id")
    def _compute_amount_line_all(self):
        super(PosOrderLineInherit, self)._compute_amount_line_all()
        for line in self:
            line.order_id._compute_totals()
