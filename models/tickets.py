from odoo import fields, models, _
from odoo.exceptions import UserError


class tickets(models.Model):
    _name = 'housemaid.tickets'
    _description = 'Records of Ticket.'
    _rec_name = 'code'
    _order = 'name ASC'
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one equipment !"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )
    # path of state mixed between sales & operation based on ticket type
    state = fields.Selection(
        string='Status',
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
    )
    ticket_type = fields.Selection(
        string='field_name',
        selection=[
            ('sales', 'Sales'),
            ('search', 'Operation Search!'),
            ('toconfirm', 'Operation Confirming!'),
            ('tohire', 'Operation Hiring!'),
        ]
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Sales/Operation Man",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        ondelete='set null',
        help="Used to display the currency when tracking monetary values"
    )
