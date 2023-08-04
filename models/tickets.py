from odoo import fields, models, _
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

    code = fields.Char(
        string='Code',
        required=True,
        default=lambda self: _('New'),
        copy=False,
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
    sponser_name = fields.Char(
        string='Sponser Name',
        tracking=True,
    )
    sponser_phone = fields.Char(
        string='Sponser Phone',
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Sponsers',
        tracking=True,
        )
    # maid search data
    country_id = fields.Many2one(
        string="Maid Country",
        comodel_name='res.country',
        help="Country of Office.",
        tracking=True,
    )
    maid_marital_status = fields.Selection(
        string='Marital Status',
        selection=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced'),
        ],
        tracking=True,
    )
    maid_religion = fields.Selection(
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
    maid_gender = fields.Selection(
        string='Gender',
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
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
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        related='company_id.currency_id',
        readonly=True,
        ondelete='set null',
        help="Used to display the currency when tracking monetary values",
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True,
    )
