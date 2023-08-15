from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


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
            if vals['type'] == 'sales':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'housemaid.sales.tickets') or _('New')
            elif vals['type'] == 'transfer':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'housemaid.transfer.tickets') or _('New')
            elif vals['type'] == 'temp':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'housemaid.temporary.tickets') or _('New')
            else:
                raise UserError("Please select Ticket Type!")

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

    def action_found_ticket(self):
        self.ensure_one()
        self.state = 'found'

    def action_runout_ticket(self):
        self.ensure_one()
        self.state = 'runout'

    def action_confirm_ticket(self):
        self.ensure_one()
        if self.new_sponsers_id.id != False:
            self.state = 'confirm'
        else:
            raise UserError('Please Select Sponser before confirm!')

    @api.onchange('garanty_day')
    def action_garanty_ticket(self):
        self.ensure_one()
        if self.garanty_day != False:
            self.state = 'garanty'
            self.maids_id.garanty_day = self.garanty_day
            self.close_ticket_day = self.garanty_day + timedelta(days=90)

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
            ('search', 'Searching'),  # 2 sales request
            ('check', 'Checking'),  # 2 sales request
            ('found', 'Found or Available'),  # 3 > #4 feedback
            ('runout', 'Not Avaliable'),  # 3 > loop #2 ask for reason feedback
            ('confirm', 'Sponser confirm'),  # 5 >#6 button
            ('hiring', 'Hiring'),  # 7 > #8 sales request
            ('garanty', 'Garanty'),  # 8 > # 9 button
            # once operation close its ticket it will change sales ticket State
            ('closed', 'Closed'),  # 9
        ],
        default='draft',
        readonly=False,
        tracking=True,
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Transfer'),
            ('temp', 'Temporary'),
        ],
        required=True,
        tracking=True,
    )
    new_sponser_name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )
    new_sponser_phone = fields.Char(
        string='Phone',
        required=True,
        tracking=True,
    )
    new_sponser_email = fields.Char(
        string='Email',
        required=True,
        default=lambda self: _('name@mail.com'),
        tracking=True,
    )
    new_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='New Sponser',
        readonly=True,
        tracking=True,
    )
    old_sponser_name = fields.Char(
        string='Name',
        related='maids_id.sponsers_id.name',
        readonly=True,
        tracking=True,
    )
    old_sponser_phone = fields.Char(
        string='Phone',
        related='maids_id.sponsers_id.phone',
        readonly=True,
        tracking=True,
    )
    old_sponser_email = fields.Char(
        string='Email',
        related='maids_id.sponsers_id.email',
        readonly=True,
        tracking=True,
    )
    old_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Old Sponser',
        related='maids_id.sponsers_id',
        readonly=True,
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
    user_id = fields.Many2one(
        string="Responsable",
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
    offices_id = fields.Many2one(
        'housemaid.offices',
        string='Offices',
        related='maids_id.offices_id',
        readonly=True,
        required=True,
        tracking=True,
    )
    garanty_day = fields.Date(
        string='Start Garanty Date',
        default=False,
        required=False,
        tracking=True,
    )
    close_ticket_day = fields.Date(
        string='Garanty Expire Date',
        required=False,
        tracking=True,
    )
    search_maids_ids = fields.Many2many(
        comodel_name='housemaid.maids',
        compute='_search_maids',
        string='Maids Search',
        # store=True,
    )
    action_maids_ids = fields.One2many(
        comodel_name='housemaid.maids',
        inverse_name='tickets_id',
        string='Maids Actions',
    )
    search_maids_ids_count = fields.Integer(
        string='Search count',
        compute='_compute_search_count',
    )
    action_maids_ids_count = fields.Integer(
        string='Action count',
        compute='_compute_action_count',
    )

    @api.depends('search_maids_ids')
    def _compute_search_count(self):
        self.search_maids_ids_count = len(self.search_maids_ids)

    @api.depends('action_maids_ids')
    def _compute_action_count(self):
        self.action_maids_ids_count = len(self.action_maids_ids)

    @api.depends('jobs_id', 'country_id', 'monthly_salary', 'arabic_lang',
                 'english_lang', 'religion', 'gender', 'marital_status', 'skin_color',
                 'age', 'hight', 'weight', 'skills_cleaning', 'skills_arabic_cooking',
                 'skills_baby_sitting', 'skills_washing', 'skills_ironing',
                 'skills_googlelocation', 'skills_driving')
    def _search_maids(self):
        self.ensure_one()
        # test list
        # jobs_id  ==
        # country_id ==
        # 2 condition with id
        # monthly_salary ==
        # arabic_lang ==
        # english_lang ==
        # religion ==
        # gender ==
        # marital_status ==
        # skin_color ==
        # skills_cleaning ==
        # skills_arabic_cooking ==
        # skills_baby_sitting ==
        # skills_washing ==
        # skills_ironing ==
        # skills_googlelocation ==
        # skills_driving ==
        # 16 condition ==
        # age +- 2
        # hight +- 1 feet
        # weight +- 5 kg
        # 3 condition with range
        id_fields = ('jobs_id', 'country_id')
        fields = ('monthly_salary', 'arabic_lang',
                  'english_lang', 'religion', 'gender', 'marital_status', 'skin_color',
                  'skills_cleaning', 'skills_arabic_cooking',
                  'skills_baby_sitting', 'skills_washing', 'skills_ironing',
                  'skills_googlelocation', 'skills_driving'
                  )
        range_fields = ('age', 'hight', 'weight')

        self.search_maids_ids = []
        if self.type == 'sales':
            domain = [
                ('state', 'in', ('draft', 'check', 'open', 'ready')),
                ('active', '=', True),
                ('tickets_id', '=', False)
            ]

            for field in id_fields:
                if self[field].id != False:
                    print('test1')
                    conditions = (field+'.id', '=', self[field].id)
                    domain.append(conditions)
                print(domain)

            for field in fields:
                if self[field] != False:
                    print('test2')
                    conditions = (field, '=', self[field])
                    domain.append(conditions)
                print(domain)

            for field in range_fields:
                if self[field] != False:
                    print('test3')
                    min_value = self[field] * 0.9
                    max_value = self[field] * 1.1
                    conditions = ([
                        '&',
                        (field, '<', max_value),
                        (field, '>', min_value)
                    ])
                    domain.append(conditions)
                print(domain)

            maids_ids = self.env['housemaid.maids'].search(
                [domain]
            )
            print(maids_ids)

            self.search_maids_ids = [(6, 0, maids_ids.ids)]
        elif self.type == 'transfer':
            domain = [
                ('state', 'in', ('ready', 'transfer')),
                ('active', '=', True),
            ]

            for field in id_fields:
                if self[field].id != False:
                    print('test1')
                    conditions = (field+'.id', '=', self[field].id)
                    domain.append(conditions)
                print(domain)

            for field in fields:
                if self[field] != False:
                    print('test2')
                    conditions = (field, '=', self[field])
                    domain.append(conditions)
                print(domain)

            for field in range_fields:
                if self[field] != False:
                    print('test3')
                    min_value = self[field] * 0.9
                    max_value = self[field] * 1.1
                    conditions = ([
                        '&',
                        (field, '<', max_value),
                        (field, '>', min_value)
                    ])
                    domain.append(conditions)
                print(domain)

            maids_ids = self.env['housemaid.maids'].search(
                [domain]
            )
            print(maids_ids)

            self.search_maids_ids = [(6, 0, maids_ids.ids)]

        elif self.type == 'temp':
            domain = [
                ('state', 'in', ('ready', 'transfer')),
                ('active', '=', True),
            ]

            for field in id_fields:
                if self[field].id != False:
                    print('test1')
                    conditions = (field+'.id', '=', self[field].id)
                    domain.append(conditions)
                print(domain)

            for field in fields:
                if self[field] != False:
                    print('test2')
                    conditions = (field, '=', self[field])
                    domain.append(conditions)
                print(domain)

            for field in range_fields:
                if self[field] != False:
                    print('test3')
                    min_value = self[field] * 0.9
                    max_value = self[field] * 1.1
                    conditions = ([
                        '&',
                        (field, '<', max_value),
                        (field, '>', min_value)
                    ])
                    domain.append(conditions)
                print(domain)

            maids_ids = self.env['housemaid.maids'].search(
                [domain]
            )
            print(maids_ids)

            self.search_maids_ids = [(6, 0, maids_ids.ids)]

            maids_ids = self.env['housemaid.maids'].search(
                [domain]
            )
        else:
            self.search_maids_ids = []
