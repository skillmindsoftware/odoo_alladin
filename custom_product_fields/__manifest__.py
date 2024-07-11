{
    'name': 'Custom Product Fields',
    'version': '1.0',
    'depends': ['product'],
    'author': 'Your Name',
    'category': 'Inventory',
    'description': """
    Adds custom fields to product template, including auto-computed SKU.
    """,
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}