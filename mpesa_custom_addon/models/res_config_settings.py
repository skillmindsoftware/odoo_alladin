from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mpesa_shortcode = fields.Char(
        string="M-Pesa Shortcode", config_parameter="pos_mpesa_payment.shortcode"
    )
    mpesa_passkey = fields.Char(
        string="M-Pesa Passkey", config_parameter="pos_mpesa_payment.passkey"
    )
    mpesa_consumer_key = fields.Char(
        string="M-Pesa Consumer Key", config_parameter="pos_mpesa_payment.consumer_key"
    )
    mpesa_consumer_secret = fields.Char(
        string="M-Pesa Consumer Secret",
        config_parameter="pos_mpesa_payment.consumer_secret",
    )
    mpesa_callback_url = fields.Char(
        string="M-Pesa Callback URL", config_parameter="pos_mpesa_payment.callback_url"
    )
