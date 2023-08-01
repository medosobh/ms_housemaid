from odoo import fields, models, _
from odoo.exceptions import UserError


class maids(models.Model):

    _name = 'housemaid.maids'
    _description = 'Records of Maids.'
    _rec_name = 'passport_no'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one equipment !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(
        string='Code',
        default=lambda self: _('New'),
        required=True,
        tracking=True
    )
    phone = fields.Char(
        string='Phone',
        required=True,
        index=True,
        tracking=True
    )
    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True
    )
    email = fields.Char(
        string='email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True
    )
    identity = fields.Char(
        string='National Identity',
        required=True,
        tracking=True
    )
    passport_no = fields.Char(
        string='Passport No.',
        required=True,
        tracking=True
    )
    place_of_birth = fields.Char(
        string='Place of birth',
        required=True,
        tracking=True
    )
    birthday = fields.Date(
        string='Birthday',
        default=fields.Date.context_today,
        tracking=True
    )
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        tracking=True
    )
    marital_status = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced'),
        ],
        tracking=True
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.",
        tracking=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        tracking=True
    )
    description = fields.Text(
        string='Description',
        tracking=True
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True,
        tracking=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Operation Man",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        ondelete='set null',
        help="Used to display the currency when tracking monetary values",
        tracking=True
    )


class maidslogs(models.Model):
    _name = 'housemaid.maidslogs'
    _description = 'Maids Logs Records.'
    _check_company_auto = True
    _sql_constraints = [
        ('visa_no_uniq', 'unique(visa_code)',
         "A visa code can only be assigned to one maid !"),
        ('contract_no_uniq', 'unique(contract_code)',
         "A contract code can only be assigned to one maid !"),
    ]

    date = fields.Char(
        string='Date',
        required=True,
        default=lambda self: _('today'),
        copy=False
    )
    visa_no = fields.Char(
        string='Visa No.',
        default=lambda self: _('new'),
        required=True
    )
    contract_no = fields.Char(
        string='Contract No.',
        default=lambda self: _('new'),
        required=True
    )
    start_contract = fields.Date(
        string='Start Date',
        default=fields.Date.context_today,
    )
    end_contract = fields.Date(
        string='End Date',
        default=fields.Date.context_today,
    )
