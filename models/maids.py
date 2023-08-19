from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo.modules.module import get_module_resource
import base64


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
        else:
            self.age = (date.today().year - self.birthday.year)
        return self.age

    # object in Maid form

    def action_draft_maid(self):
        self.ensure_one()
        # maid state to draft
        self.state = 'draft'
        self.tickets_id = False
        self.sponsers_id = False

    def action_open_maid(self):
        self.ensure_one()
        # maid state to open
        self.state = 'open'
        # update ticket state
        self.tickets_id.state = 'found'
        self.tickets_id.garanty_day = False
        self.garanty_day = False
        # create activity to user to check on maid

    def action_ready_maid(self):
        self.ensure_one()
        # maid state to ready
        self.state = 'ready'
        # update ticket state
        self.tickets_id.state = 'found'
        self.tickets_id.garanty_day = False
        self.garanty_day = False
        # create activity to user to check on maid

    def action_backout_maid(self):
        self.ensure_one()
        # check maid if linked break link
        if self.tickets_id.id == False:
            self.state = 'backout'
            self.garanty_day = False
        else:
            # maid state to backout
            self.state = 'backout'
            # change ticket state
            self.tickets_id.state = 'runout'
            self.tickets_id = False
            self.sponsers_id = False
            self.garanty_day = False

    # object in search page
    def action_check_maid(self):
        self.ensure_one()
        # test maids_tickets_id exist or not?
        if self.tickets_id.id == False:
            active_id = self._context.get('active_id')
            if active_id:
                ticket_rec = self.env['housemaid.tickets'].browse(
                    int(active_id))
            # create an activity
            self.activity_schedule(
                'ms_housemaid.mail_act_checking',
                user_id=ticket_rec.user_id,
                note=f'Sponser: {ticket_rec.new_sponsers_id} ask checking Maid: {self.name} of the ticket {ticket_rec.code}'
            )
            # change ticket state
            ticket_rec.state = 'check'
            # maid state to check
            self.state = 'check'
        else:
            raise UserError(
                "Maid already linked to another Ticket review maid cv.!")
        # refresh page
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_hiring_maid(self):
        self.ensure_one()
        # test maids_tickets_id exist or not?
        if self.tickets_id.id == False:
            active_id = self._context.get('active_id')
            if active_id:
                ticket_rec = self.env['housemaid.tickets'].browse(
                    int(active_id))
            # create an activity
            self.activity_schedule(
                'ms_housemaid.mail_act_hiring',
                user_id=ticket_rec.user_id,
                note=f'Sponser: {ticket_rec.new_sponsers_id} ask hiring Maid: {self.name} of the ticket {ticket_rec.code}'
            )
            # change ticket state
            ticket_rec.state = 'hiring'
            # maid state to check
            self.state = 'hiring'
        else:
            raise UserError(
                "Maid already linked to another Ticket review maid cv.!")
        # refresh page
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),  # 1 > #2   fa-unlink # show in search page
            # 2 > #3 fa-question-circle # show in action page
            ('check', 'Checking'),
            ('open', 'Open to Work'),  # 3 > #4 fa-hourglass # show in search page
            # 3 > #4 fa-hourglass # show in search page
            ('ready', 'Ready Inhouse'),  # fa-home
            ('transfer', 'Treansfer'),  # fa-retweet #  fa-exchange
            ('hiring', 'Hiring'),  # 5 fa-link # show in action page
            ('garanty', 'Garanty'),  # fa-warning
            ('work', 'Working'),  # fa-user-plus
            ('backout', 'Backout'),  # 3  stop here fa-ban # show in Maid Form only
            ('runaway', 'runaway'),
            ('contract_end', 'Contract End'),
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
        index=True,
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
        string='Email',
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
        required=True,
        tracking=True
    )
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        ondelete='set null',
        help="Used to display the currency when tracking monetary values",
        required=False,
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
        required=False,
        tracking=True,
    )
    english_lang = fields.Boolean(
        string="English Language",
        required=False,
        tracking=True,
    )
    educations_id = fields.Many2one(
        comodel_name='housemaid.educations',
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
    identation = fields.Char(
        string='Identation No.',
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
        required=True,
        tracking=True,
    )
    place_of_birth = fields.Char(
        string='Place of Birth',
        required=False,
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
    weight = fields.Integer(
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
    user_id = fields.Many2one(
        string="Operation Man",
        comodel_name='res.users',
        required=True,
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
    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        string='Ticket no.',
        required=False,
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
        required=False,
        tracking=True,
    )
    garanty_day = fields.Date(
        string='Start Garanty Date',
        required=False,
        tracking=True,
    )
    maidscontracts_ids = fields.One2many(
        string="History",
        comodel_name='housemaid.maidscontracts',
        inverse_name='maids_id',
        required=False,
        tracking=True,
    )
    contract_no = fields.Char(
        string='Contract No.',
        required=False,
        tracking=True,
    )
    visa_no = fields.Char(
        string='Visa No.',
        required=False,
        tracking=True
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
