# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveExtended(models.Model):
    _inherit = "stock.move"

    product_available_qty = fields.Float(
        string="Available Quantity",
        compute="_compute_product_available_qty",
        store=True,
        help="The available quantity of the product in the source location.",
    )

    @api.depends("product_id", "location_id", "product_uom_qty")
    def _compute_product_available_qty(self):
        for move in self:
            if move.product_id and move.location_id:
                available_qty = move.product_id.with_context(
                    location=move.location_id.id
                ).qty_available
                move.product_available_qty = available_qty
            else:
                move.product_available_qty = 0.0


# You can add any additional logic or methods here if needed
