from odoo import fields, models, _
from odoo.exceptions import UserError

class Maid(models.Model):

    _name = 'Housemaid.Maid'
    _description = 'a table of maids data '
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one equipment !"),
    ]

    code = fields(
        string = 'Code',
        required=True
    )
    name = fields.Char(
        string = 'Name',
        required = True
    )
    identity = fields.Char(
        string = 'National Identity',
        required=True
    )
    passport_no = fields.Char(
        string='Passport No.',
        required=True
    )
    place_of_birth = fields.Char(
        string='Place of birth',
        required=True
    ) 
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office."
    )
    birthday = fields.Date(
        string='field_name',
        default=fields.Date.context_today,
    )
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )
    marital_status = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced'),
        ]
    )
    description = fields.Text(
        string = 'Description')


class MaidActivity(models.Model):
    _name = 'Housemaid.MaidActivity'
    _description = 'ModelName'
    _check_company_auto = True
    _sql_constraints = [
        ('visa_code_uniq', 'unique(visa_code)', "A visa code can only be assigned to one maid !"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one maid !"),
        ('contract_code_uniq', 'unique(contract_code)', "A contract code can only be assigned to one maid !"),
    ]

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )
    visa_code = fields.Char(
        string = 'Visa Code',
        required=True
    )
    contract_code = fields.Char(
        string = 'Visa Code',
        required=True
    )
    sponser_id = fields.Many2one(
        string = 'Sponser',
        comodel_name='Housmaid.Sponser',
    )
    start_contract = fields.Date(
        string='field_name',
        default=fields.Date.context_today,
    )
    end_contract = fields.Date(
        string='field_name',
        default=fields.Date.context_today,
    )
    