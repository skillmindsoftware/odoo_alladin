{
    "name": "POS Order Fields",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Adds total_without_tax and total_discount fields to POS orders",
    "description": """
        This module adds two new fields to the POS order:
        - Total Without Tax
        - Total Discount
        These fields are computed based on the order lines.
    """,
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_order_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
