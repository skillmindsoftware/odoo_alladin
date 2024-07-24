from odoo import http
from odoo.http import request
import requests
import logging

_logger = logging.getLogger(__name__)


class MpesaProxy(http.Controller):
    @http.route("/mpesa_proxy/stkpush", type="json", auth="user")
    def mpesa_stkpush_proxy(self, **kwargs):
        mpesa_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        config = request.env["ir.config_parameter"].sudo()
        access_token = config.get_param("pos_mpesa_payment.access_token")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        try:
            response = requests.post(
                mpesa_url, json=kwargs, headers=headers, timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _logger.error(f"M-Pesa API request failed: {str(e)}")
            return {"error": str(e)}
