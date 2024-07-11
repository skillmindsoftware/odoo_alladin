{
    "name": "Required Customer POS",
    "version": "1.0",
    "description": "This  modules  inherits  the  patners editor  and  makes  more  fields  required  for  creating  a  customer.",
    "summary": "This  modules  inherits  the  patners editor  and  makes  more  fields  required  for  creating  a  customer.",
    "author": "Elvice Ouma",
    "license": "LGPL-3",
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    "auto_install": False,
    "application": False,
    "installable": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "required_customer_pos/static/**/*",
        ],
    },
}
