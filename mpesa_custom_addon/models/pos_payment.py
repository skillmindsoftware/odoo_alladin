from odoo import models, fields, api


class PosPayment(models.Model):
    _inherit = "pos.payment"

    confirmation_code = fields.Char(string="Confirmation Code")

    @api.model
    def update_payment_confirmation_code(self, order_name, confirmation_code):
        company_id = self.env.context.get("company_id")
        domain = [("pos_order_id.name", "=", order_name)]
        if company_id:
            domain.append(("company_id", "=", company_id))

        payment = self.search(domain, limit=1)
        if payment:
            payment.write({"confirmation_code": confirmation_code})
            return True
        return False
