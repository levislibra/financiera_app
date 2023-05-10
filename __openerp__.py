# -*- coding: utf-8 -*-
{
    'name': "Financiera App",

    'summary': """
        Manejo de opciones para la app""",

    'description': """
        Manejo de opciones para la app
    """,

    'author': "Librasoft",
    'website': "https://libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'financiera_prestamos', 'financiera_pagos_360', 'financiera_sms',
    'financiera_buro_rol_base', 'financiera_cobranza_mora'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/app_config.xml',
		'views/extends_financiera_prestamo.xml',
        'views/extends_res_company.xml',
        'views/extends_res_partner.xml',
		'views/onboarding.xml',
		'wizards/financiera_prestamo_cambiar_monto_portal_wizard.xml',
		'wizards/res_partner_set_password_wizard.xml',
		'wizards/financiera_prestamo_cuota_to_excel_wizard.xml',
		'wizards/invoice_refacturar_wizard.xml',
		'data/defaultdata.xml',
		'data/ir_cron.xml',
    ],
		'css': [
			'static/src/css/perfil_portal.css',
			'static/src/css/app.css',
		],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}