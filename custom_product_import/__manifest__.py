# -*- coding: utf-8 -*-
{
    "name": "Custom Product Import",
    "version": "1.0",
    "summary": "Import products from CSV or Excel files",
    "description": """
This module allows users to import products from CSV or Excel files.
It provides a user-friendly interface for file upload and processing, and ensures
that imported data is correctly created as products with variants.
    """,
    "author": "Elvice Ouma",
    "website": "https://www.skillmindsoftware.com",
    "category": "Inventory",
    "depends": ["base", "product", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/import_product_views.xml",
        "data/product_import_template.csv",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
