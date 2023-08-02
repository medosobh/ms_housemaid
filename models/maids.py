from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maids(models.Model):

    _name = 'housemaid.maids'
    _description = 'Records of Maids.'
    _rec_name = 'passport_no'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one Maid!"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one Maid !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            'ms_housemaid', 'static/img', 'maid.png')
        return base64.b64encode(open(image_path, 'rb').read())

    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('close', 'Close'),
            ('cancel', 'Cancel')
        ],
        default='draft',
        readonly=True,
    )
    skills = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Skills",
        help='Set the overall skills level.')
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
    image_1920 = fields.Image(
        default=_default_image
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
    religion = fields.Selection(
        [
            ('Baha i', 'Baha i'),
            ('Buddhism', 'Buddhism'),
            ('Christianity', 'Christianity'),
            ('Confucianism', 'Confucianism'),
            ('Hinduism', 'Hinduism'),
            ('Islam', 'Islam'),
            ('Jainism', 'Jainism'),
            ('Judaism', 'Judaism'),
            ('Shinto', 'Shinto'),
            ('Sikhism', 'Sikhism'),
            ('Taoism', 'Taoism'),
            ('Zoroastrianism', 'Zoroastrianism'),
        ]
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
    maidslogs_ids = fields.One2many(
        comodel_name='housemaid.maidslogs',
        inverse_name='maids_id',
        string="History",
        tracking=True
    )


class maidslogs(models.Model):
    _name = 'housemaid.maidslogs'
    _description = 'Maids Logs Records.'

    date = fields.Char(
        string='Date',
        required=True,
        default=datetime.today(),
        copy=False,
        tracking=True
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('open', 'Open to Work'),
            ('work', 'Working'),
            ('valuated', '90 Days Valuation'),
            ('backout', 'Backout'),
            ('reserve', 'Reserved'),
        ],
        default='draft',
        tracking=True
    )
    visa_no = fields.Char(
        string='Visa No.',
        default=lambda self: _('new'),
        index=True,
        required=True,
        tracking=True
    )
    contract_no = fields.Char(
        string='Contract No.',
        default=lambda self: _('new'),
        index=True,
        required=True,
        tracking=True
    )
    start_contract = fields.Date(
        string='Start Date',
        default=fields.Date.context_today,
        tracking=True
    )
    end_contract = fields.Date(
        string='End Date',
        default=fields.Date.context_today,
        tracking=True
    )
    maids_id = fields.Many2one(
        comodel_name='housemaid.maids',
        string='Maids',
        tracking=True
    )
