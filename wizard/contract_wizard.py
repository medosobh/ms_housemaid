from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class contractwizard(models.TransientModel):
    _name = 'housemaid.contractwizard'
    _description = 'Contract Wizard'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def default_get(self, fields):
        res = super(contractwizard, self).default_get(fields)
        active_id = self._context.get('active_id')
        if active_id:
            ticket_rec = self.env['housemaid.tickets'].browse(int(active_id))
            res['tickets_id'] = ticket_rec.id
            res['old_sponsers_id'] = ticket_rec.old_sponsers_id
            res['new_sponsers_id'] = ticket_rec.new_sponsers_id
            res['maids_id'] = ticket_rec.maids_id
            res['offices_id'] = ticket_rec.offices_id
            res['user_id'] = ticket_rec.user_id
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
    old_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='Old Sponser',
        required=True,
        tracking=True,
    )
    new_sponsers_id = fields.Many2one(
        'housemaid.sponsers',
        string='New Sponser',
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
    air_ticket_no = fields.Char(
        string='Air Ticket No.',
        required=True,
        tracking=True
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
        required=False,
        tracking=True,
    )

    def action_create_contract(self):
        self.ensure_one()
        vals = {
            'issue_date': date.today(),
            'tickets_id': self.tickets_id.id,
            'type': self.type,
            'old_sponsers_id': self.old_sponsers_id.id,
            'new_sponsers_id': self.new_sponsers_id.id,
            'maids_id': self.maids_id.id,
            'offices_id': self.offices_id.id,
            'contract_no': self.contract_no,
            'start_contract': self.start_contract,
            'end_contract': self.end_contract,
            'visa_no': self.visa_no,
            'user_id': self.user_id.id,
            'country_id': self.country_id.id,
            'company_id': self.company_id.id,
            'description': self.description,
        }
        self.env['housemaid.maidscontracts'].self.create(vals)
        # change ticket state
        record = self.env['housemaid.tickets'].browse(tickets_id)
        record.activity_schedule(
            'ms_housemaid.mail_act_hiring',
            user_id=self.user_id.id,
            note=f'Please check ticket {record.code}; a contract no: {self.contract_no} was created.'
        )