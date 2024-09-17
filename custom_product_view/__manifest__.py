{
    "name": "Custom Product View",
    "version": "1.0",
    "category": "Sales",
    "summary": "Customizes product form view with additional fields and layout changes",
    "description": """
This module adds customizations to the product form view for both product.product and product.template models:
- Adds discount_rate and sales_price fields
- Customizes the layout of the general information section
- Adds computed fields for tax-inclusive/exclusive prices
""",
    "depends": ["product", "account"],
    "data": [
        "views/product_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
