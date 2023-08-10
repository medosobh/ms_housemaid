from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import base64
from datetime import date, datetime, timedelta


class maids(models.Model):

    _name = 'housemaid.maids'
    _description = 'Maids'
    _rec_name = 'code'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one Maid!"),
        ('name_uniq', 'unique(name)', "A name can only be assigned to one Maid!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            'ms_housemaid', 'static/img', 'maid.png')
        return base64.b64encode(open(image_path, 'rb').read())

    # object in search page
    def action_check_maid(self):
        self.ensure_one()
        # test maid ticket id exist or update?
        context = dict(self.env.context or {})
        tickets_id = context.get('tickets_id', False)
        if self.tickets_id == False:
            # maid state to check
            self.state = 'check'
            self.tickets_id = tickets_id
            # create activity to user to check on maid
            user_id = context.get('user_id', False)
            # create an activity
            # users = self.env.ref('ms_housemaid.group_housemaid_operator').users
            # for user in users:
            self.activity_schedule(
                'ms_housemaid.mail_act_checking',
                user_id=user_id,
                note=f'Please Check Maid {self.name} of the ticket {self.tickets_id.code}'
            )
            # change ticket state
            record = self.env['housemaid.tickets'].browse(tickets_id)
            record.state = 'check'
        else:
            raise UserError("Maid already linked to another Ticket!")
        # refresh page
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_reserve_maid(self):
        self.ensure_one()
        # test maid ticket id exist or update?
        context = dict(self.env.context or {})
        tickets_id = context.get('tickets_id', False)
        if self.tickets_id == False:
            # maid state to check
            self.state = 'reserve'
            self.tickets_id = tickets_id
            # create activity to user to check on maid
            user_id = context.get('user_id', False)
            # create an activity
            # users = self.env.ref('ms_housemaid.group_housemaid_operator').users
            # for user in users:
            self.activity_schedule(
                'ms_housemaid.mail_act_checking',
                user_id=user_id,
                note=f'Please Check Maid {self.name} of the ticket {self.tickets_id.code}'
            )
            # change ticket state
            record = self.env['housemaid.tickets'].browse(tickets_id)
            record.state = 'reserve'
        else:
            raise UserError("Maid already linked to another Ticket!")
        # refresh page
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    # object in Maid form
    def action_draft_maid(self):
        self.ensure_one()
        # maid state to draft
        self.state = 'draft'
        self.tickets_id = []
      

    def action_open_maid(self):
        self.ensure_one()
        # maid state to open
        for rec in self:
            rec.state = 'open'
        # create activity to user to check on maid
        # update maid field ticket id
        print('Maid open to work!')

    def action_ready_maid(self):
        self.ensure_one()
        # maid state to ready
        for rec in self:
            rec.state = 'ready'
        # create activity to user to check on maid
        # update maid field ticket id
        print('Maid Ready to Work!')

    def action_runout_maid(self):
        self.ensure_one()
        # maid state to runout
        self.state = 'runout'
        tickets_id = self.tickets_id
        if tickets_id == True:
            # change ticket state
            record = self.env['housemaid.tickets'].browse(tickets_id)
            record.state = 'runout'
            self.tickets_id = []
            self.garanty_day = []
        else:
            self.garanty_day = []
    
    def action_backout_maid(self):
        self.ensure_one()
        # maid state to backout
        self.state = 'backout'
        tickets_id = self.tickets_id
        if tickets_id == True:
            # change ticket state
            record = self.env['housemaid.tickets'].browse(tickets_id)
            record.state = 'runout'
            self.tickets_id = []
            self.garanty_day = []
        else:
            self.garanty_day = []

    # object in action page
    def action_hiring_maid(self):
        self.ensure_one()
        # maid state to hiring
        for rec in self:
            rec.state = 'hiring'
        # create activity to operation user to proceed on maid
        # update maid field ticket id once more!!
        print('Recruitment Procedures!')

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

    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),  # 1 > #2   fa-unlink # show in search page
            # 2 > #3 fa-question-circle # show in action page
            ('check', 'Checking'),
            ('open', 'Open to Work'),  # 3 > #4 fa-hourglass # show in search page
            # 3 > #4 fa-hourglass # show in search page
            ('ready', 'Ready at Guesthouse'),
            ('reserve', 'Reserved'),  # 4 > #5   fa-link # show in action page
            ('hiring', 'Hiring'),  # 5 fa-link # show in action page
            ('backout', 'Backout'),  # 3  stop here fa-ban # show in Maid Form only
            # no search state!
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
        default=_default_image,
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
        required=True,
        tracking=True
    )
    # ---------------------------
    arabic_lang = fields.Boolean(
        string="Arabic Language",
        required=False,
        tracking=True,

    )
    english_lang = fields.Boolean(
        string="English Language",
        required=False,
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
        required=False,
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
        required=False,
        tracking=True,
    )
    passport_issue_date = fields.Date(
        string='Issue Date',
        required=False,
        default=datetime.today(),
        tracking=True,
    )
    passport_expire_date = fields.Date(
        string='Expire Date',
        required=False,
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
        required=False,
        tracking=True,
    )
    gender = fields.Selection(
        string='Gender',
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        required=False,
        tracking=True,
    )
    children_no = fields.Integer(
        string='Children No',
        required=False,
        tracking=True,
    )
    birthday = fields.Date(
        string='Birthday',
        default=fields.Date.context_today,
        required=False,
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
        required=False,
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
        required=False,
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
        required=False,
        tracking=True,
    )
    skills_arabic_cooking = fields.Boolean(
        string="Arabic Cooking",
        required=False,
        tracking=True,
    )
    skills_baby_sitting = fields.Boolean(
        string="Baby Sitting",
        required=False,
        tracking=True,
    )
    skills_washing = fields.Boolean(
        string="Washing",
        required=False,
        tracking=True,
    )
    skills_ironing = fields.Boolean(
        string="Ironing",
        required=False,
        tracking=True,
    )
    skills_googlelocation = fields.Boolean(
        string="Google Location",
        required=False,
        tracking=True,
    )
    skills_driving = fields.Boolean(
        string="Drive License",
        required=False,
        tracking=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Maid.",
        default=lambda self: self.offices_id.country_id,
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=False,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        required=False,
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
        default=lambda self: self.offices_id.user_id,
        required=True,
        tracking=True,
    )
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=False,
        string='Ticket no.',
    )
    garanty_day = fields.Date(
        string='Start Garanty Date',
        required=False,
        tracking=True,
    )
    maidslogs_ids = fields.One2many(
        string="History",
        comodel_name='housemaid.maidslogs',
        inverse_name='maids_id',
        required=False,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        required=True,
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
