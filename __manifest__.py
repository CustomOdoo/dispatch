# -*- coding: utf-8 -*-
{
    'name': "dispatch",

    'summary': """
        Fleet Dispatch Module""",

    'description': """
        Fleet Dispatch Module
    """,

    'author': "AthmanZiri",
    'website': "https://www.innovus.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dispatch.xml',
        'views/vehicle_fleet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'sequence': 2,
}