from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maids(models.Model):

    _name = 'housemaid.maids'
    _description = 'Records of Maids.'
    _rec_name = 'code'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one Maid!"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one Maid!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            if record.code:
                name = '[' + record.code + '] ' + record.name
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.depends('birthday')
    def _get_age(self):
        self.ensure_one()
        if not self.birthday:
            self.age = 0
        elif not self.birthday:
            raise UserError('Please define birthday for current maid')
        else:
            self.age = (date.today().year - self.birthday.year)

        return self.age

    ticket_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        string='Ticket no.',
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open to Work'),
            ('ready', 'Ready at Guesthouse'),
            ('booked', 'Booked by ticket'),
            ('backout', 'Backout'),
        ],
        default='draft',
        readonly=False,
        tracking=True,
    )
    offices_id = fields.Many2one(
        'housemaid.offices',
        string='Offices',
        required=True,
        tracking=True,
    )
    image = fields.Image(
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        default=lambda self: _('New'),
        required=True,
        tracking=True,
    )
    name = fields.Char(
        string='Name',
        default=lambda self: _('New'),
        required=True,
        tracking=True,
    )
    phone = fields.Char(
        string='Phone',
        required=False,
        index=True,
        tracking=True,
    )
    email = fields.Char(
        string='email',
        required=False,
        default=lambda self: _('name@mail.com'),
        tracking=True,
    )
    jobs_id = fields.Many2one(
        comodel_name='housemaid.jobs',
        string='Applied Jobs',
        required=True,
        tracking=True,
    )
    monthly_salary = fields.Monetary(
        string='Monthly Salary',
        currency_field='currency_id',
        required=False,
        tracking=True
    )
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        ondelete='set null',
        help="Used to display the currency when tracking monetary values",
        tracking=True,
    )
    contract_period = fields.Integer(
        string='Contract Period in Years',
        required=False,
        tracking=True
    )
    # ---------------------------
    arabic_lang = fields.Boolean(
        string="Arabic Language",
        tracking=True,

    )
    english_lang = fields.Boolean(
        string="English Language",
        tracking=True,
    )
    education = fields.Selection(
        selection=[
            ('no', 'No'),
            ('basic', 'Read and Write'),
            ('low', 'less then high school'),
            ('mid', 'high school diploma'),
            ('mid2', 'collage no dgree'),
            ('mid3', 'collage dgree'),
        ],
        string="Education level",
        help='Set the Education level',
    )
    # --------------------------------
    passport_no = fields.Char(
        string='Passport No.',
        required=True,
        tracking=True,
    )
    passport_place = fields.Char(
        string='Issue Place',
        required=True,
        tracking=True,
    )
    passport_issue_date = fields.Date(
        string='Issue Date',
        required=True,
        default=datetime.today(),
        tracking=True,
    )
    passport_expire_date = fields.Date(
        string='Expire Date',
        required=True,
        tracking=True,
    )
    # ----------------------------------------------
    religion = fields.Selection(
        string='Religion',
        selection=[
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
        ],
        tracking=True,
    )
    gender = fields.Selection(
        string='Gender',
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        tracking=True,
    )
    children_no = fields.Integer(
        string='children No',
        required=False,
        tracking=True,
    )
    birthday = fields.Date(
        string='Birthday',
        default=fields.Date.context_today,
        tracking=True,
    )
    place_of_birth = fields.Char(
        string='Place of Birth',
        required=True,
        tracking=True,
    )
    marital_status = fields.Selection(
        string='Marital Status',
        selection=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced'),
        ],
        tracking=True,
    )
    # ----------------------------
    skin_color = fields.Char(
        string='Skin Color',
        required=False,
        tracking=True,
    )
    age = fields.Integer(
        string='Age in Years',
        compute='_get_age',
        tracking=True,
    )
    hight = fields.Float(
        string='Hight in feet,inch',
        digits=(2, 1),
        required=False,
        tracking=True,
    )
    weight = fields.Char(
        string='Weight in kg',
        required=False,
        tracking=True,
    )
    # -----------------------------
    skills_cleaning = fields.Boolean(
        string="Cleaning",
        tracking=True,
    )
    skills_arabic_cooking = fields.Boolean(
        string="Arabic Cooking",
        tracking=True,
    )
    skills_baby_sitting = fields.Boolean(
        string="Baby Sitting",
        tracking=True,
    )
    skills_washing = fields.Boolean(
        string="Washing",
        tracking=True,
    )
    skills_ironing = fields.Boolean(
        string="Ironing",
        tracking=True,
    )
    skills_googlelocation = fields.Boolean(
        string="Google Location",
        tracking=True,
    )
    skills_driving = fields.Boolean(
        string="Drive License",
        tracking=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Maid.",
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        tracking=True,
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        tracking=True,
    )
    user_id = fields.Many2one(
        string="Operation Man",
        comodel_name='res.users',
        required=True,
        tracking=True,
    )
    maidslogs_ids = fields.One2many(
        string="History",
        comodel_name='housemaid.maidslogs',
        inverse_name='maids_id',
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )


class maidslogs(models.Model):
    _name = 'housemaid.maidslogs'
    _description = 'Maids Logs Records.'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Char(
        string='Date',
        required=True,
        default=datetime.today(),
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
        required=True,
        tracking=True
    )
    contract_no = fields.Char(
        string='Contract No.',
        default=lambda self: _('new'),
        required=True,
        tracking=True,
    )
    start_contract = fields.Date(
        string='Start Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    end_contract = fields.Date(
        string='End Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    maids_id = fields.Many2one(
        string='Maids',
        comodel_name='housemaid.maids',
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
