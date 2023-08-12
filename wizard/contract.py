from odoo import api, fields, models, _
from odoo.exceptions import UserError


class contract(models.TransientModel):
    _name = 'housemaid.contract'
    _description = 'Contract Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def default_get(self, fields):
        res = super(contract, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            ticket_rec = self.env['housemaid.tickets'].browse(int(active_id))
            res['tickets_id'] = ticket_rec.id
            res['sponsers_id'] = ticket_rec.sponsers_id
            res['maids_id'] = ticket_rec.maids_id
            res['offices_id'] = ticket_rec.offices_id
            res['user_id'] = ticket_rec.user_id
            print(active_id)
        return res

    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=True,
        string='Ticket no.',
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('sales', 'Sales'),
            ('transfer', 'Transfer'),
            ('temp', 'Temporary'),
        ],
        required=False,
        tracking=True,
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
        required=True,
        tracking=True,
    )
    new_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
        required=False,
        tracking=True,
    )
    maids_id = fields.Many2one(
        comodel_name='housemaid.maids',
        string='Maid',
        required=True,
        tracking=True,
    )
    offices_id = fields.Many2one(
        'housemaid.offices',
        string='Offices',
        related='maids_id.offices_id',
        required=True,
        tracking=True,
    )
    contract_no = fields.Char(
        string='Contract No.',
        required=True,
        tracking=True,
    )
    start_contract = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
    )
    end_contract = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
    )
    visa_no = fields.Char(
        string='Visa No.',
        required=True,
        tracking=True,
    )
    user_id = fields.Many2one(
        string="Responsable",
        comodel_name='res.users',
        required=True,
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
    description = fields.Text(
        string='Description',
        required=True,
        tracking=True,
    )

    def action_create_contract(self):
        self.ensure_one()
        context = dict(self.env.context or {})
        user_id = context.get('user_id', False)
        tickets_id = context.get('tickets_id', False)
        # change ticket state

        print('action_closed_ticket')
