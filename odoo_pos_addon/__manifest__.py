{
    "name": "POS Custom Module",
    "version": "1.0",
    "description": "Customizations for the pos screen",
    "summary": "Many changes",
    "author": "Elvice Ouma",
    "license": "LGPL-3",
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    "data": ["views/pos_order_views.xml"],
    # "demo": [""],
    "auto_install": False,
    "application": False,
    "assets": {
        "point_of_sale._assets_pos": [
            "odoo_pos_addon/static/**/*",
        ],
    },
}
