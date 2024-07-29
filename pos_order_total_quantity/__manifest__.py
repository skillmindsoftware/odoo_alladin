{
    'name': 'POS Order Total Quantity',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Add total quantity to POS orders list view',
    'description': """
        This module adds a 'Total Quantity' column to the POS orders list view,
        showing the total quantity sold for each order and the sum at the bottom.
    """,
    'author': 'Edwin Mutua',
    'website': 'https://www.skillmindsoftware.com',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_order_views.xml',
        'data/pos_order_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}