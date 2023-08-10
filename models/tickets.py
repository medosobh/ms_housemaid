from odoo import api, fields, models, _
from odoo.exceptions import UserError


class tickets(models.Model):
    _name = 'housemaid.tickets'
    _description = 'Tickets'
    _rec_name = 'code'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one ticket!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        if not vals.get('code') or vals['code'] == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'housemaid.sales.tickets') or _('New')
        return super(tickets, self).create(vals)

    def action_search_ticket(self):
        self.ensure_one()
        self.state = 'search'
        context = dict(self.env.context or {})
        # create activity to user to check on maid
        user_id = context.get('user_id', False)
        # create an activity
        self.activity_schedule(
            'ms_housemaid.mail_act_searching',
            user_id=user_id,
            note=f'Please Search for a new Maid of the ticket {self.code}'
        )

    def action_draft_ticket(self):
        self.ensure_one()
        self.state = 'draft'
        print('action_draft_ticket')

    def action_found_ticket(self):
        self.ensure_one()
        self.state = 'found'
        print('action_avaliable_ticket')

    def action_runout_ticket(self):
        self.ensure_one()
        self.state = 'runout'
        print('action_runout_ticket')

    def action_confirm_ticket(self):
        self.ensure_one()
        self.state = 'confirm'
        print('action_confirm_ticket')

    @api.onchange('garanty_day')
    def action_garanty_ticket(self):
        self.ensure_one()
        self.state = 'garanty'
        print('action_garanty_ticket')

    def action_closed_ticket(self):
        self.ensure_one()
        self.state = 'closed'
        print('action_closed_ticket')

    code = fields.Char(
        string='Code',
        required=True,
        default=lambda self: _('New'),
        index=True,
        tracking=True,
    )
    # path of state mixed between sales & operation based on ticket type
    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),  # 1 > #2 button
            ('check', 'Checking'),  # 2 sales request
            ('search', 'Searching'),  # 2 sales request
            ('found', 'Found'),  # 3 > #4 feedback
            ('runout', 'Not avaliable'),  # 3 > loop #2 ask for reason feedback
            ('reserve', 'Reserve a Maid'),  # 4 > #5 request
            ('confirm', 'Sponser confirm'),  # 5 >#6 button
            ('hiring', 'Hiring'),  # 7 > #8 sales request
            ('garanty', 'Start 90days Garanty'),  # 8 > # 9 button
            # once operation close its ticket it will change sales ticket State
            ('closed', 'Closed'),  # 9
        ],
        default='draft',
        readonly=False,
        tracking=True,
    )
    ticket_type = fields.Selection(
        string='Ticket Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Sponser Transfer'),
        ],
        required=True,
        tracking=True,
    )
    sponser_name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )
    sponser_phone = fields.Char(
        string='Phone',
        required=True,
        tracking=True,
    )
    sponser_email = fields.Char(
        string='Email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Link to Sponser',
        tracking=True,
    )
    # maid search data
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
        related='company_id.currency_id',
        readonly=False,
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
        string='Children No',
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
        string="Responsable",
        comodel_name='res.users',
        required=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
    maids_id = fields.Many2one(
        comodel_name='housemaid.maids',
        string='Maid',
        help='Maids Check, Reserved or Hired',
        tracking=True,
    )
    garanty_day = fields.Date(
        string='Start Garanty Date',
        required=False,
        tracking=True,
    )
    action_maids_ids = fields.One2many(
        comodel_name='housemaid.maids',
        inverse_name='tickets_id',
        string='Maids Actions',
    )
    search_maids_ids = fields.Many2many(
        comodel_name='housemaid.maids',
        compute='_search_maids',
        string='Maids Search',
        # store=True,
    )

    @api.depends('jobs_id', 'country_id', 'monthly_salary')
    def _search_maids(self):
        self.ensure_one()
        maids_ids = self.env['housemaid.maids'].search(
            [
                ('state', 'not in', ('backout', 'reserve')),
                ('active', '=', True),
                ('tickets_id', '=', False),
            ]
        )
        if self.jobs_id != False:
            maids_ids1 = maids_ids.filtered(
                lambda maids: maids.jobs_id.id == self.jobs_id.id)
        else:
            maids_ids1 = maids_ids

        if len(self.country_id) == 1:
            maids_ids2 = maids_ids1.filtered(
                lambda maids: maids.country_id.id == self.country_id.id)
        else:
            maids_ids2 = maids_ids1

        if self.monthly_salary != 0:
            maids_ids3 = maids_ids2.filtered(
                lambda maids: maids.monthly_salary == self.monthly_salary)
        else:
            maids_ids3 = maids_ids2

        self.search_maids_ids = [(6, 0, maids_ids3.ids)]
