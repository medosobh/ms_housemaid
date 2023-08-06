from odoo import api, fields, models, _
from odoo.exceptions import UserError


class tickets(models.Model):
    _name = 'housemaid.tickets'
    _description = 'Records of Ticket.'
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
            ('draft', 'Draft Request'),
            ('available', 'Operation Confirm Maid avaliable'),
            ('runout', 'Maid is Not avaliable'),
            ('reserve', 'Maid Reserved'),
            ('confirm', 'Sponser confirm the Maid'),
            ('90days', 'Maid in 90days Garanty'),
            # sales ask for 1 of 3 tiket type
            ('search', 'Search for Maid'),
            ('insure', 'Insure Maid avaliable'),
            ('hiring', 'Hiring the Maid'),
            # once operation close its ticket it will change sales ticket State
            ('closed', 'Ticket Closed'),
        ],
        default='draft',
        readonly=False,
        tracking=True,
    )
    ticket_type = fields.Selection(
        string='Ticket Type',
        selection=[
            ('sales', 'Sales'),
            ('search', 'Operation Search!'),
            ('toconfirm', 'Operation Confirming!'),
            ('tohire', 'Operation Hiring!'),
        ],
        tracking=True,
    )
    name = fields.Char(
        string='Name',
        tracking=True,
    )
    sponser_phone = fields.Char(
        string='Phone',
        tracking=True,
    )
    sponser_email = fields.Char(
        string='Email',
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Link to Sponser',
        tracking=True,
    )
    # maid search data
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
        readonly=True,
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
    arabic_lang = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        string="Arabic Language",
        help='Set the level language'
    )
    english_lang = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        string="English Language",
        help='Set the level language'
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
    skills_cleaning = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Cleaning",
        help='Set the overall skills level.',
        tracking=True,
    )
    skills_arabic_cooking = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Arabic Cooking",
        help='Set the overall skills level.',
        tracking=True,
    )
    skills_baby_sitting = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Baby Sitting",
        help='Set the overall skills level.',
        tracking=True,
    )
    skills_washing = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Washing",
        help='Set the overall skills level.',
        tracking=True,
    )
    skills_ironing = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        string="Ironing",
        help='Set the overall skills level.',
        tracking=True,
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        help="Country of Office.",
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
        string="Sales/Operation Man",
        comodel_name='res.users',
        required=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
    maids_ids = fields.Many2many(
        comodel_name='housemaid.maids',
        compute='_search_maids',
        store=True,
        string='Maids Search Result',
    )

    @api.onchange('country_id','monthly_salary')
    def _search_maids(self):
        maids_ids = self.env['housemaid.maids'].search(
            [
                ('state', '!=', 'backout'),
                ('ticket_id', '=', False),
                ('active', '=', True),
            ])
        if self.country_id != '':
            maids_ids.filtered(lambda maids: maids.country_id == self.country_id)
        else:
            maids_ids
            
        if self.monthly_salary == 0:
            maids_ids.filtered(lambda maids: maids.monthly_salary == self.monthly_salary)
        else:
            maids_ids
        
        self.maids_ids = [(6, 0, maids_ids.ids)]
