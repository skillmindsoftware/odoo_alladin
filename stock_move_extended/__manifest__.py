{
    "name": "Stock Move Extended",
    "version": "1.0",
    "category": "Inventory",
    "summary": "Adds available quantity field to stock moves",
    "description": """
        This module extends the stock.move model to add a product_available_qty field.
    """,
    "depends": ["stock"],
    "data": [
        "views/stock_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
