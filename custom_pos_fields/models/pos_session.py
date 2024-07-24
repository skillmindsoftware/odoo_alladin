# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    discount_rate = fields.Float(string="Discount Rate (%)", default=0.0)


class ProductProduct(models.Model):
    _inherit = "product.product"

    discount_rate = fields.Float(
        related="product_tmpl_id.discount_rate", readonly=False
    )


class PosSession(models.Model):
    _inherit = "pos.session"

    def _pos_ui_models_to_load(self):
        models_to_load = super()._pos_ui_models_to_load()
        models_to_load.append("product.product")
        _logger.info(f"Models to load in POS: {models_to_load}")
        return models_to_load

    def _loader_params_product_product(self):
        params = super()._loader_params_product_product()
        params["search_params"]["fields"].append("discount_rate")
        _logger.info(f"Product loader params: {params}")
        return params

    def _get_pos_ui_product_product(self, params):
        products = super()._get_pos_ui_product_product(params)
        _logger.info(f"Loaded {len(products)} products with discount_rate field")
        return products


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        for line in order_fields["lines"]:
            if line[2].get("product_id"):
                product = self.env["product.product"].browse(line[2]["product_id"])
                line[2]["discount"] = product.discount_rate
                _logger.info(
                    f"Applied discount {product.discount_rate}% to product {product.id}"
                )
        return order_fields
