from odoo import api, fields, models, _
from odoo.exceptions import UserError


class contract(models.TransientModel):
    _name = 'housemaid.contract'
    _description = 'Close Ticket Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tickets_id = fields.Many2one(
        comodel_name='housemaid.tickets',
        required=False,
        string='Ticket no.',
    )
    sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Current Sponser',
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
        required=True,
        tracking=True,
    )
    
    contract_no = fields.Char(
        string='Contract No.',
        required=False,
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
        required=False,
        tracking=True,
    )
    user_id = fields.Many2one(
        string="Responsable",
        comodel_name='res.users',
        required=True,
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
