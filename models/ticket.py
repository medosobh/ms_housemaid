from odoo import fields, models, _
from odoo.exceptions import UserError



class Ticket(models.Model):
    _name = 'HouseMaid.Ticket'
    _description = 'Ticket request for sales team'
    _rec_name = 'code'
    _order = 'name ASC'
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
    ]

    code = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    

