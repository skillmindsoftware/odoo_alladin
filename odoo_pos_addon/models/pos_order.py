# File: pos_order.py

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    confirmation_code = fields.Char(string="Confirmation Code", readonly=True)

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        if "confirmation_code" in ui_order:
            order_fields["confirmation_code"] = ui_order["confirmation_code"]
        _logger.info(f"Order fields with confirmation code: {order_fields}")
        return order_fields

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)
        for order in orders:
            if "data" in order and "confirmation_code" in order["data"]:
                created_order = self.browse(order_ids[0]["id"])
                created_order.write(
                    {"confirmation_code": order["data"]["confirmation_code"]}
                )
                _logger.info(
                    f"Updated order {created_order.name} with confirmation code: {order['data']['confirmation_code']}"
                )
        return order_ids

    @api.model
    def update_order_confirmation_code(self, order_name, confirmation_code):
        order = self.search([("pos_reference", "=", order_name)], limit=1)
        if order:
            order.write({"confirmation_code": confirmation_code})
            _logger.info(
                f"Updated confirmation code for order {order_name}: {confirmation_code}"
            )
            return True
        _logger.warning(f"Order not found for updating confirmation code: {order_name}")
        return False
