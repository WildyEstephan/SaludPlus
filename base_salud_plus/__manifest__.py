# -*- coding: utf-8 -*-
{
    'name': "Base Salud Plus",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Salud Plus",
    'website': "http://www.saludplus.com.do",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'stock', 'crm'],

    # always loaded
    'data': [
        'data/groups.xml',
        'security/ir.model.access.csv',
        'views/medical_insurance.xml',
        'views/partner_view.xml',
        'views/diseases.xml',
        'views/physical_pressure_exam.xml',
        'views/medical_consultation.xml',
        'data/sequence.xml',
        'views/views.xml',
        'views/patient.xml',
        'views/symptoms_view.xml',
        'views/specialty.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
}
