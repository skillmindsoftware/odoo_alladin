import logging
from odoo import models, fields,api

_logger = logging.getLogger(__name__)

class CustomStockmove(models.Model):
    _inherit = 'stock.move'
   
    available_qty = fields.Char(
        string='Available Quantity'
    )

   