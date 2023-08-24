{
    'name': 'Housemaid Sales and Operation System',
    'version': '15.0.1.0',
    'description': 'A system that help to maintain maids data and manage match \
         and hiring maid ',
    'summary': '',
    'author': 'mohamed sobh',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base',
        'base_setup',
        'mail',
        'resource',
        'web_kanban_gauge',
        'portal',
        'web',
        'account',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_views.xml',
        'data/data_views.xml',
        'wizard/close_ticket_wizard.xml',
        'wizard/contract_wizard.xml',
        'views/maids_template.xml',
        'views/menu.xml',
        'views/offices.xml',
        'views/maids.xml',
        'views/maids_contracts.xml',
        'views/sponsers.xml',
        'views/tickets.xml',
        'views/jobs.xml',
        'views/close_reason.xml',
        'views/closed_tickets.xml',
        'views/educations.xml',
        'report/maid_report_template.xml',
    ],
    'demo': [
        ''
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            # 'ms_housemaid/static/src/js/custom_script.js',
            'ms_housemaid/static/scr/js/maids_create_validate.js',
            'ms_housemaid/static/scr/js/display_image.js',
        ]
    },
}
