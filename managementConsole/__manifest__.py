{
    'name': "Management Console",
    'version': '1.0',
    'depends': ['base', 'multi_step_wizard'],
    'license': 'Other proprietary',
    'author': 'myodoo Services',
    'company': 'myodoo Services',
    'maintainer': 'myodoo Services',
    'category': 'Category',
    'summary': "Odoo Module to display server details",
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
      'security/ir.model.access.csv',
      'views/pmc_views.xml',
      'views/optout_views.xml',
    ],    
    'license': 'LGPL-3',
    'support': 'mail@myodoo.services'
   
}
