{
    'name': 'HouseMaid Sales and Operation System',
    'version': '1.0',
    'description': 'A system that help to maintain maids data and manage match \
         and hiring maid ',
    'summary': '',
    'author': 'mohamed sobh',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Human Resources/Employees',
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
    ],
    'data': [
        'views/menu.xml',
        'views/maids.xml'
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