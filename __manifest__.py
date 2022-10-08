

{
    'name': 'Real Estate Management',
    'version': '1.0.0',
    'category': 'Real Estate / Brokerage',
    'author': 'Parametric Systems',
    'summary': '',
    'sequence': -100,
    'description': """Real Estate Management System""",
    'depends': ['mail', 'product', 'base'],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            'views/menu.xml',
            'views/estate_property_view.xml',
            'views/estate_property_type_view.xml',
            'views/estate_property_tag_view.xml',
            'views/estate_property_offer_view.xml',
            'views/res_users_view.xml'
            ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {}

}
