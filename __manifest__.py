{
    'name': 'Housemaid Sales and Operation System',
    'version': '1.0',
    'description': 'A system that help to maintain maids data and manage match \
         and hiring maid ',
    'summary': '',
    'author': 'mohamed sobh',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/offices.xml',
        'views/maids.xml'
        'views/sponsers.xml'
        # 'views/tickets.xml'

    ],
    'demo': [
        ''
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {

    }
}
