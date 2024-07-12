{
    "name": "Partner Email and Vendor SKU",
    "version": "1.0",
    "summary": "Makes email required and adds vendor SKU to partners",
    "description": "This module makes the email field required and adds a required vendor SKU field to the res.partner model.",
    "category": "Sales",
    "author": "Your Name",
    "depends": ["base"],
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
