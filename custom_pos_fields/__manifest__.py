{
    "name": "Custom POS Fields",
    "version": "17.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Add custom fields to POS products",
    "depends": ["point_of_sale"],
    "data": ["views/product_views.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "custom_pos_fields/static/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
