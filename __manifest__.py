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
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_views.xml',
        'data/data_views.xml',
        'wizard/closeticket_wizard.xml',
        'wizard/contract_wizard.xml',
        'views/maids_template.xml',
        'views/menu.xml',
        'views/offices.xml',
        'views/maids.xml',
        'views/maidscontracts.xml',
        'views/sponsers.xml',
        'views/tickets.xml',
        'views/jobs.xml',
        'views/closereason.xml',
        'views/closedtickets.xml',
        'views/educations.xml',
    ],
    'demo': [
        ''
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'ms_housemaid/static/src/js/custom_script.js',
        ]
    },
}
