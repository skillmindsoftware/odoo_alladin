{
    'name': 'Stock Transfer Fetch Data',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Fetch available stock data for internal transfers',
    'description': """
        This module adds a 'Fetch Data' button to internal transfer forms.
        It populates move lines with available stock from the source location.
    """,
    'author': 'Edwin Mutua',
    'website': 'https://www.skillmindsoftware.com',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_transfer_fetch_data/static/src/js/stock_picking_fetch_data.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}