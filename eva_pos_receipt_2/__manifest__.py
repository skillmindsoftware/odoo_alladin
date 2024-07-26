# Copyright 2011-2016 Agile Business Group
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "eva_pos_receipt",
    "version": "17.0.1.0.1",
    "category": "Accounting & Finance",
    "summary": "Allows to force invoice numbering on specific invoices",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoicing",
    "license": "AGPL-3",
    # "depends": ["account"],
    "data": [
        # "security/security.xml",
        # "views/assets.xml",
    ],
    "installable": True,
    'assets': {
        'web.assets.backend': ['eva_pos_receipt/static/src/**/*'],
        'point_of_sale._assets_pos': [
            'eva_pos_receipt/static/src/js/pos_receipt_total_qty.js',
            'eva_pos_receipt/static/src/xml/pos_receipt_total_qty.xml',
            'eva_pos_receipt/static/src/xml/pos_header.xml',
            # 'eva_pos_receipt/static/src/pos_receipts.css',
        ],
    },
    'images': ['static/description/banner.png'],
}
