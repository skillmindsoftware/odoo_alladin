{
    "name": "POS Max % Discount",
    "version": "1.0",
    "description": "This module allows you to set a maximum positive discount for a product.",
    "summary": "Maximum positive discount for a product in the  POS Product screen",
    "author": "Elvice Ouma",
    "license": "LGPL-3",
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    # "data": ["views/pos_order_views.xml"],
    # "demo": [""],
    "auto_install": False,
    "application": False,
    "installable": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "max_pos_disc/static/**/*",
        ],
    },
}
